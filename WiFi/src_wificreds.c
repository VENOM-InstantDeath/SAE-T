#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>
#include <net/if.h>
#include <sys/mount.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

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

void writeconf(char* ssid, char* pass) {
	/* <Example config>
	ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
	update_config=1
	network={
	ssid="name"
	psk="plain passw"
	scan_ssid=1
	key_mgmt=WPA-PSK
	}
	   <End Example>*/
	char* confpath = "/etc/wpa_supplicant/wpa_supplicant.conf";
	FILE* f = fopen(confpath, "w");
	fprintf(f, "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\nnetwork={\nssid=\"%s\"\npsk=\"%s\"\nscan_ssid=1\nkey_mgmt=WPA-PSK\n}", ssid, pass);
	fclose(f);
}

void interface_ctrl(char* interface, int mode) {
	struct ifreq ifr;
	strcpy(ifr.ifr_name, interface);
	if (mode) ifr.ifr_flags = IFF_UP;
	else ifr.ifr_flags = IFF_BROADCAST;
	int fd = socket(AF_INET, SOCK_DGRAM, 0);
	ioctl(fd, SIOCSIFFLAGS, &ifr);
	perror("Ioctl");
}

int main() {
	DIR *d = opendir("/dev/");
	struct dirent *dir;
	while ((dir = readdir(d)) != NULL) {	
		char* fname = dir->d_name;
		int result;
		if (!strncmp(fname, "sd", 2) && strlen(fname) == 4) {
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
			writeconf(ssid, pass);
			interface_ctrl("wlan0", 0);
			system("systemctl restart dhcpcd");
		}
	}
	closedir(d);
	umount("/mnt");
	return 0;
}
