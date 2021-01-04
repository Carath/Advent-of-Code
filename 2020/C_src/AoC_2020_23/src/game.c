#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "game.h"
#include "CircularLinkedList.h"


StringInput* createStringInput(const char *input_string, int max_value)
{
	StringInput *input = (StringInput*) calloc(1, sizeof(StringInput));

	input -> stringLength = strlen(input_string);
	input -> maxValue = max_value;
	input -> values = (int*) calloc(input -> stringLength, sizeof(int));

	if (!input -> values)
	{
		printf("\nNot enough memory.\n");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < input -> stringLength; ++i)
	{
		int value = input_string[i] - 48; // ascii to int.
		input -> values[i] = value;
	}

	if (max_value < input -> stringLength)
	{
		printf("\nMax value must be at least 'input -> stringLength', changed to %d.\n",
			input -> stringLength);
		input -> maxValue = input -> stringLength;
	}

	return input;
}


void freeStringInput(StringInput **input)
{
	if (!input || !*input)
		return;

	free((*input) -> values);
	free(*input);
	*input = NULL;
}


static inline int find_dest(int max_value, int current_cup, int picked_1, int picked_2, int picked_3)
{
	do {
		--current_cup;
		if (current_cup < 1)
			current_cup = max_value;
	} while (current_cup == picked_1 || current_cup == picked_2 || current_cup == picked_3);
	return current_cup;
}


// Uses circular linked lists + node hash map:
void game_1(const StringInput *input, int rounds)
{
	// Setup:

	CircularLinkedList *cups = initCircularLinkedList();

	// Values range from 1 to input -> maxValue, but index 0 is allowed:
	Node **node_addresses = (Node**) calloc(input -> maxValue + 1, sizeof(Node*));

	if (!node_addresses)
	{
		printf("\nNot enough memory.\n");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < input -> stringLength; ++i)
	{
		int value = input -> values[i];
		addRight(cups, value);
		node_addresses[value] = cups -> end;
	}

	for (int i = input -> stringLength + 1; i <= input -> maxValue; ++i)
	{
		addRight(cups, i);
		node_addresses[i] = cups -> end;
	}

	// Tight loop:

	Node *current_cup_node = cups -> start;

	for (int i = 0; i < rounds; ++i)
	{
		Node *p1 = current_cup_node -> next;
		Node *p2 = p1 -> next;
		Node *p3 = p2 -> next;

		int dest_cup_value = find_dest(input -> maxValue, current_cup_node -> value, p1 -> value, p2 -> value, p3 -> value);
		Node *dest_cup_node = node_addresses[dest_cup_value];

		current_cup_node -> next = p3 -> next;
		p3 -> next = dest_cup_node -> next;
		dest_cup_node -> next = p1;

		current_cup_node = current_cup_node -> next;
	}

	// Result and freeing:

	Node *node_of_1 = node_addresses[1];
	int next_1 = node_of_1 -> next -> value;
	int next_2 = node_of_1 -> next -> next -> value;
	long result = (long) next_1 * next_2;

	// printCircularLinkedList(cups);
	printf("\n-> %d, %d\n\nResult: %ld\n", next_1, next_2, result);

	free(node_addresses);
	freeCircularLinkedList(&cups);
}


// Simpler version: hash map of next indexes!
void game_2(const StringInput *input, int rounds)
{
	// Setup:

	// Values range from 1 to input -> maxValue, but index 0 is allowed:
	int *idx_next_map = (int*) calloc(input -> maxValue + 1, sizeof(int));

	if (!idx_next_map)
	{
		printf("\nNot enough memory.\n");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < input -> stringLength - 1; ++i)
		idx_next_map[input -> values[i]] = input -> values[i + 1];

	int last_input_value = input -> values[input -> stringLength - 1];

	if (input -> maxValue > input -> stringLength)
	{
		idx_next_map[last_input_value] = input -> stringLength + 1;

		for (int i = input -> stringLength + 1; i < input -> maxValue; ++i)
			idx_next_map[i] = i + 1;

		idx_next_map[input -> maxValue] = input -> values[0];
	}
	else
		idx_next_map[last_input_value] = input -> values[0];

	// Tight loop:

	int current_index = input -> values[0];

	for (int i = 0; i < rounds; ++i)
	{
		int p1 = idx_next_map[current_index];
		int p2 = idx_next_map[p1];
		int p3 = idx_next_map[p2];

		int dest_cup_value = find_dest(input -> maxValue, current_index, p1, p2, p3);

		idx_next_map[current_index] = idx_next_map[p3];
		idx_next_map[p3] = idx_next_map[dest_cup_value];
		idx_next_map[dest_cup_value] = p1;
		current_index = idx_next_map[current_index];
	}

	// Result and freeing:

	int next_1 = idx_next_map[1];
	long result = (long) next_1 * idx_next_map[next_1];

	printf("\n-> %d, %d\n\nResult: %ld\n", next_1, idx_next_map[next_1], result);

	free(idx_next_map);
}
