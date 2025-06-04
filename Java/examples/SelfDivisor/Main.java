package examples.SelfDivisor;
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a number \n> ");
        int number = scanner.nextInt();
        
        int originalNumber = number;
        boolean isSelfDivisor = true;

        while (number != 0) {
            int digit = number % 10;
            
            if (digit == 0 || originalNumber % digit != 0) {
                isSelfDivisor = false;
                break;
            }
            
            number /= 10; 
        }

        if (isSelfDivisor) {
            System.out.println(originalNumber + " is a self-divisor.");
        } else {
            System.out.println(originalNumber + " is not a self-divisor.");
        }
    }
}