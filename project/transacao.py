import json
from datetime import datetime


ARQUIVO_DADOS = "transacoes.json"

def carregar_transacoes():
    try:
        with open(ARQUIVO_DADOS, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def salvar_transacoes(transacoes):
    with open(ARQUIVO_DADOS, "w") as file:
        json.dump(transacoes, file, indent=4)

def adicionar_transacao(tipo, categoria, valor, descricao, data=None):
    if not data:
        data = datetime.now().strftime("%Y-%m-%d")
    transacoes = carregar_transacoes()
    transacao = {
        "tipo": tipo,
        "categoria": categoria,
        "valor": valor,
        "descricao": descricao,
        "data": data
    }
    transacoes.append(transacao)
    salvar_transacoes(transacoes)

def filtrar_por_data(transacoes, data_inicio, data_fim):
    return [
        t for t in transacoes
        if data_inicio <= datetime.strptime(t["data"], "%Y-%m-%d") <= data_fim
    ]

def listar_transacoes():
    transacoes = carregar_transacoes()
    return transacoes

def calcular_resumo():
    transacoes = carregar_transacoes()
    total_receitas = sum(t["valor"] for t in transacoes if t["tipo"] == "receita")
    total_despesas = sum(t["valor"] for t in transacoes if t["tipo"] == "despesa")
    saldo = total_receitas - total_despesas
    return total_receitas, total_despesas, saldo
