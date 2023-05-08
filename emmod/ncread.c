#include <stdio.h>
#include <ncurses.h>
#include <stdlib.h>
#include "ncread.h"
#include "vector.h"

struct string vslice(struct string v,int a, int b) {
	struct string s;
	string_init(&s);
        for (int i=a;i<b;i++){
		if (i >= v.size) break;
                string_addch(&s, v.str[i]);
        }
        return s;
}

char* listostr(struct string l) {
	char* s;
	if (!l.size) s=calloc(1,1);
	else s = malloc(l.size);
	for (int i=0;i<l.size;i++) {
		s[i] = l.str[i];
	}
	s[l.size] = 0;
	return s;
}

void clrbox(WINDOW* win, int y, int x, int minlim, int vislim, int color) {
	wattron(win, COLOR_PAIR(color));
	for (int i=x;i<x+(vislim-minlim)+1;i++) {
		mvwaddch(win,y,i,32);
	}
	wattroff(win, COLOR_PAIR(color));
}

int ampsread(WINDOW* win, char** ptr, int y, int x, int vislim, int chlim, int mode, int color) {
	struct string String;
	struct string vsliced;
	string_init(&String); string_init(&vsliced);
	int p = 0;
	int sp = 0;
	int minlim = 0;
	noecho();
	clrbox(win,y,x,minlim,vislim, color);
	wrefresh(win);

	while (1) {
		int ch = mvwgetch(win,y,x+p);
		if (ch == 127) ch = KEY_BACKSPACE;
		else if (ch == 8) ch = KEY_BACKSPACE;
		if (ch == 4) {}
		if (ch == 27) {ptr = NULL;return 1;}
		if (ch == '\n') {*ptr = listostr(String);return 0;}
		if (ch == KEY_BACKSPACE) {
			if (!sp) continue;
			string_popat(&String, sp-1);
			clrbox(win,y,x,minlim,vislim, color);
			if (!p && sp) {vislim--;minlim--;}
			int acum1 = 0;
			vsliced = vslice(String,minlim,vislim+1);
			for (int i=0;i<vsliced.size;i++) {
				if (mode) mvwaddch(win,y,x+acum1,'*');
				else mvwaddch(win,y,x+acum1,vsliced.str[i]);
				acum1++;
			}
			wrefresh(win);
			if (!(!p && sp)) p--;
			sp--;
		}
		if (ch == KEY_RIGHT) {
			if (sp == String.size) continue;
			if (sp == vislim) {
				vislim++;minlim++;
				clrbox(win,y,x,minlim,vislim, color);
				int acum1=0;
				vsliced = vslice(String,minlim,vislim+1);
				for (int i=0;i<vsliced.size;i++) {
					if (mode) mvwaddch(win,y,x+acum1,'*');
					else mvwaddch(win,y,x+acum1,vsliced.str[i]);
					acum1++;
				}
				wrefresh(win);
				sp++;continue;
			}
			p++;
			sp++;
		}
		if (ch == KEY_LEFT) {
			if (!sp) continue;
			if (!p && sp) {
				vislim--;minlim--;
				clrbox(win,y,x,minlim,vislim, color);
				int acum1 = 0;
				vsliced = vslice(String,minlim,vislim+1);
				for (int i=0;i<vsliced.size;i++) {
					if (mode) mvwaddch(win,y,x+acum1,'*');
					else mvwaddch(win,y,x+acum1,vsliced.str[i]);
					acum1++;
				}
				wrefresh(win);
				sp--;continue;
			}
			p--;
			sp--;
		}
		if (String.size == chlim) continue;
		if (ch < 32 || ch > 250) continue;
		string_addchat(&String, ch, sp);
		clrbox(win,y,x,minlim,vislim, color);
		if (sp == vislim) {
			vislim++;minlim++;
			int acum1=0;
			vsliced = vslice(String,minlim,vislim+1);
			for (int i=0;i<vsliced.size;i++) {
				if (mode) mvwaddch(win,y,x+acum1,'*');
				else mvwaddch(win,y,x+acum1,vsliced.str[i]);
				acum1++;
			}
			wrefresh(win);
			sp++;continue;
		}
		int acum1=0;
		vsliced = vslice(String,minlim,vislim+1);
		for (int i=0;i<vsliced.size;i++) {
			if (mode) mvwaddch(win,y,x+acum1,'*');
			else mvwaddch(win,y,x+acum1,vsliced.str[i]);
			acum1++;
		}
		wrefresh(win);
		sp++;
		p++;
	}
}
