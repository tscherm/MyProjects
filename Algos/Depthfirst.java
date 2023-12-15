import java.util.Scanner;
import java.util.Hashtable;

public class DepthFirst {
  
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
    
    //set toPrint to ""
    toPrint = "";
    
    // create hashtable
    Hashtable<String, Integer> table = new Hashtable<String, Integer>();
    
    // create array with nodes and find num nodes

    int numNodes = Integer.parseInt(scan.nextLine()); 

    Node[] nodes = new Node[numNodes];
    
    // make array with all nodes O(v)
    for(int i = 0; i < numNodes; i++) {
      // get strings
      String newNode = scan.nextLine().trim();
      String name = firstString(newNode);
      String[] adjacencies = adjacencyList(newNode, numNodes);
      
      Node toAdd = new Node(name, adjacencies);
      
      table.put(name, i);
      nodes[i] = toAdd;
    }
    
    // get list of neighbors for each node O(E)
    for(Node n : nodes) {
      n.hash(nodes, table);     
    }
    
    // find next un-visited node and search that graph O(E)
    for(Node n : nodes) {
      if(!n.visited) {
     // recursive implementation
        addNode(n);
      }
    }
    
    //print result
    System.out.println(toPrint.trim());
    
  }
  
  /*
   * get name of node
   * O(1)
   */
  private static String firstString(String str) {
    
    Scanner scnr = new Scanner(str);
    String toReturn = scnr.next();
    
    scnr.close();
    return toReturn;
    
  }

  /*
   * get name of adjacencies
   * O(V) (Worst cases where a node is connected to all nodes)
   */
  private static String[] adjacencyList(String str, int max) {
    
    Scanner scnr = new Scanner(str);
    int size = 0;
    String[] tempArray = new String[max-1];
    scnr.next(); // get rid of name part
    
    while(scnr.hasNext()) {
      tempArray[size] = scnr.next();
      size++;
    }
    
    String[] toReturn = new String[size];
    System.arraycopy(tempArray, 0, toReturn, 0, size);
    
    
    scnr.close();
    return toReturn;
    
  }
  
  /*
   * recursively visits each node and checks each edge
   * run time 2E exists in O(E) (Worst case one graph has all edges)
   */
  private static void addNode(Node node) {
    
    // change string and indicate node was visited.
    toPrint += node.name + " ";
    node.visited = true;
    
    // look at each edge and see if 
    for(Node n : node.neighbors) {
      //visit next node that hasn't already been accessed
      if(!n.visited) {
        addNode(n);
      }
    }    
  }

}

class Node {
  
  public String name;
  public String[] adjacencies;
  public Node[] neighbors = new Node[1];
  public boolean visited = false;
  
  public Node(String name, String[] adjacencies) {
    this.name = name;
    this.adjacencies = adjacencies;
    neighbors = new Node[adjacencies.length];
  }
  
  public void hash(Node[] nodes, Hashtable<String, Integer> table) {
    
    // hash each adjacency into neighbors
    for(int i = 0; i < adjacencies.length; i++) {
      
      neighbors[i] = nodes[table.get(adjacencies[i])];
      
    }
    
  }
  
}

