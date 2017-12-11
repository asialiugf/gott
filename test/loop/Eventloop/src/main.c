#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <errno.h>
#include <string.h>
#include "nw_eventloop.h"
#include <stdio.h>

int myhandler(int fd, void *data) {
	char buf[128];
	int size;

	if ((size = read(fd, buf, sizeof(buf))) < 0) {
		printf("fail to read.error[%s]\n", strerror(errno));
		return (0);
	}

	printf("data[%s]\n", buf);
	return (0);
}

int
main() {
	printf("123\n");
	evtqueue *eq = eventloop_init(10);

	if (eq == NULL) {
		printf("init fail.\n");
		return (0);
	}

	printf("34\n");
	int sock = server_init(NULL, 50001);

	if (sock <= 0) return 0;

	evtobj *ev = (evtobj *)malloc(sizeof(evtobj));
	ev->fd = sock;
	ev->rhandler = server_rhandle;
	ev->whandler = NULL;

	ev->events = 0;
	set_read_mask(ev->events);

	eventloop_add(ev);
	printf("123\n");
	eventloop_run(5);

	printf("test done\n");

	return 0;
}
