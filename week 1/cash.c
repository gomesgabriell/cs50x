#include "cs50.h"
#include <stdio.h>

int minimum_coins(int change);

int main(void)
{
    int change;
    int coins;

    do
    {
        change = get_int("Change owed: ");
    } while (change < 0);
        
    coins = minimum_coins(change);

    printf("%d\n", coins);
}

int minimum_coins(int change)
{
    int coins = 0;

    coins += change / 25;
    change %= 25;

    coins += change / 10;
    change %= 10;

    coins += change / 5;
    change %= 5;

    coins += change / 1;
    change %= 1;

    return coins;
}