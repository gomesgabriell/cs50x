#include "cs50.h"
#include <stdio.h>

void print_bricks(int h);

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    } while (height < 1);
    
    print_bricks(height);
}

void print_bricks(int h)
{
    for (int i = 1; i <= h; i++)
    {
        for (int j = 0; j < h - i; j++)
        {
            printf(" ");
        }

        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}