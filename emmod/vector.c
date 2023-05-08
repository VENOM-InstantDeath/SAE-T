#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vector.h"

void vector_init(struct vector* sm) {
	sm->str = malloc(sizeof(char*));
	sm->size=0;
}

int vector_add(struct vector* sm, char* str) {
	int size = strlen(str);
	if (size > 50) {return -1;}
	sm->str = realloc(sm->str, sizeof(char*)*sm->size+1);
	sm->str[sm->size] = str;
	sm->size++;
	return 0;
}

int vector_addstr(struct vector* sm, struct string *st) {
	if (st->size > 50) {return -1;}
	sm->size++;
	sm->str = realloc(sm->str, sizeof(char*)*sm->size);
	sm->str[sm->size-1] = calloc(50, 1);
	for (int i=0; i<st->size; i++) {
		sm->str[sm->size-1][i] = st->str[i];
	}
	return 0;
}

int vector_pop(struct vector* sm) {
	if (sm->size == 0) {return -1;}
	sm->size--;
	sm->str = realloc(sm->str, sizeof(char*)*sm->size);
	return 0;
}

int vector_popat(struct vector* sm, int index) {
	if (sm->size == 0) {return -1;}
	if (index >= sm->size || index < 0) {return -1;}
	for (int i=index+1;i<sm->size;i++) {
		sm->str[i-1] = sm->str[i];
	}
	sm->size--;
	sm->str = realloc(sm->str, sizeof(char*)*sm->size);
	return 0;
}

void vector_free(struct vector* sm) {free(sm->str);}

void ivector_init(struct ivector* sm) {
	sm->num = malloc(sizeof(int));
	sm->size=0;
}

int ivector_add(struct ivector* sm, int num) {
	sm->num = realloc(sm->num, sizeof(int)*sm->size+1);
	sm->num[sm->size] = num;
	sm->size++;
	return 0;
}

int ivector_pop(struct ivector* sm) {
	if (sm->size == 0) {return -1;}
	sm->size--;
	sm->num = realloc(sm->num, sizeof(int)*sm->size);
	return 0;
}

int ivector_popat(struct ivector* sm, int index) {
	if (sm->size == 0) {return -1;}
	if (index >= sm->size || index < 0) {return -1;}
	for (int i=index+1;i<sm->size;i++) {
		sm->num[i-1] = sm->num[i];
	}
	sm->size--;
	sm->num = realloc(sm->num, sizeof(int)*sm->size);
	return 0;
}

void ivector_free(struct ivector* sm) {free(sm->num);}

void string_init(struct string* st) {
	st->str = calloc(1,1);
	st->size=0;
}

int string_add(struct string* st, char* str) {
	st->size += strlen(str);
	st->str = realloc(st->str, st->size+1);
	strcat(st->str, str);
	return 0;
}

int string_addch(struct string* st, char ch) {
	st->size++;
	st->str = realloc(st->str, st->size+1);
	st->str[st->size-1] = ch;
	return 0;
}

int string_addchat(struct string* st, char ch, int index) {
	st->size++;
	st->str = realloc(st->str, st->size+1);
	for (int i=index; i<st->size; i++) {
		char aux = st->str[i];
		st->str[i] = st->str[st->size-1];
		st->str[st->size-1] = aux;
	}
	st->str[index] = ch;
	return 0;
}

int string_pop(struct string* st) {
	if (st->size == 0) {return -1;}
	st->size--;
	st->str = realloc(st->str, st->size);
	return 0;
}

int string_popat(struct string* st, int index) {
	if (st->size == 0) {return -1;}
	if (index >= st->size || index < 0) {return -1;}
	for (int i=index+1;i<st->size;i++) {
		st->str[i-1] = st->str[i];
	}
	st->size--;
	st->str = realloc(st->str, st->size);
	return 0;
}

struct vector string_split(char *str, char sep) {
	struct vector vec;
	vector_init(&vec);
	struct string S;
	string_init(&S);
	for (int i=0; i<strlen(str); i++) {
		if (str[i] != sep) {
			string_addch(&S, str[i]);
		} else {
			vector_addstr(&vec, &S);
			string_free(&S);string_init(&S);
		}
	}
	vector_addstr(&vec, &S);
	string_free(&S);
	return vec;
}

void string_free(struct string* st) {free(st->str);st->size=0;}
