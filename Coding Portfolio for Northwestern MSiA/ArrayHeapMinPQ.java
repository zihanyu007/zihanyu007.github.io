package bearmaps;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.NoSuchElementException;

public class ArrayHeapMinPQ<T> implements ExtrinsicMinPQ<T> {
    private ArrayList<Node> keysMinHeap;
    private int size;
    private HashMap<T, MyStuff> hm;


    public ArrayHeapMinPQ() {
        keysMinHeap = new ArrayList<>();
        hm = new HashMap<>();
        size = 0;
    }


    private class Node<T> {
        private T item;
        private double priority;

        Node(T e, double p) {
            item = e;
            priority = p;
        }

        void setPriority(double priority) {
            this.priority = priority;
        }
    }

    private class MyStuff {
        double priority;
        int index;
        private MyStuff(int i, double p) {
            this.priority = p;
            this.index = i;
        }
    }





    @Override
    public void add(T item, double p) {
        if (contains(item)) {
            throw new IllegalArgumentException();
        }
        Node n = new Node(item, p);
        keysMinHeap.add(n);
        swim(size);
        hm.put(item, new MyStuff(keysMinHeap.indexOf(n), p));
        size = size + 1;
    }

    private void swim(int k) {
        if (k > 0 && keysMinHeap.get(parent(k)).priority > keysMinHeap.get(k).priority) {
            swap(k, parent(k));
            swim(parent(k));
        }
    }

    private void swap(int j, int k) {
        hm.replace((T) keysMinHeap.get(k).item, new MyStuff(j, keysMinHeap.get(k).priority));
        hm.replace((T) keysMinHeap.get(j).item, new MyStuff(k, keysMinHeap.get(j).priority));
        Node swap = keysMinHeap.get(j);
        keysMinHeap.set(j, keysMinHeap.get(k));
        keysMinHeap.set(k, swap);
    }


    private int parent(int k) {
        if (k == 0) {
            return 0;
        }
        return (k - 1) / 2;
    }



    private void sink(int m) {
        while (m * 2 + 1 <= size - 1) {
            int l = m * 2 + 1;
            if (l < size - 1 && keysMinHeap.get(l).priority > keysMinHeap.get(l + 1).priority) {
                l = l + 1;
            }
            if (!(keysMinHeap.get(m).priority > keysMinHeap.get(l).priority)) {
                break;
            }
            swap(m, l);
            m = l;
        }
    }

    @Override
    public boolean contains(T item) {
        return hm.containsKey(item);
    }




    @Override
    public T getSmallest() {
        if (keysMinHeap.isEmpty() || size == 0) {
            throw new NoSuchElementException();
        }
        return (T) keysMinHeap.get(0).item;
    }

    @Override
    public T removeSmallest() {
        if (keysMinHeap.isEmpty() || size == 0) {
            throw new NoSuchElementException();
        }
        T min = (T) keysMinHeap.get(0).item;
        hm.remove(keysMinHeap.get(0).item);
        keysMinHeap.set(0, keysMinHeap.get(size - 1));
        MyStuff newStuff = new MyStuff(0, keysMinHeap.get(0).priority);
        hm.replace((T) keysMinHeap.get(0).item, newStuff);
        sink(0);
        keysMinHeap.set(size - 1, null);
        size = size - 1;
        return min;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public void changePriority(T item, double priority) {
        if (!contains(item)) {
            throw new NoSuchElementException();
        }
        int index = hm.get(item).index;
        keysMinHeap.get(index).priority = priority;
        sink(index);
        swim(index);
        hm.replace(item, new MyStuff(keysMinHeap.indexOf(item), priority));
    }
}
