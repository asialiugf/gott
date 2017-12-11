#ifndef NW_EVENTLOOP
#define NW_EVENTLOOP

#include "nw_util.h"
#include "nw_list.h"
#include "nw_server.h"
#include "nw_event.h"
#include "nw_epoll.h"

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>


evtqueue *evtlp = &evtqueue_obj;

#define eventloop_init(maxsize)	evtlp->evt_init(evtlp,maxsize)
#define eventloop_add(ev)  		evtlp->evt_add(evtlp, ev)
#define eventloop_remove(ev)	evtlp->evt_remove(evtlp, ev)
#define eventloop_run(timeout)	evtlp->evt_run(evtlp, timeout)
#define eventloop_destroy()		evtlp->evt_destroy(evtlp)

#endif
