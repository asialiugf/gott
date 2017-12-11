#include "nw_util.h"

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>

int
setnonblock(int fd) 
{
	int fdflags;

	if ((fdflags = fcntl(fd, F_GETFL, 0)) == -1) {
		printf("get fd[%d] flag error[%s].\n", fd, strerror(errno));
		return -1;
	}

	if (fcntl(fd, F_SETFL, fdflags | O_NONBLOCK) == -1) {
		printf("set fd[%d] flag error[%s].\n", fd, strerror(errno));
		return -1;
	}

	return 0;
}
