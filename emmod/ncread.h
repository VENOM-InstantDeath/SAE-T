#ifndef NCREAD_H
#define NCREAD_H
#include <stdio.h>
#include <ncurses.h>
#include <stdlib.h>
#include "vector.h"

struct string vslice(struct string v,int a, int b);
char* listostr(struct string l);
void clrbox(WINDOW* win, int y, int x, int minlim, int vislim, int color);
int ampsread(WINDOW* win, char** ptr, int y, int x, int vislim, int chlim, int mode, int color);
#endif
