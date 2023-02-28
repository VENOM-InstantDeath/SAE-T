#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>
#include <sys/mount.h>

/*/etc/mtab to get mountpoints of mounted partitions*/

int checkforfile(char* fname) {
	char *base="/dev/";char *ss = malloc(11);
	sprintf(ss, "/dev/%s", fname);
	if (mount(ss, "/mnt", "vfat", 0, NULL) != 0) {return 1;}
	if (access("/mnt/WIFI", F_OK)) {umount("/mnt"); return 2;}
	return 0;
}

void readcont(char* ssid, char* pass) {
	FILE* f = fopen("/mnt/WIFI", "r");
	int c = 0;
	char ch;
	while ((ch = fgetc(f)) != '\n') {
		ssid[c] = ch; c++;
	}
	c = 0;
	while ((ch = fgetc(f)) != '\n') {
		pass[c] = ch; c++;
	}
	fclose(f);
}

int main() {
	DIR *d = opendir("/dev/");
	struct dirent *dir;
	while ((dir = readdir(d)) != NULL) {	
		char* fname = dir->d_name;
		int result;
		if (!strncmp(fname, "sd", 2) && strncmp(fname, "sda", 3) && strlen(fname) == 4) {
			printf("Checking for /dev/%s... ", fname);
			result = checkforfile(fname);
			switch(result) {
				case 0:
					puts("Success");break;
				case 1:
					puts("Mount error");continue;
				case 2:
					puts("File not found error");continue;
			}
			printf("Reading file content...\n");
			char* ssid = calloc(33,1);
			char* pass = calloc(33,1);
			readcont(ssid, pass);
		}
	}
	closedir(d);
	umount("/mnt");
	return 0;
}
