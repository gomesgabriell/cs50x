import csv
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    database = []
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

    with open(sys.argv[2], 'r') as file:
        sequence = file.read()

    str_sequences = list(database[0].keys())[1:]
    str_counts = {}

    for str_seq in str_sequences:
        str_counts[str_seq] = longest_match(sequence, str_seq)

    for person in database:
        match = True
        for str_seq in str_sequences:
            if int(person[str_seq]) != str_counts[str_seq]:
                match = False
                break

        if match:
            print(person["name"])
            return

    print("No match")

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0

        while True:

            start = i + count * subsequence_length
            end = start + subsequence_length

            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run

main()