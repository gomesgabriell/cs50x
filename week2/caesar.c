#include "cs50.h"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool is_digit(string text);
void caesar(string text, int key);

int main(int argc, string argv[])
{
    if (argc != 2 || !is_digit(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");
    caesar(plaintext, key);

    return 0;
}

bool is_digit(string text)
{
    int size = strlen(text);
    for (int i = 0; i < size; i++)
    {
        if (!isdigit(text[i]))
        {
            return false;
        }
    }
    return true;
}

void caesar(string text, int key)
{
    int size = strlen(text);

    for (int i = 0; i < size; i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                printf("%c", ((text[i] - 64 + key) % 26) + 64);
            }
            else
            {
                printf("%c", ((text[i] - 96 + key) % 26) + 96);
            }
        }
        else
        {
            printf("%c", text[i]);
        }
    }

    printf("\n");
}