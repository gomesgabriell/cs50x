def main():
    text = input("Text: ")

    level = coleman_liau(text)

    if level >= 16:
        print("Grade 16+")
    elif level < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {level}")

def coleman_liau(text):
    letters = 0
    words = 0
    sentences = 0

    for char in text:
        if char.isalpha():
            letters += 1
        elif char.isspace():
            words += 1
        elif char in ['.', '!', '?']:
            sentences += 1

    if len(text.strip()) > 0:
        words += 1

    l = letters / words * 100
    s = sentences / words * 100

    return round(0.0588 * l - 0.296 * s - 15.8)

main()