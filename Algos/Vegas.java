import java.util.Scanner;
import java.util.HashMap;
import java.util.Random;


public class Vegas {

  static String toPrint;
  static int returns = 0;
  static String info2 = "";

  public static void main(String args[]) throws Exception {

    Scanner in = new Scanner(System.in);

    //int instances = Integer.parseInt(in.nextLine());
    int instances = 1;

    while (returns < instances) {

      // run program
      
      runInst(in);
      // update how many times the program has run
      returns++;
      info2 = "";

    }

    in.close();

  }
  
  private static void runInst(Scanner scan) throws Exception {
    int numLits = Integer.parseInt(scan.nextLine().trim());
    int numStas = Integer.parseInt(scan.nextLine().trim());
    int numNeed = (7 * numStas) / 8;
    Random rand = new Random();
    
    Statement[] statements = new Statement[numStas];
    
    for(int i = 0; i < numStas; i++) {
      Scanner tempScan = new Scanner(scan.nextLine());
      
      int v1 = Integer.parseInt(tempScan.next());
      int v2 = Integer.parseInt(tempScan.next());
      int v3 = Integer.parseInt(tempScan.next());
      
      boolean n1 = v1 < 0;
      boolean n2 = v2 < 0;
      boolean n3 = v3 < 0;
      
      statements[i] = new Statement(n1, n2, n3, Math.abs(v1)-1, Math.abs(v2)-1, Math.abs(v3)-1);
    }
    
    boolean solFound = false;
    boolean[] assignments = null;
    
    while (!solFound) {
      boolean[] assigns = randLits(numLits, rand);
      
      int numTrue = trueCount(statements, assigns);
      
      if (numTrue >= numNeed) {
        assignments = assigns;
        solFound = true;
      }
      
    }
    
    printLits(assignments);
    
  }
  
  private static boolean[] randLits(int numLit, Random r) {
    
    boolean[] lits = new boolean[numLit];
    
    for(int i = 0; i < numLit; i++) {
      lits[i] = r.nextBoolean();
    }
    
    return lits;
  }
  
  private static int trueCount(Statement[] statements, boolean[] assignments) {
    int nt = 0;
    
    for(Statement s : statements) {
      boolean sta = (s.n1 ^ assignments[s.l1]) || (s.n2 ^ assignments[s.l2]) || (s.n3 ^ assignments[s.l3]);
      nt += sta ? 1 : 0;
    }
    
    return nt;
  }
  
  private static void printLits(boolean[] lits) {
    String toPrint = "";
    for(boolean l : lits) {
      int toAdd = l ? 1 : -1;
      toPrint += toAdd + " ";
    }
    
    System.out.println(toPrint.trim());
    
  }
  
}

class Statement{
  public boolean n1, n2, n3;
  public int l1, l2, l3;
  
  public Statement(boolean one, boolean two, boolean thr, int na, int nam, int name) {
    n1 = one;
    n2 = two;
    n3 = thr;
    l1 = na;
    l2 = nam;
    l3 = name;
  }
  
}
