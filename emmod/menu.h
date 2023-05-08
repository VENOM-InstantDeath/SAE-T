#ifndef MENU_H
#define MENU_H
#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>

struct optst {
	const char** opt;
	int (**func)(WINDOW*, int*, void*);
	int size;
};

struct bindst {
	int *key;
	void (**func)(WINDOW*,int*,struct optst,int*,void*);
	int size;
};

int bindcheck(struct bindst bindings, int ch);
int bindsearch(struct bindst bindings, int ch);

void defwrite(WINDOW* win, int* wcaps, struct optst opts, int mode, int* mdata, void* data, int* colors);

int menu(WINDOW* win, int* wcaps, struct optst opts, void (*wrwrap)(WINDOW*,int*,struct optst,int,int*,void*,int*), int emptyopts, struct bindst bindings, int allowesc, int* colors, void* data);

#endif
