#include "nw_server.h"
#include "nw_eventloop.h"

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>

int 
server_init(char* ip, int port) 
{
	int sock = socket(AF_INET, SOCK_STREAM, 0);

	if(sock <= 0) {
		printf("failt to init server sock,err[%s]\n", strerror(errno));
		return -1;
	}

	 struct sockaddr_in addr;
	 addr.sin_family = AF_INET;
	 addr.sin_port = htonl(port);

	 addr.sin_addr.s_addr = ip == NULL ? INADDR_ANY : inet_addr(ip);

	 if (bind(sock, (struct sockaddr *)&addr, sizeof(struct sockaddr)) != 0) {
	 	printf("bind fail.err[%s]\n", strerror(errno));
	 	return -1;
	 }

	if (listen(sock, 5) != 0) {
		printf("listen fail.err[%s]\n", strerror(errno));
		return -1;
	}

	setnonblock(sock);

	return sock;
}


int 
server_rhandle(int fd, void *data) 
{
	char buf[2014];
	struct sockaddr_in addr;
	socklen_t len;

	int csock = accept(fd, (struct sockaddr *)&addr, &len);

	//printf("client:[%s]",inet_ntoa(inet_addr(addr)));
	
	 evtobj *ev = event_create(csock, EVT_READ, client_rhandle, NULL);

	 if (ev == NULL) {
		return -1;
	 }

	 eventloop_add(ev);
 		 
	return csock;
}


int client_rhandle(int fd, void *data) {
	char buff[1024];		
	int len;
	do{
		len = read(fd, buff, sizeof(buff));
		if (len <= 0) {
			break;
		}
		printf("data:%s\n",buff);
	}while(1);
	return 0;
}


int client_whandle(int fd, void *data) {
	return 0;	
} 
