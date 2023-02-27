#include <stdio.h>
#include <stdlib.h>
#include <sys/mount.h>

int main() {
	if (mount("/dev/sdb1", "/mnt/sd", "vfat", 0, NULL) != 0) {perror("Mount");return 1;}
	return 0;
}
