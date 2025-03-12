import java.util.*;
public class ThreeScores {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter first score:");
        int score1 = input.nextInt();
        System.out.println("Enter second score:");
        int score2 = input.nextInt();
        System.out.println("Enter third score:");
        int score3 = input.nextInt();

        int total = (score1 + score2 + score3);
        System.out.println("Average score: " + total / 3);
        
        input.close();
    }
}
