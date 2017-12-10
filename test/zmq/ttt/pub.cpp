#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
#include <assert.h>  
#include <string.h>  
#include <zmq.h>  
  
  
int main()  
{  
    printf("Hello world!\n");  
  
    void* context = zmq_ctx_new();///创建一个新的环境  
    assert(context != NULL);  
  
    int ret = zmq_ctx_set(context, ZMQ_MAX_SOCKETS, 1);/// 在该环境中最大只允许一个socket存在  
    assert(ret == 0);  
  
    void* publisher = zmq_socket(context, ZMQ_PUB);/// 创建一个发布者  
    assert(publisher != NULL);  
  
    ret = zmq_bind(publisher, "tcp://127.0.0.1:8888");/// 绑定该发布到TCP通信  
    assert(ret == 0);  
  
    while(1)  
    {  
        ret = zmq_send(publisher, "Hi,I'm server", 16, 0);/// 发送消息  
        //assert(ret == 7);  
        printf("%d\n", ret);  
        sleep(1);  
    }  
  
    printf("1\n");  
  
    return 0;  
}  
