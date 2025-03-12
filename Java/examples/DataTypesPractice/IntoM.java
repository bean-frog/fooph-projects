package examples.DataTypesPractice;
import java.util.*;
public class IntoM {
    public static void main(String[] args) {
        
        Scanner input = new Scanner(System.in);

        System.out.print("Input icnhes");
        double inch = input.nextDouble();
        double meters = inch * 0.0254;
        System.out.println("M: " + meters + "In: " + inch);
        input.close();
    }
}
