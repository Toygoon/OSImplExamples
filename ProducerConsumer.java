public class ProducerConsumer {
    public static int total = 10;
    public static final int LOOPS = 100000;

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

    public static class Producer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                total++;
            }
        }
    }

    public static class Consumer implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < LOOPS; i++) {
                total--;
            }
        }
    }
}