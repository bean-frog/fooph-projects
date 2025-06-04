package examples.loops;

public class Cross {
    public static void main(String[] args) {
        int x = Integer.parseInt(args[0]);
        String character = "🯅";
        for (int i = 0; i < x; i++) {
            for (int s = 0; s < x; s++) {
                System.out.print(" ");
            }
            for (int j = 0; j < x; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
        for (int i = 0; i < x; i++) {
            for (int j = 0; j < 3 * x; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
        for (int i = 0; i < x; i++) {
            for (int s = 0; s < x; s++) {
                System.out.print(" ");
            }
            for (int j = 0; j < x; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
    }
}
