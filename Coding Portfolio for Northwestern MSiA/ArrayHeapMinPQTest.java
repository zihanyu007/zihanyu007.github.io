package bearmaps;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import edu.princeton.cs.algs4.Stopwatch;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ArrayHeapMinPQTest {
    private static Random r = new Random(500);

    private static void generateRandomNodes(ExtrinsicMinPQ t, int n) {
        for (int i =  0; i < n; i += 1) {
            t.add(r.nextInt(), r.nextDouble());
        }
    }







    public static void main(String[] args) {
        Stopwatch sw = new Stopwatch();
        ArrayHeapMinPQ example = new ArrayHeapMinPQ();


        example.add(2, 1.5);
        example.add(3, 7.0);
        example.add(6, 67.0);
        example.add(5, 34.6);
        example.add(4, 34.7);
        example.changePriority(2,8.0);

        generateRandomNodes(example, 100000);

        for (int i = 1; i < 50000; i++) {
            example.removeSmallest();
        }



        example.removeSmallest();
        int smallest = (int) example.removeSmallest();
        int size = example.size();
        System.out.println(size);
        System.out.println(smallest);
        System.out.println("Total time elapsed: " + sw.elapsedTime() +  " seconds.");


        Stopwatch sw2 = new Stopwatch();
        NaiveMinPQ example2 = new NaiveMinPQ();

       generateRandomNodes(example2, 100000);

        for (int i = 1; i < 50000; i++) {
            example2.removeSmallest();
        }
        int smallest2 = (int) example2.removeSmallest();
        int size2 = example2.size();
        System.out.println(size2);
        System.out.println(smallest2);

        System.out.println("Total time elapsed: " + sw2.elapsedTime() +  " seconds.");
    }
}
