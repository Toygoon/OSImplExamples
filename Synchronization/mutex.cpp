#include <iostream>
#include <thread>
#include <atomic>
using namespace std;

void producer();
void consumer();

void acquire();
void release();

int total = 10;
constexpr int LOOPS = 100000;

atomic_flag lock = false;

int main(void) {
    cout << "Start : " << total << endl;

    thread t1(producer);
    thread t2(consumer);

    t1.join();
    t2.join();

    cout << "End : " << total << endl;

    return 0;
}

void producer() {
    for (int i = 0; i < LOOPS; i++) {
        acquire();
        total++;
        release();
    }
}

void consumer() {
    for (int i = 0; i < LOOPS; i++) {
        acquire();
        total--;
        release();
    }
}

void acquire() {
    while (lock.test_and_set(memory_order_acquire));
}

void release() {
    lock.clear(memory_order_release);
}