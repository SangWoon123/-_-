//compile: gcc -o <File name> <code.c>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main() {
    
while (1) {
	FILE* fp;
        char buff[256];
	fp = popen("curl -s --unix-socket /var/run/docker.sock http://v1.41/containers/json", "r");
	
	while(fgets(buff, 256, fp) != NULL){
		FILE* s=fopen("con_info.text","a");
        	printf("%s", buff);
        	fputs(buff,s);
        	fclose(s);
        }
	sleep(3);
    	pclose(fp);
    }
    return 0;
}
