package examples.DataTypesPractice;
import java.util.*;
public class FtoC {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.print("Input fahrenheit:");
        double fahrenheit = input.nextDouble();
        if (fahrenheit == 451) {
            System.out.println("It was a pleasure to burn....");
        }
        double  celsius =(( 5 *(fahrenheit - 32.0)) / 9.0);
        System.out.println("F: " + fahrenheit + "\nC: " + celsius );   
        input.close();
    }
}
