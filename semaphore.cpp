#include <iostream>
#include <thread>
#include <atomic>
using namespace std;

void producer();
void consumer();

void wait();
void signal();

int total = 10;
constexpr int count = 100000;

atomic<int> S(1);

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
    for (int i = 0; i < count; i++) {
        wait();
        total++;
        signal();
    }
}

void consumer() {
    for (int i = 0; i < count; i++) {
        wait();
        total--;
        signal();
    }
}

void wait() {
    while (true) {
        int s = S.load();
        if (s > 0 && S.compare_exchange_strong(s, s - 1))
            break;
    }
}

void signal() {
    S.fetch_add(1);
}