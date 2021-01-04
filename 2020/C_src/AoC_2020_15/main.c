// gcc -Wall -O2 main.c -o exec

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define ARRAY_LENGTH(array) (sizeof(array) / sizeof(*(array)))


typedef struct
{
	int count;
	int age1;
	int age2;
} ValueData;

typedef struct
{
	ValueData *hashMap;
	int mapLength;
	int currentEpoch;
	int lastValue;
} Game;


void initGame(Game *game, const int *sequence, int sequence_length, int target_rank);
void freeGame(Game *game);
inline void addValue(Game *game, int value);
inline int nextState(Game *game);


int main(void)
{
	// int sequence[] = {0, 3, 6};
	int sequence[] = {0, 13, 1, 8, 6, 15};

	int sequence_length = ARRAY_LENGTH(sequence);

	// int rank = 2020;
	int rank = 30000000;

	Game game = {0};
	initGame(&game, sequence, sequence_length, rank);

	for (int i = 0; i < rank - sequence_length; ++i)
		nextState(&game);

	printf("\nResult: %d\n\n", game.lastValue);

	freeGame(&game);

	return 0;
}


void initGame(Game *game, const int *sequence, int sequence_length, int target_rank)
{
	if (!game)
	{
		printf("Cannot init a non existing Game object.\n");
		return;
	}

	if (game -> hashMap) // in case initGame() has already been called.
		free(game -> hashMap);

	game -> hashMap = (ValueData*) calloc(target_rank, sizeof(ValueData));
	game -> mapLength = target_rank;
	game -> currentEpoch = 1;

	if (!game -> hashMap)
	{
		printf("\nOut of Memory!\n\n");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < sequence_length; ++i)
		addValue(game, sequence[i]);
}


void freeGame(Game *game)
{
	if (!game)
		return;

	free(game -> hashMap);
	memset(game, 0, sizeof(Game));
}


inline void addValue(Game *game, int value)
{
	if (value >= game -> mapLength) // values are never < 0.
	{
		printf("\nMap too small! (value: %d)\n\n", value);
		exit(EXIT_FAILURE);
	}

	ValueData *dataToUpdate = game -> hashMap + value;
	++(dataToUpdate -> count);
	dataToUpdate -> age1 = dataToUpdate -> age2;
	dataToUpdate -> age2 = game -> currentEpoch;
	++(game -> currentEpoch);
	game -> lastValue = value;
}


inline int nextState(Game *game)
{
	ValueData *lastValueData = game -> hashMap + game -> lastValue;
	int new_value = (lastValueData -> count == 1) ? 0 : lastValueData -> age2 - lastValueData -> age1;
	// printf("Epoch %d, choosing: %d\n", game -> currentEpoch, new_value);
	addValue(game, new_value);
	return new_value;
}
