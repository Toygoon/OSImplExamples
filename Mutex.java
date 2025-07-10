import java.util.concurrent.locks.ReentrantLock;

public class Mutex {
    public static int total = 10;
    public static final int LOOPS = 100000;

    public static final ReentrantLock lock = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Start : " + total);

        Thread producer = new Thread(new Producer());
        Thread consumer = new Thread(new Consumer());

        producer.start();
        consumer.start();

        producer.join();
        consumer.join();

        System.out.println("End : " + total);
    }

    public static void acquire() {
        while (lock.isLocked())
            ;
        lock.lock();
    }

    public static void release() {
        lock.unlock();
    }

    public static class Producer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                acquire();
                total++;
                release();
            }
        }
    }

    public static class Consumer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                acquire();
                total--;
                release();
            }
        }
    }
}