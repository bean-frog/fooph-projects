package examples.u2d2;

public class Main {
    public static void printStars(int numStars) {
        for (int i = 0; i < numStars; i++) {
            System.out.print("*");
        }
        System.out.println();
    }
    public static void printChars(String character, int numChars) {
        for (int i = 0; i < numChars; i++) {
            System.out.print(character);
        }
        System.out.println();
    }
    public static void printOddIndices(String input) {
        for (int i = 1; i < input.length(); i += 2) {
            System.out.print(input.charAt(i));
        }
    }
    public static void printRowsOfStars(int num) {
        for (int i = 1; i <= num; i++) {
            for (int j = 0; j < i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
    public static void main(String[] args) {
    //    printStars(5);
    //     printChars("e", 5);
    //     printOddIndices("hello");
    printRowsOfStars(5);
    }
}
