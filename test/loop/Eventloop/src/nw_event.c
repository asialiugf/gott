#include "nw_event.h"

#include <stdlib.h>

evtobj 
*event_create(int fd, int events, read_handler rhandler, write_handler whandler)
{
	evtobj *ev = (evtobj *) malloc(sizeof(evtobj));

	if (ev == NULL)  return NULL;

	ev->fd 		 = fd;
	ev->events 	 = events;
	ev->rhandler = rhandler;
	ev->whandler = whandler;

	return ev;
}