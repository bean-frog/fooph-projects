package projects.Balls;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;
import javax.swing.*;
import java.util.List;  


public class BallWorld extends JPanel {
   private static final int UPDATE_RATE = 30;
   private final List<Ball> balls = new ArrayList<>();
   private Square square1, square2;
   private ContainerBox box;
   private DrawCanvas canvas;
   private int canvasWidth, canvasHeight;

   public BallWorld(int width, int height) {
      canvasWidth = width;
      canvasHeight = height;

      Random rand = new Random();

      // Ask user how many balls to spawn
      int numBalls = 5; // default
      try {
         String input = JOptionPane.showInputDialog("Enter number of balls:");
         if (input != null) {
            numBalls = Math.max(1, Integer.parseInt(input));
         }
      } catch (NumberFormatException e) {
         JOptionPane.showMessageDialog(null, "Invalid input. Defaulting to 5 balls.");
      }

      // Spawn n balls
      for (int i = 0; i < numBalls; i++) {
         int radius = 15 + rand.nextInt(20); // 15-35
         int x = rand.nextInt(canvasWidth - 2 * radius);
         int y = rand.nextInt(canvasHeight - 2 * radius);
         int speed = 5 + rand.nextInt(10);
         int angle = rand.nextInt(360);
         Color color = new Color(rand.nextInt(256), rand.nextInt(256), rand.nextInt(256));
         balls.add(new Ball(x, y, radius, speed, angle, color));
      }

      // Create random squares
      square1 = new Square(canvasWidth, canvasHeight);
      square2 = new Square(canvasWidth, canvasHeight);

      box = new ContainerBox(0, 0, canvasWidth, canvasHeight, Color.BLACK, Color.WHITE);
      canvas = new DrawCanvas();
      this.setLayout(new BorderLayout());
      this.add(canvas, BorderLayout.CENTER);

      this.addComponentListener(new ComponentAdapter() {
         @Override
         public void componentResized(ComponentEvent e) {
            Dimension dim = e.getComponent().getSize();
            canvasWidth = dim.width;
            canvasHeight = dim.height;
            box.set(0, 0, canvasWidth, canvasHeight);
         }
      });

      bounce();
   }

   public void bounce() {
      Thread thread = new Thread(() -> {
         while (true) {
            update();
            repaint();
            try {
               Thread.sleep(1000 / UPDATE_RATE);
            } catch (InterruptedException ignored) {}
         }
      });
      thread.start();
   }

   public void update() {
      for (Ball b : balls) {
         b.moveOneStepWithCollisionDetection(box);
         b.collides(square1);
         b.collides(square2);
      }

      //ball to ball collisions
      for (int i = 0; i < balls.size(); i++) {
         for (int j = i + 1; j < balls.size(); j++) {
            balls.get(i).collides(balls.get(j));
         }
      }
   }

   class DrawCanvas extends JPanel {
      @Override
      public void paintComponent(Graphics g) {
         super.paintComponent(g);
         box.draw(g);
         square1.draw(g);
         square2.draw(g);
         for (Ball b : balls) {
            b.draw(g);
         }
      }

      @Override
      public Dimension getPreferredSize() {
         return new Dimension(canvasWidth, canvasHeight);
      }
   }
}
