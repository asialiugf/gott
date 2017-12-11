INC=-I.

LIBS=-L. -lnw_evtloop

VPATH=.

SRC=nw_list.c nw_epoll.c nw_server.c nw_util.c nw_event.c

OBJS=$(SRC:.c=.o)

OUTPUT=libnw_evtloop.so libnw_evtloop.a main

all:$(OUTPUT)
		
main:main.o 
	gcc -g $^ -o $@ -L.  -lnw_evtloop 

libnw_evtloop.so:$(OBJS)
	gcc -fPIC -shared -g $^ -o $@

libnw_evtloop.a:$(OBJS)
		ar -rcs $@  $^

.SUFFIXES:.o .c .so .a
.c.o:
	gcc -fPIC $(INC) -g -c $^


test:main
		./main
			
clean:
		rm -f *.o *.a *.so  $(OUTPUT) 
