package projects.schedule;
import java.util.*;

public class Tui {
    private static String vertical = "┃";
    private static String horizontal = "━";
    private static String cornerTR = "┓";
    private static String cornerTL = "┏";
    private static String cornerBR = "┛";
    private static String cornerBL = "┗";

    public static void Generate(String title, String day, String[] classes) {
        // set period order and times based on provided day
        Map<String, String> periodTimes = new LinkedHashMap<>();
        List<String> periodOrder = new ArrayList<>();
        switch(day.toLowerCase()) {
            case "monday":
                periodOrder = Arrays.asList("P1", "P2", "P3", "P4", "P5", "P6", "P7");
                periodTimes.put("P1", "9:00 AM");
                periodTimes.put("P2", "9:55 AM");
                periodTimes.put("P3", "10:55 AM");
                periodTimes.put("P4", "11:50 AM");
                periodTimes.put("P5", "1:15 PM");
                periodTimes.put("P6", "2:10 PM");
                periodTimes.put("P7", "3:05 PM");
                break;
            case "wednesday":
                periodOrder = Arrays.asList("P5", "P6", "P7", "PRIME");
                periodTimes.put("P5", "9:00 AM");
                periodTimes.put("P6", "10:50 AM");
                periodTimes.put("P7", "1:00 PM");
                periodTimes.put("PRIME", "2:40 PM");
                break;
            case "friday":
                periodOrder = Arrays.asList("P5", "P6", "Adv/SH", "P7");
                periodTimes.put("P5", "9:00 AM");
                periodTimes.put("P6", "10:50 AM");
                periodTimes.put("Adv/SH", "1:00 PM");
                periodTimes.put("P7", "2:00 PM");
                break;
            case "tuesday":
                periodOrder = Arrays.asList("P1", "P2", "P3", "P4");
                periodTimes.put("P1", "9:00 AM");
                periodTimes.put("P2", "10:50 AM");
                periodTimes.put("P3", "1:00 PM");
                periodTimes.put("P4", "2:40 PM");
                break;
            case "thursday":
                periodOrder = Arrays.asList("P1", "P2", "P3", "P4");
                periodTimes.put("P1", "9:00 AM");
                periodTimes.put("P2", "10:50 AM");
                periodTimes.put("P3", "1:00 PM");
                periodTimes.put("P4", "2:40 PM");
                break;
            default: // Saturday/Sunday/Invalid
                System.out.println("No School!");
                break;
        }

        // calculate column widths
        int periodWidth = 2;

        if (periodTimes.containsKey("Adv/SH")) {
            periodWidth = 6;
        } else if (periodTimes.containsKey("PRIME")) {
            periodWidth = 5;
        }

        int timeWidth = 10;
        int classWidth = 30;
        String rowFormat = vertical + " %-" + timeWidth + "s " + vertical 
                           + " %-" + periodWidth + "s " + vertical 
                           + " %-" + classWidth + "s " + vertical;
        String sampleRow = String.format(rowFormat, "", "", "");
        int totalWidth = sampleRow.length();

        // Title
        String fullTitle = title + " - " + day;
        int topInnerWidth = totalWidth - 2;
        int leftBars = 2;
        int rightBars = topInnerWidth - leftBars - fullTitle.length();
        StringBuilder topBorder = new StringBuilder();
        topBorder.append(cornerTL);
        for (int i = 0; i < leftBars; i++) topBorder.append(horizontal);
        topBorder.append(fullTitle);
        for (int i = 0; i < rightBars; i++) topBorder.append(horizontal);
        topBorder.append(cornerTR);

        // Bottom border
        StringBuilder bottomBorder = new StringBuilder();
        bottomBorder.append(cornerBL);
        for (int i = 0; i < totalWidth - 2; i++) bottomBorder.append(horizontal);
        bottomBorder.append(cornerBR);

        // print out completed box
        System.out.println(topBorder.toString());
        for (String periodKey : periodOrder) {
            String time = periodTimes.get(periodKey);
            String className;

            // get class names
            switch (periodKey) {
                case "P1": className = classes[0]; break;
                case "P2": className = classes[1]; break;
                case "P3": className = classes[2]; break;
                case "P4": className = classes[3]; break;
                case "P5": className = classes[4]; break;
                case "P6": className = classes[5]; break;
                case "P7": className = classes[6]; break;
                case "PRIME": className = "PRIME"; break;
                case "Adv/SH": className = "Adv/SH"; break;
                default: className = "N/A"; break;
            }

            System.out.println(String.format(rowFormat, time, periodKey, className));
        }
        System.out.println(bottomBorder.toString());
    }


}
