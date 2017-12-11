#ifndef NW_EPOLL
#define NW_EPOLL

#include "nw_event.h"

extern evtqueue evtqueue_obj;

evtqueue *evt_epoll_init(evtqueue *eq, int maxsize);

int evt_epoll_add(evtqueue *eq, evtobj *ev);

int evt_epoll_remove(evtqueue *eq, evtobj *ev);

int evt_epoll_run(evtqueue* eq, int timeout);

void evt_epoll_destroy(evtqueue* eq);

#endif