package projects.BankAccount;
public class Utils {

    // ANSI escape code formatter
    public static String formatAnsi(String text, String color, boolean bold) {
        String ansiCode = "";
        switch (color.toLowerCase()) {
            case "red":
                ansiCode = "\u001B[31m";
                break;
            case "green":
                ansiCode = "\u001B[32m";
                break;
            case "yellow":
                ansiCode = "\u001B[33m";
                break;
            case "blue":
                ansiCode = "\u001B[34m";
                break;
            case "purple":
                ansiCode = "\u001B[35m";
                break;
            case "cyan":
                ansiCode = "\u001B[36m";
                break;
            default:
                ansiCode = "\u001B[0m"; // Reset
        }
        if (bold) {
            ansiCode += "\u001B[1m";
        }
        return ansiCode + text + "\u001B[0m";
    }

    // Print text inside a box
    public static void printInBox(String text) {
        int length = text.length();
        
        // Print top border
        System.out.print("+");
        for (int i = 0; i < length + 2; i++) {
            System.out.print("-");
        }
        System.out.println("+");
        
        // Print text line
        System.out.println("| " + text + " |");
        
        // Print bottom border
        System.out.print("+");
        for (int i = 0; i < length + 2; i++) {
            System.out.print("-");
        }
        System.out.println("+");
    }
}
