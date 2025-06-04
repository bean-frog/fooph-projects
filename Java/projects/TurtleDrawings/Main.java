import javax.swing.*;
import java.awt.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        // Get user input
        int n = Integer.parseInt(JOptionPane.showInputDialog("Enter number of sides:"));
        String colorInput = JOptionPane.showInputDialog("Enter comma-separated hex codes (e.g., #FF0000,#00FF00,#0000FF):");

        // hex codes into java Colors
        String[] hexCodes = colorInput.split(",");
        ArrayList<Color> colors = new ArrayList<>();
        for (String hex : hexCodes) {
            colors.add(Color.decode(hex.trim()));
        }

        World world = new World(400, 500);
        Turtle tia = new Turtle(world);

        drawPinwheel(tia, n, colors, 100, 100);
        drawPolygon(tia, n, colors, 100, 250);
        drawAsterisk(tia, n, colors, 100, 400);

        world.setVisible(true);
    }

    public static void drawPinwheel(Turtle t, int n, ArrayList<Color> colors, int cx, int cy) {
        t.penUp();
        t.moveTo(cx, cy);
        t.penDown();

        for (int i = 0; i < n; i++) {
            t.setColor(colors.get(i % colors.size()));
            t.setHeading(i * (360.0 / n));
            t.forward(40);
            t.backward(40);
        }
    }

    public static void drawPolygon(Turtle t, int n, ArrayList<Color> colors, int cx, int cy) {
        double radius = 40;
        double angleStep = 360.0 / n;

        // Move to first vertex
        t.penUp();
        double startAngle = 0;
        double x = cx + radius * Math.cos(Math.toRadians(startAngle));
        double y = cy - radius * Math.sin(Math.toRadians(startAngle));
        t.moveTo((int)x, (int)y);
        t.penDown();

        for (int i = 0; i < n; i++) {
            t.setColor(colors.get(i % colors.size()));
            double angle = i * angleStep;
            x = cx + radius * Math.cos(Math.toRadians(angle));
            y = cy - radius * Math.sin(Math.toRadians(angle));
            t.moveTo((int)x, (int)y);
        }

        // Connect last to first
        double endX = cx + radius * Math.cos(0);
        double endY = cy - radius * Math.sin(0);
        t.moveTo((int)endX, (int)endY);
    }

    public static void drawAsterisk(Turtle t, int n, ArrayList<Color> colors, int cx, int cy) {
        t.penUp();
        t.moveTo(cx, cy);
        t.penDown();

        for (int i = 0; i < n; i++) {
            t.setColor(colors.get(i % colors.size()));
            t.setHeading(i * (360.0 / n));
            t.forward(30);
            t.backward(30);
        }
    }
}
