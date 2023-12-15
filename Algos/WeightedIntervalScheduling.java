import java.util.Arrays;
import java.util.Scanner;

public class WeightedIntervalScheduling {
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
    
    int numJobs = Integer.parseInt(scan.nextLine());
    Job[] jobs = new Job[numJobs];
    
    //O(n)
    for (int i = 0; i < numJobs; i++) {
      String[] vals = scan.nextLine().trim().split(" ", 3);
      jobs[i] = new Job(Integer.parseInt(vals[0]), Integer.parseInt(vals[1]),
          Integer.parseInt(vals[2]));
    }
    
    //O(nlog(n))
    Arrays.parallelSort(jobs);
    
    int[] times = new int[numJobs];
    
    // fill each spot with max time for jobs ending at that end time
    times[0] = jobs[0].weight;
    
    for(int i = 1; i < numJobs; i++) {
      int earlierScheduleVal = 0;
      for(int j = i -1; j >= 0; j--) {
        if(jobs[i].start >= jobs[j].end) {
          earlierScheduleVal = times[j];
          break;
        }
      }
      times[i] = earlierScheduleVal + jobs[i].weight; // best with jobs[i]
      if(times[i] < times[i-1]) { // max of best w/ jobs[i] and w/o jobs[i]
        times[i] = times[i-1];
      }
    }
    
    System.out.println(times[numJobs-1]);
    
  }
}

class Job implements Comparable<Job>{
  
  final int start;
  final int end;
  final int weight;
  
  
  public Job(int s, int e, int w) {
    start = s;
    end = e;
    weight = w;
  }


  @Override
  public int compareTo(Job j) {
    // TODO Auto-generated method stub
    return this.end - j.end;
  }
}
