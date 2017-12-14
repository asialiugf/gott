#include <stdio.h>
#include <uv.h>

int64_t counter = 0;

void wait_for_a_while(uv_idle_t* handle) {
    counter++;
	sleep(2);
	printf(" : %dnnnnn\n",counter);
    if (counter >= 10) {
	    printf(" I will exit!\n");
        uv_idle_stop(handle); // 这里有handle是怎么传入的？
	}
}

int ii=0;
void test() {
    ii++;
	sleep(1);
	printf("kkkk ii:%d\n",ii);
	printf("test!\n");
}

int main() {
    uv_idle_t idler;
    uv_idle_t idler1;

    uv_idle_init(uv_default_loop(), &idler);
    uv_idle_start(&idler, wait_for_a_while);
    uv_idle_init(uv_default_loop(), &idler1);
    uv_idle_start(&idler1, test);

    printf("Idling...\n");
    uv_run(uv_default_loop(), 0);

    uv_loop_close(uv_default_loop());
    return 0;
}
