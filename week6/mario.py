def main():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                break
        except ValueError:
            pass

    print_blocks(height)

def print_blocks(height):
    for i in range(1, height + 1):
        print(" " * (height - i) + "#" * i)

main()
