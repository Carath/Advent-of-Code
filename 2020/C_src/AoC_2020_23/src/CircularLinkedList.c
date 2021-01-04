#include <stdio.h>
#include <stdlib.h>

#include "CircularLinkedList.h"


inline Node* createNode(ValueType value, const Node *nextNode)
{
	Node *node = (Node*) calloc(1, sizeof(Node));
	node -> value = value;
	node -> next = (Node*) nextNode;
	return node;
}


CircularLinkedList* initCircularLinkedList(void)
{
	return (CircularLinkedList*) calloc(1, sizeof(CircularLinkedList));
}


void freeCircularLinkedList(CircularLinkedList **list)
{
	if (!list || !*list)
		return;

	Node *node = (*list) -> start;
	while (node != NULL)
	{
		Node *temp = node -> next;
		free(node);
		node = temp;
		if (node == (*list) -> start)
			break;
	}

	free(*list);
	*list = NULL;
}


void printCircularLinkedList(const CircularLinkedList *list) // int specific!
{
	if (!list)
		return;

	Node *node = list -> start;
	while (node != NULL)
	{
		printf("%d, ", node -> value);
		node = node -> next;
		if (node == list -> start)
			break;
	}
	printf("\n");
}


inline void addLeft(CircularLinkedList *list, ValueType value)
{
	list -> start = createNode(value, list -> start);
	if (list -> length == 0)
		list -> end = list -> start;
	list -> end -> next = list -> start;
	++(list -> length);
}


void addRight(CircularLinkedList *list, ValueType value)
{
	if (list -> end == NULL)
		addLeft(list, value);
	else
	{
		list -> end -> next = createNode(value, list -> start);
		list -> end = list -> end -> next;
		++(list -> length);
	}
}


Node* find(const CircularLinkedList *list, ValueType value)
{
	Node *node = list -> start;
	while (node != NULL)
	{
		if (node -> value == value)
			return node;
		node = node -> next;
		if (node == list -> start)
			break;
	}
	return NULL;
}
