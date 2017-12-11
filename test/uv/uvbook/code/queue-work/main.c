#include "uv.h"
#include "stdio.h"

uv_loop_t *loop;
uv_async_t async;


void hare(void *arg)
{
    int tracklen = *((int *) arg);
    while (tracklen) {
        tracklen--;
        sleep(1);
        fprintf(stderr, "Hare ran another step\n");
    }
    fprintf(stderr, "Hare done running!\n");
}

void work_cb1(uv_work_t *req) {
    int size = *((int*) req->data);
    fprintf(stderr, "work_cb1 \n");
}
void work_cb2(uv_work_t *req, int status) {
    fprintf(stderr, "work_cb2   \n");
}



void print_progress(uv_async_t *handle) {
    double percentage = *((double*) handle->data);
    fprintf(stderr, "Downloaded %.2f%%\n", percentage);
}

void after(uv_work_t *req, int status) {
    fprintf(stderr, "Download complete\n");
    uv_close((uv_handle_t*) &async, NULL);
}

void fake_download(uv_work_t *req) {
    int size = *((int*) req->data);
    int downloaded = 0;
    double percentage;
    while (downloaded < size) {
    percentage = downloaded*100.0/size;
    async.data = (void*) &percentage;
    uv_async_send(&async);

    sleep(1);
    downloaded += (200+random())%1000; // can only download max 1000bytes/sec,
    // but at least a 200;
    //fprintf(stderr, "---- downloaded:%d\n", downloaded);
    if(downloaded < 600)
    {
       pid_t pid,pc;
       pid = fork();
        if(pid == -1) {
           printf("fork err\n");
        }else if(pid == 0) {
           fprintf(stderr, "fork child process ...\n");
           uv_work_t req;
			  int size = 10240;
			  req.data = (void*) &size;
			  fprintf(stderr, "fork child process ...1\n");
			  uv_queue_work(loop, &req, work_cb1, work_cb2);//fork的子进程再使用
			  fprintf(stderr, "fork child process ...2\n");
	  }else {
	}
  }


  }
}
int main()
{

loop = uv_default_loop();

uv_work_t req;
int size = 10240;
req.data = (void*) &size;

  uv_async_init(loop, &async, print_progress);
  uv_queue_work(loop, &req, fake_download, after);//主进程先使用一次

  return uv_run(loop, UV_RUN_DEFAULT);

  return 0;
}

