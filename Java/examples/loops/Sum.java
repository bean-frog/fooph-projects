package examples.loops;
import java.util.*;
public class Sum {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter an integer: ");
        int number = scanner.nextInt();
        
        int sum = 0;
        while (number != 0) {
            sum += number % 10;
            number /= 10;
        }
        
        System.out.println("sum: " + sum);
        
        scanner.close();
    }
}
