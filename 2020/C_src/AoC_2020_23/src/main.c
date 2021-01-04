#include <stdio.h>

#include "game.h"


int main(void)
{
	// const char input_string[] = "389125467";
	const char input_string[] = "253149867";

	printf("\nInput: %s\n", input_string);

	// int max_value = 9;
	// int rounds = 100;

	int max_value = 1000000;
	int rounds = 10000000;

	StringInput *input = createStringInput(input_string, max_value);

	// game_1(input, rounds);
	game_2(input, rounds); // ~ 4.5x faster than game_1()

	freeStringInput(&input);

	return 0;
}
