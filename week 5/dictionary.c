#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"  // No lib

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

bool find_word(node *head, const char *word);
void free_list(node *head);

int total_words = 0;

const unsigned int NUM_BUCKETS = 26;

node *hash_table[NUM_BUCKETS][LENGTH];

bool check(const char *word)
{
    int index = hash(word);
    int length = strlen(word) - 1;
    node *current = hash_table[index][length];
    return find_word(current, word);
}

bool find_word(node *head, const char *word)
{
    if (head == NULL)
    {
        return false;
    }
    if (strcasecmp(head->word, word) == 0)
    {
        return true;
    }
    return find_word(head->next, word);
}

unsigned int hash(const char *word)
{
    return toupper(word[0]) - 'A';
}

bool load(const char *dictionary)
{
    for (int i = 0; i < NUM_BUCKETS; i++)
    {
        for (int j = 0; j < LENGTH; j++)
        {
            hash_table[i][j] = NULL;
        }
    }

    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word_buffer[LENGTH + 1];

    while (fscanf(file, "%s", word_buffer) != EOF)
    {
        int index = hash(word_buffer);
        int length = strlen(word_buffer) - 1;

        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        strcpy(new_node->word, word_buffer);
        new_node->next = NULL;

        if (hash_table[index][length] == NULL)
        {
            hash_table[index][length] = new_node;
        }
        else
        {
            new_node->next = hash_table[index][length];
            hash_table[index][length] = new_node;
        }

        total_words++;
    }

    fclose(file);
    return true;
}

unsigned int size(void)
{
    return total_words;
}

bool unload(void)
{
    for (int i = 0; i < NUM_BUCKETS; i++)
    {
        for (int j = 0; j < LENGTH; j++)
        {
            if (hash_table[i][j] != NULL)
            {
                free_list(hash_table[i][j]);
            }
        }
    }
    return true;
}

void free_list(node *head)
{
    if (head == NULL)
    {
        return;
    }
    free_list(head->next);
    free(head);
}