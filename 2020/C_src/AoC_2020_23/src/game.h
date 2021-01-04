#ifndef GAME_H
#define GAME_H


typedef struct
{
	int stringLength;
	int maxValue;
	int *values;
} StringInput;


StringInput* createStringInput(const char *input_string, int max_value);

void freeStringInput(StringInput **input);

void game_1(const StringInput *input, int rounds);

void game_2(const StringInput *input, int rounds);


#endif
