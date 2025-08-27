import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;
import java.util.function.BooleanSupplier;

public class Monitor {
    public static int total = 10;
    public static final int LOOPS = 100000, MAX_SIZE = 100;

    public static final ReentrantLock lock = new ReentrantLock();
    public static final Condition condition = lock.newCondition();

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
        lock.lock();
    }

    public static void release() {
        lock.unlock();
    }

    public static void _wait(BooleanSupplier conditionCheck) {
        try {
            while (conditionCheck.getAsBoolean()) {
                condition.await();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public static void _signal() {
        condition.signal();
    }

    public static class Producer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                acquire();
                _wait(() -> (MAX_SIZE <= total));
                total++;
                _signal();
                release();
            }
        }
    }

    public static class Consumer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                acquire();
                _wait(() -> (total <= 0));
                total--;
                _signal();
                release();
            }
        }
    }
}
