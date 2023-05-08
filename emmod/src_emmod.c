#include <stdio.h>
#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <json.h>
#include "menu.h"
#include "ncread.h"

char* tostring(int num) {
	char *x = malloc(0);
	int size = 0;
	while (num) {
		x = realloc(x, size+1);
		size++;
		int t = num % 10;
		num /= 10;
		x[size-1] = t+48;
	}
	for (int i=0; i<size/2; i++) {
		int temp = x[i];
		x[i] = x[size-i-1];
		x[size-i-1] = temp;
	}
	x = realloc(x, size+1); x[size] = 0;
	return x;
}

int quit(WINDOW* mwin, int* mdata, void* data) {
	endwin();
	exit(0);
}

int add(WINDOW* mwin, int* mdata, void* data) {
	const char* emo[] = {"Anger", "Sadness", "Disgust", "Fear", "Neutral", "Happiness"};
	WINDOW* stdscr = (WINDOW*)data;
	int y, x; getmaxyx(stdscr, y, x);
	WINDOW* win = newwin(5,20, y/2-2, x/2-10);
	int wy,wx; getmaxyx(win, y,x);
	wbkgd(win, COLOR_PAIR(3));
	mvwaddstr(win, 0, x/2-strlen(emo[mdata[1]])/2, emo[mdata[1]]);
	wrefresh(stdscr);
	wrefresh(win);
	char* ptr;
	ampsread(win, &ptr, 2, 1, 17, 50, 0, 2);
	if (ptr == NULL) return 1;
	FILE* conf = fopen("emotion.json", "r");
	fseek(conf, 0, SEEK_END);
	int size = ftell(conf);
	fseek(conf, 0, SEEK_SET);
	char *str = calloc(size, 1);
	int c = 0; int ch;
	while ((ch=fgetc(conf)) != EOF) {
		str[c] = ch;c++;
	}
	fclose(conf);
	json_object *jobj = json_tokener_parse(str);
	char *modstr = NULL;
	size = snprintf(modstr, 0, "{\"%s\": \"%s\"}", emo[mdata[1]], ptr);
	modstr = malloc(size+1);
	snprintf(modstr, size+1, "{\"%s\": \"%s\"}", emo[mdata[1]], ptr);
	json_object *val = json_tokener_parse(modstr);
	json_object_object_get_ex(val, emo[mdata[1]], &val);
	json_object_object_add(jobj, emo[mdata[1]], val);
	const char* fstr = json_object_to_json_string(jobj);
	conf = fopen("emotion.json", "w");
	fwrite(fstr, 1, strlen(fstr), conf);
	fclose(conf);
	delwin(win);
	free(str);free(jobj);free(val);free(ptr);
	touchwin(stdscr);wrefresh(stdscr);
	return 1;
}

int main() {
	WINDOW* stdscr = initscr();
	start_color();
	init_pair(1, 7, 0);
	init_pair(2, 0, 7);
	init_pair(3, 7, 4);
	keypad(stdscr, 1);
	curs_set(0);
	cbreak();
	noecho();
	int y, x; getmaxyx(stdscr,y,x);
	int wcaps[4] = {7,10,y/2,x/2-5};
	int colors[2] = {1 ,2};
	struct optst opts;
	struct bindst bindings; bindings.size = 0;
	const char* opt[] = {"Anger", "Sadness", "Disgust", "Fear", "Neutral", "Happiness"};
	int (*func[6])(WINDOW*, int*, void*) = {add, add, add, add, add, add};
	opts.opt = opt;
	opts.func = func;
	opts.size = 6;
	for (;;) {
		wattron(stdscr, A_BOLD | A_UNDERLINE);
		mvwaddstr(stdscr, y/2-3, x/2-9, "Answers to emotions");
		wattroff(stdscr, A_BOLD | A_UNDERLINE);
		wrefresh(stdscr);
		if (menu(stdscr,wcaps,opts,defwrite,0,bindings,1,colors,stdscr)) {
			move(0,0);clrtobot();
			wrefresh(stdscr);
		} else {
			break;
		}
	}
	endwin();
	return 0;
}
