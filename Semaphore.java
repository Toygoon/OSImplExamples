import java.util.concurrent.atomic.AtomicInteger;

public class Semaphore {
    public static int total = 10;
    public static final int LOOPS = 100000;

    public static final AtomicInteger S = new AtomicInteger(1);

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

    public static void _wait() {
        while (true) {
            int s = S.get();

            if (s > 0 && S.compareAndSet(s, s - 1))
                break;
        }
    }

    public static void _signal() {
        S.incrementAndGet();
    }

    public static class Producer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                _wait();
                total++;
                _signal();
            }
        }
    }

    public static class Consumer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                _wait();
                total--;
                _signal();
            }
        }
    }
}
