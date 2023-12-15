import java.util.Arrays;
import java.util.Scanner;

public class CrossCounter {
  static String toPrint;
  static int returns = 0;

  public static void main(String args[]) {

    Scanner in = new Scanner(System.in);

    int instances = Integer.parseInt(in.nextLine());

    while (returns < instances) {

      // run program
      
      runInst(in);
      // update how many times the program has run
      returns++;

    }

    in.close();

  }

  private static void runInst(Scanner scan) {
    int numItems = Integer.parseInt(scan.nextLine());
    int[] topHalf = new int[numItems];
    int[] bottomHalf = new int[numItems];
    Pair[] pairs = new Pair[numItems];

    for (int i = 0; i < numItems; i++) {
      topHalf[i] = Integer.parseInt(scan.nextLine());
    }
    for (int i = 0; i < numItems; i++) {
      bottomHalf[i] = Integer.parseInt(scan.nextLine());
    }
    // sort top half and inversion counter second half
    for (int i = 0; i < numItems; i++) {
      pairs[i] = new Pair(topHalf[i], bottomHalf[i]);
    }

    Arrays.parallelSort(pairs, (p1, p2) -> p1.getFirst() - p2.getFirst());
    
    int[] toCount = new int[numItems];
    for (int i = 0; i < numItems; i++) {
      toCount[i] = pairs[i].getSecond();
    }

    // inversion counter
    System.out.println(adjustedMergeSort(toCount, 0, toCount.length));

  }

  private static long adjustedMergeSort(int[] toCount, int firstIndex, int secondIndex) {
    long count = 0;

    if (secondIndex - firstIndex <= 1) {
      return count;
    }

    // get inversions in each half and it mutates the array O(logn) calls
    long first = adjustedMergeSort(toCount, firstIndex, (secondIndex + firstIndex) / 2);
    long second = adjustedMergeSort(toCount, (secondIndex + firstIndex) / 2, secondIndex);

    // sort array
    int[] temp = new int[secondIndex - firstIndex];

    int firstInd = firstIndex;
    int secondInd = (secondIndex + firstIndex) / 2;

    // O(n)
    for (int i = firstIndex; i < secondIndex; i++) {
      // check and make sure indices are in the right range
      if (secondInd >= secondIndex || (firstInd < (secondIndex + firstIndex) / 2
          && toCount[firstInd] <= toCount[secondInd])) {
        temp[i - firstIndex] = toCount[firstInd];
        firstInd++;
      } // second is smaller so increment count
      else {
        temp[i - firstIndex] = toCount[secondInd];
        secondInd++;
        count += ((secondIndex + firstIndex) / 2) - firstInd;
      }
    }

    // O(n)
    for (int i = firstIndex; i < secondIndex; i++) {
      toCount[i] = temp[i - firstIndex];
    }

    return count + first + second;
  }



}


class Pair {
  private int first;
  private int second;

  public Pair(int first, int second) {
    this.first = first;
    this.second = second;
  }
  
  public int getFirst() {return first;}
  public int getSecond() {return second;}

}
