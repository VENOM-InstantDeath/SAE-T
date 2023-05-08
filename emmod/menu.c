#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>
#include "menu.h"

int bindcheck(struct bindst bindings, int ch) {
	for (int i=0; i<bindings.size; i++) {
		if (bindings.key[i] == ch) return 1;
	}
	return 0;
}

int bindsearch(struct bindst bindings, int ch) {
	for (int i=0; i<bindings.size; i++) {
		if (bindings.key[i] == ch) return i;
	}
	return -1;
}

void defwrite(WINDOW* win, int* wcaps, struct optst opts, int mode, int* mdata, void* data, int* colors) {
	/*Mode 0 - Escribir todas las opciones y dejar p en 0
	 *Mode 1 - Disminuir p por 1
	 *Mode 2 - Aumentar p por 1*/
	const char** keys = opts.opt;
	if (!mode) {
		int tmp = 0;
		for (int i=mdata[2]; i<mdata[3]; i++) {
			if (i == opts.size) break;
			mvwaddstr(win,tmp, 0, keys[i]);
			tmp++;
		}
		wattron(win, COLOR_PAIR(colors[1]));
		mvwaddstr(win, 0, 0, keys[0]);
		wattroff(win, COLOR_PAIR(colors[1]));
		wrefresh(win);
		return;
	}
	mvwaddstr(win, mdata[0], 0, keys[mdata[1]]);
	if (mode == 1) {
		if (!mdata[0]) { /*if p == minlim*/
			wscrl(win, -1);
			mdata[1]--;mdata[2]--;mdata[3]--;
		} else {
			mdata[1]--;mdata[0]--;
		}
	} else {
		if (mdata[1] == mdata[3]-1) {
			wscrl(win, 1);
			mdata[1]++;mdata[2]++;mdata[3]++;
		} else {
			mdata[0]++;mdata[1]++;
		}
	}
	wattron(win, COLOR_PAIR(colors[1]));
	mvwaddstr(win, mdata[0], 0, keys[mdata[1]]);
	wattroff(win, COLOR_PAIR(colors[1]));
	wrefresh(win);
}

int menu(WINDOW* win, int* wcaps, struct optst opts, void (*wrwrap)(WINDOW*,int*,struct optst,int,int*,void*,int*), int emptyopts, struct bindst bindings, int allowesc, int* colors, void* data) {
	curs_set(0);
	WINDOW* mwin = derwin(win, wcaps[0], wcaps[1], wcaps[2], wcaps[3]);
	keypad(mwin, 1);
	wbkgd(mwin, COLOR_PAIR(colors[0]));
	noecho();
	scrollok(mwin, 1);
	int mdata[] = {0, 0, 0, wcaps[0]}; /*Menu data: p,sp,minlim,vislim*/
	const char **keys = opts.opt;
	if (!emptyopts && !opts.size) {
		endwin();
		printf("libmenu error: No se han especificado opciones.\n");
		return 1;
	}
	wrwrap(mwin,wcaps,opts,0,mdata,data,colors);
	/*Interact part*/
	while (1) {
		int ch = wgetch(mwin);
		if (ch == 27) { /*ESC*/
			if (!allowesc) continue;
			return 0;
		}
		if (ch == 259) { /*UP*/
			if (!mdata[1]) continue;
			wrwrap(mwin,wcaps,opts,1,mdata,data,colors);
		}
		if (ch == 258) { /*DOWN*/
			if (mdata[1] == opts.size-1) continue;
			wrwrap(mwin,wcaps,opts,2,mdata,data,colors);
		}
		if (ch == 10) { /*ENTER*/
			return opts.func[mdata[1]](mwin, mdata, data);
		}
		if (!bindcheck(bindings, ch)) continue;
		bindings.func[bindsearch(bindings, ch)](mwin, wcaps, opts, mdata, data);
	}
}
