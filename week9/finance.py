''' app.py '''

import os

from cs50 import SQL  # No lib
from flask import Flask, flash, redirect, render_template, request, session  # No lib
from flask_session import Session  # No lib
from werkzeug.security import check_password_hash, generate_password_hash  # No lib

from helpers import apology, login_required, lookup, usd  # No lib

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT symbol, SUM(num_shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    stocks_total = 0

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["total_value"] = quote["price"] * stock["total_shares"]
        stocks_total += stock["total_value"]

    grand_total = stocks_total + cash

    return render_template("index.html", stocks=stocks, cash=cash, grand_total=grand_total, stocks_total=stocks_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        quote = lookup(symbol)
        if not symbol or not shares:
            return apology("incomplete details")
        elif not quote:
            return apology("invalid symbol")
        elif not shares.isdigit() or int(shares) <= 0:
            return apology("invalid shares")

        shares = int(shares)
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        total_price = shares * quote['price']

        if user['cash'] < total_price:
            return apology("not enough cash")

        db.execute("""INSERT INTO transactions (user_id, username, symbol, num_shares, total_price, date, type)
                   VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
                   """, session["user_id"], user["username"], symbol, shares, total_price, "purchase")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", user['cash'] - total_price, session['user_id'])

        flash(f"Successfully purchased {shares} shares of {symbol} for {usd(total_price)}")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC", session['user_id'])
    for transaction in transactions:
        if transaction["num_shares"] < 0:
            transaction["num_shares"] *= -1

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")
        return render_template("quoted.html", quote=quote, usd_func=usd)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("confirmation")

        if not username or len(username) < 3:
            return apology("invalid username", 400)
        elif not password1 or len(password1) < 3:
            return apology("invalid password", 400)
        elif not password2 or (password1 != password2):
            return apology("passwords don't match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username already exists", 400)

        hashed = generate_password_hash(password1)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT symbol, SUM(num_shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["total_value"] = quote["price"] * stock["total_shares"]

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        quote = lookup(symbol)
        if not symbol or not shares:
            return apology("incomplete details")
        elif not quote:
            return apology("invalid symbol")
        elif not shares.isdigit() or int(shares) <= 0:
            return apology("invalid shares")
        shares = int(shares)

        for stock in stocks:
            if stock["symbol"] == symbol:
                if shares > stock["total_shares"]:
                    return apology("not enough owned shares")
                else:
                    sale = shares * stock["price"]
                    db.execute("""INSERT INTO transactions (user_id, username, symbol, num_shares, total_price, date, type)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
                    """, session["user_id"], user["username"], symbol, -shares, sale, "sale")
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", user["cash"] + sale, session['user_id'])
                    flash(f"Successfully sold {shares} shares of {symbol} for {usd(sale)}")

                    return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])[0]

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not old_password or not new_password or not confirmation:
            return apology("incomplete details")
        elif not check_password_hash(user['hash'], old_password):
            return apology("incorrect old password")
        elif new_password != confirmation:
            return apology("new password and confirmation do not match")

        hashed = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed, user['id'])
        flash("Successfully changed password")

        return redirect("/account")

    else:
        return render_template("account.html", user=user)

'''sell.html

{% extends "layout.html" %}

{% block title %}
    Sell
{% endblock %}

{% block main %}
    <h1>Sell Stocks</h1>
    <br />
    <form action="/sell" method="post">
        <div class="mb-3">
            <select name="symbol" class="form-select" aria-label="Default select example">
                <option disabled selected value="">Select a stock</option>
                {% for stock in stocks %}
                    <option value="{{ stock['symbol'] }}">{{ stock['symbol'] }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="mb-3">
            <input name="shares" class="form-control mx-auto w-auto" type="text" placeholder="Number of Shares">
        </div>
        <div class="mb-3">
            <button class="btn btn-primary" type="submit">Sell</button>
        </div>
    </form>

{% endblock %}

'''

'''register.html

{% extends "layout.html" %}

{% block title %}
    Sign Up
{% endblock %}

{% block main %}
    <form action="/register" method="post">
        <div class="mb-3">
            <input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="username" placeholder="Choose a username" type="text">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="password" placeholder="Choose a password" type="password">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="confirmation" placeholder="Confirm password" type="password">
        </div>
        <button class="btn btn-primary" type="submit">Sign Up</button>
    </form>
{% endblock %}

'''

