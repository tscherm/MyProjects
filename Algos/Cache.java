import java.util.Scanner;

public class Cache {
  
  static String toPrint;
  static int returns = 0;
  
  public static void main(String args[]) {
    
    Scanner in = new Scanner(System.in);
    
    int instances = Integer.parseInt(in.nextLine());
    
    while(returns < instances) {
      
      // run program
      runInst(in);
      //update how many times the program has run
      returns++;
      
    }
    
    in.close();
    
  }
  
  private static void runInst(Scanner scan) {
    int numPages = Integer.parseInt(scan.nextLine());
    int numRequests = Integer.parseInt(scan.nextLine());
    
    Scanner scana = new Scanner(scan.nextLine());
    
    // create arrays that represent what is in the cache and when it is used next
    int[] cache = new int[numPages];
    int[] nextUse = new int[numPages];
    // this means they are not in the cache and stored as essentially infinitely far away
    for(int i = 0; i < nextUse.length; i++) {
      nextUse[i] = Integer.MAX_VALUE;
    }
    
    int[] cacheSequence = new int[numRequests];
    
    int pageFaults = 0;
    
    // run through each new page and add it to sequence
    for(int i = 0; i < numRequests; i++) {
      cacheSequence[i] = scana.nextInt();
    }
      
    // iterate over cache
    for(int p = 0; p < numRequests; p++) {
      
      //preemptively add page fault, but take away if there is not one.
      pageFaults++;
      
      // find where to put new page or if it is already there.
      int newPageIndex = 0;
      for(int u = 0; u < nextUse.length; u++) {
        if(nextUse[u] > nextUse[newPageIndex]) {
          newPageIndex = u;
        }
        else if(nextUse[u] == 0) {
          newPageIndex = u;
          pageFaults--;
          break;
        }
      }
      
      // put page where it should be
      replace(newPageIndex, cacheSequence[p], p, cache, cacheSequence, nextUse);
      
      // increment down when pages will be used next
      for(int i = 0; i <  nextUse.length; i++) {
        nextUse[i]--;
      }
      
    }
    
    System.out.println(pageFaults);
    
  }
  
  // replace in cache and nextUse
  private static void replace(int dest, int val, int currSpot, int[] cache, int[] cacheSequence, int[] nextUse) {
    
    cache[dest] = val;
    
    for(int i = currSpot + 1; i < cacheSequence.length; i++) {
      if(cacheSequence[i] == val) {
        nextUse[dest] = i - currSpot;
        return;
      }
    }
    // it is never used again
    nextUse[dest] = Integer.MAX_VALUE;
    
  }

}
