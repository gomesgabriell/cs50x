#include "cs50.h"
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int coleman_liau(string text);

int main(void)
{
    string text = get_string("Text: ");

    int level = coleman_liau(text);

    if (level >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (level < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", level);
    }
}

int coleman_liau(string text)
{
    float index, l, s;
    int letters = 0, words = 1, sentences = 0;
    int size = strlen(text);

    for (int i = 0; i < size; i++)
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }

        if (isspace(text[i]))
        {
            words += 1;
        }

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }

    l = (float) letters / (float) words * 100;
    s = (float) sentences / (float) words * 100;
    index = round(0.0588 * l - 0.296 * s - 15.8);

    return (int) index;
}