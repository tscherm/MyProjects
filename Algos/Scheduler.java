import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;

public class Scheduler {
  
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
    
    int numJobs = Integer.parseInt(scan.nextLine());
    
    Job[] jobs = new Job[numJobs];
    
    // iterate through new jobs and put them in an array O(n)
    for(int i = 0; i < numJobs; i++) {
      Scanner newJobScan = new Scanner(scan.nextLine());
      
      Job newJob = new Job(newJobScan.nextInt(), newJobScan.nextInt());
      jobs[i] = newJob;
      
      newJobScan.close();
    }
    
    //sort jobs by end time with Arrays.sort. This uses timsort O(n*log(n)) 
    // (which I have implement and have done so 
    // in other classes so it is not a total cop-out)
    Arrays.sort(jobs, (j1, j2) -> j1.end - j2.end);
    
    // add first job on schedule to latest job and num jobs
    Job lastJob = jobs[0];
    int totalJobs = 1;
    
    // iterate through jobs and make schedule O(n)
    for(int i = 1; i < jobs.length; i++) {
      if(jobs[i].start >= lastJob.end) {
        lastJob = jobs[i];
        totalJobs++;
      }
    }
    
    System.out.println(totalJobs);
    
  }
  
  
}

/*
 * Job class that stores start and end times of jobs
 */
class Job implements Comparator<Job>{
  
  public int start;
  public int end;
  
  public Job(int start, int end) {
    this.start = start;
    this.end = end;
  }

  @Override
  public int compare(Job j1, Job j2) {
    return j1.end - j2.end;
  }
}
