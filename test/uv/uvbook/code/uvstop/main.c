#include <stdio.h>
#include <uv.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/wait.h>

int64_t counter = 0;

void idle_cb(uv_idle_t *handle) {
    printf("Idle callback\n");
    counter++;

    if (counter >= 5) {
        //uv_stop(uv_default_loop());
        printf("uv_stop() called\n");
    }
}

void prep_cb0(uv_prepare_t *handle) {
    printf("Prep callback  0\n");
}
void prep_cb1(uv_prepare_t *handle) {
    printf("Prep callback  1\n");
}
void prep_cb2(uv_prepare_t *handle) {
    printf("Prep callback 2\n");
	sleep(1);
}
void prep_cb3(uv_prepare_t *handle) {
    printf("Prep callback 3\n");
}
void prep_cb4(uv_prepare_t *handle) {
    printf("Prep callback 4\n");
}
void prep_cb5(uv_prepare_t *handle) {
    printf("Prep callback 5\n");
}



int main() {
    uv_idle_t idler;
    uv_prepare_t prep0;
    uv_prepare_t prep1;
    uv_prepare_t prep2;
    uv_prepare_t prep3;
    uv_prepare_t prep4;
    uv_prepare_t prep5;

    uv_idle_init(uv_default_loop(), &idler);
    uv_idle_start(&idler, idle_cb);

    uv_prepare_init(uv_default_loop(), &prep0);
    uv_prepare_start(&prep0, prep_cb0);

    uv_prepare_init(uv_default_loop(), &prep1);
    uv_prepare_start(&prep1, prep_cb1);

    uv_prepare_init(uv_default_loop(), &prep2);
    uv_prepare_start(&prep2, prep_cb2);

    uv_prepare_init(uv_default_loop(), &prep3);
    uv_prepare_start(&prep3, prep_cb3);

    uv_prepare_init(uv_default_loop(), &prep4);
    uv_prepare_start(&prep4, prep_cb4);

    uv_prepare_init(uv_default_loop(), &prep5);
    uv_prepare_start(&prep5, prep_cb5);


    //uv_run(uv_default_loop(), UV_RUN_DEFAULT);
    uv_run(uv_default_loop(), UV_RUN_NOWAIT);

    return 0;
}
