#ifndef CIRCULAR_LINKED_LIST_H
#define CIRCULAR_LINKED_LIST_H


typedef int ValueType;

typedef struct node
{
	ValueType value;
	struct node *next;
} Node;

typedef struct
{
	Node *start;
	Node *end;
	size_t length;
} CircularLinkedList;


Node* createNode(ValueType value, const Node *nextNode);

CircularLinkedList* initCircularLinkedList(void);

void freeCircularLinkedList(CircularLinkedList **list);

void printCircularLinkedList(const CircularLinkedList *list); // int specific!

void addLeft(CircularLinkedList *list, ValueType value);

void addRight(CircularLinkedList *list, ValueType value);

Node* find(const CircularLinkedList *list, ValueType value);


#endif
