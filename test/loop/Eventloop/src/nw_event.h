#ifndef NW_EVTLOOP
#define NW_EVTLOOP

#include "nw_list.h"

#define EVT_READ 	0x001
#define EVT_WRITE 	0x010

#define reset_rw_mask(events) 	events = 0x00
#define set_read_mask(events) 	events |=0x001
#define set_write_mask(events) 	events |=0x010

typedef int (*write_handler)(int fd, void *data);
typedef int (*read_handler)(int fd, void *data);

typedef struct evtobj {
	int fd;
	int events;	
	read_handler  rhandler;
	write_handler whandler;
} evtobj;

typedef struct _evtqueue {
	int fd;
	int maxsize;
	int freesize;
	listhead evtlist;
	struct _evtqueue * (*evt_init)(struct _evtqueue *,int);
	int (*evt_add)(struct _evtqueue *, evtobj *);
	int (*evt_remove)(struct _evtqueue *, evtobj *);
	int (*evt_run)(struct _evtqueue*, int );
	void (*evt_destroy)(struct _evtqueue* );
} evtqueue;

evtobj *event_create(int fd, int events, read_handler rhandler, write_handler whandler);

#endif// end of NW_EVTLOOP
