#include <iostream>
#include <thread>
using namespace std;

void producer();
void consumer();

int total = 10;
constexpr int LOOPS = 100000;

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
        total++;
    }
}

void consumer() {
    for (int i = 0; i < LOOPS; i++) {
        total--;
    }
}
