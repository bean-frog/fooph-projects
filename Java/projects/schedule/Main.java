
package projects.schedule;
import java.util.*;

public class Main {
    public static void main(String[] args) {
       boolean alldays = false;
       for (String string : args) {
        if (string.contains("alldays")) {
            alldays = true;
        }
       }
       
        Scanner scanner = new Scanner(System.in);
        List<String> classList = new ArrayList<>();

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        int numInputtedClasses = 0;
        while (numInputtedClasses < 7) {
            System.out.print("Enter class " + (numInputtedClasses + 1) + ": ");
            String className = scanner.nextLine();
            classList.add(className); 
            numInputtedClasses++;
        }
        String[] classes = classList.toArray(new String[0]);

            if (alldays == true) {
                String[] days = {"monday", "tuesday", "wednesday", "thursday", "friday"};
                for (String item : days) {
                    Tui.Generate(name, item, classes);
                }
            } else if (alldays == false && args.length == 0) {
                String day = java.time.LocalDate.now().getDayOfWeek().toString();
                Tui.Generate(name, day, classes);
            } else {
                // todo finish this bs
                String day;
                Tui.Generate(name, args[0].toLowerCase().trim(), classes);
            }
        
        scanner.close();
    }
}
