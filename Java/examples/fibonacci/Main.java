package examples.fibonacci;
import examples.fibonacci.Fibonacci;
public class Main {
   public static void main(String[] args) {
    Fibonacci f1 = new Fibonacci();
    for (int i = 0; i < 50; i++) {
        System.out.println(f1.nextFib());
    }
   }
    
}