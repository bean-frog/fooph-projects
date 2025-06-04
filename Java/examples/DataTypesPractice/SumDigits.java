package examples.DataTypesPractice;
import java.util.*;
public class SumDigits {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.print("input integer");
        int num = input.nextInt();

        int first = num % 10;
        int remainder = num / 10;
        int second = remainder % 10;
        remainder = remainder / 10;
        int third = remainder % 10;
        remainder = remainder / 10;
        int fourth = remainder % 10;
        int sum = third + second + first + fourth;
        System.out.println("Sum: " + sum);
        input.close();

    }
}
