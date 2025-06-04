package examples.stars;

public class Star {
    private int num;
    private String character = "𜱃";
    public Star() {
        this.num = 5;
    }
    public Star(int num) {
        this.num = num;
    }
    private void header(String text) {
        System.out.println("┏━━━" + text + "━━━┓");
    }
    public void printStars() {
        header("printStars");
        for (int i = 0; i < num; i++) {
            System.out.print(character);
        }
        System.out.println();
    }
    public void printRowsOfStars(){
        header("printRowsOfStars");
        for (int i = 1; i <= num; i++) {
            for (int j = 0; j < i; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
    }
    public void cross() {
        header("cross");
        for (int i = 0; i < num; i++) {
            for (int s = 0; s < num; s++) {
                System.out.print(" ");
            }
            for (int j = 0; j < num; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
        for (int i = 0; i < num; i++) {
            for (int j = 0; j < 3 * num; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
        for (int i = 0; i < num; i++) {
            for (int s = 0; s < num; s++) {
                System.out.print(" ");
            }
            for (int j = 0; j < num; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
    }
    public void printSolidDiamond() {
        header("printSolidDiamond");
         for (int i = 0; i < num; i++) {
            for (int j = 0; j < num - i - 1; j++) {
                System.out.print(" ");
            }
            for (int j = 0; j < 2 * i + 1; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
        
        for (int i = num - 2; i >= 0; i--) {
            for (int j = 0; j < num - i - 1; j++) {
                System.out.print(" ");
            }
            for (int j = 0; j < 2 * i + 1; j++) {
                System.out.print(character);
            }
            System.out.println();
        }
    }
    
}
