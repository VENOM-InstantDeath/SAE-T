#ifndef VECTOR_H
#define VECTOR_H
#include <stdio.h>
#include <stdlib.h>

struct vector {
	char** str;
	int size;
};

struct ivector {
	int* num;
	int size;
};

struct string {
	char *str;
	int size;
};

void vector_init(struct vector* sm);
int vector_add(struct vector* sm, char* str);
int vector_addstr(struct vector* sm, struct string *st);
int vector_pop(struct vector* sm);
int vector_popat(struct vector* sm, int index);
void vector_free(struct vector* sm);


void ivector_init(struct ivector* sm);
int ivector_add(struct ivector* sm, int num);
int ivector_pop(struct ivector* sm);
int ivector_popat(struct ivector* sm, int index);
void ivector_free(struct ivector* sm);


void string_init(struct string* st);
int string_add(struct string* st, char* str);
int string_addch(struct string* st, char ch);
int string_addchat(struct string* st, char ch, int index);
int string_pop(struct string* st);
int string_popat(struct string* st, int index);
struct vector string_split(char *str, char sep);
void string_free(struct string* st);

#endif
