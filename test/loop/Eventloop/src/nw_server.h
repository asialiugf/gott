#ifndef NW_SERVER
#define NW_SERVER 

int server_init(char* ip, int port);

int server_rhandle(int fd, void *data);

//int server_whandle(int fd, void *data);

int client_rhandle(int fd, void *data);

int client_whandle(int fd, void *data);

#endif