'''quoted.html

{% extends "layout.html" %}

{% block title %}
    Quote
{% endblock %}

{% block main %}
    <h1>Request for a Stock Quote</h1>
    <br />
    <h2>{{ quote["symbol"] }}</h2>
    <p>{{ usd_func(quote["price"]) }}</p>
{% endblock %}

'''

'''quote.html

{% extends "layout.html" %}

{% block title %}
    Quote
{% endblock %}

{% block main %}
    <h1>Request for a Stock Quote</h1>
    <form action="/quote" method="post">
        <div class="mb-3">
            <input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="symbol" placeholder="Enter a stock symbol" type="text">
        </div>
        <button class="btn btn-primary" type="submit">Request</button>
    </form>
{% endblock %}

'''

'''index.html

{% extends "layout.html" %}

{% block title %}
    Stock Portfolio
{% endblock %}

{% block main %}
    <h2>Your Stocks</h2>
    <br />
    <table class="table table-striped table-hover">
        <thead>
            <td>Stock Symbol</td>
            <td>No. of Shares Owned</td>
            <td>Current Price</td>
            <td>Total Value of Holding</td>
        </thead>
        <tbody>
            {% for stock in stocks %}
                <tr>
                    <td>{{ stock["symbol"] }}</td>
                    <td>{{ stock["total_shares"] }}</td>
                    <td>{{ stock["price"] | usd }}</td>
                    <td>{{ stock["total_value"] | usd }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <br />
    <table class="table table-striped table-hover">
        <thead>
            <td>Cash Balance</td>
            <td>Value of All Stocks Owned</td>
            <td>Total Value of Stocks Owned and Cash Balance</td>
        </thead>
        <tbody>
            <tr>
                <td>{{ cash | usd}}</td>
                <td>{{ stocks_total | usd }}</td>
                <td>{{ grand_total | usd }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}

'''

'''history.html

{% extends "layout.html" %}

{% block title %}
    History
{% endblock %}

{% block main %}
    <h1>Transaction History</h1>
    <br />
    <table class="table table-striped table-hover">
        <thead>
            <td>Transaction Type</td>
            <td>Stock Symbol</td>
            <td>No. of Shares</td>
            <td>Purchase/Sale Price</td>
            <td>Date and Time</td>
        </thead>
        <tbody>
            {% for transaction in transactions %}
                <tr>
                    <td>{{ transaction["type"] }}</td>
                    <td>{{ transaction["symbol"] }}</td>
                    <td>{{ transaction["num_shares"] }}</td>
                    <td>{{ transaction["total_price"] | usd }}</td>
                    <td>{{ transaction["date"] }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>

{% endblock %}

'''

'''buy.html

{% extends "layout.html" %}

{% block title %}
    Buy
{% endblock %}

{% block main %}
    <h1>Buy Stocks</h1>
    <br />
    <form action="/buy" method="post">
        <div class="mb-3">
            <input name="symbol" autocomplete="off" class="form-control mx-auto w-auto" autofocus type="text" placeholder="Stock Symbol">
        </div>
        <div class="mb-3">
            <input name="shares" class="form-control mx-auto w-auto" type="text" placeholder="Number of Shares">
        </div>
        <div class="mb-3">
            <button class="btn btn-primary" type="submit">Buy</button>
        </div>
    </form>

{% endblock %}

'''

'''account.html

{% extends "layout.html" %}

{% block title %}
    Account
{% endblock %}

{% block main %}
    <h1>{{ user["username"] }}</h1>
    <br />
    <h2>Change Password</h2>
    <br />
    <form action="/account" method="post">
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="old_password" placeholder="Enter old password" type="password">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="new_password" placeholder="Choose a new password" type="password">
        </div>
        <div class="mb-3">
            <input class="form-control mx-auto w-auto" name="confirmation" placeholder="Confirm new password" type="password">
        </div>
        <button class="btn btn-primary" type="submit">Change Password</button>
    </form>


{% endblock %}

'''