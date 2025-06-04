package projects.BouncingBalls;
/*
 * BallWorld class with multiple balls and collision detection
 */

import java.awt.*;
import java.awt.event.*;
import java.util.Random;
import java.util.ArrayList;
import javax.swing.*;

public class BallWorld extends JPanel {
   private static final int UPDATE_RATE = 30;  // Frames per second (fps)
   private static final int NUM_BALLS = 5;     // Number of balls to create
   
   private ArrayList<Ball> balls;              // List to hold all balls

   private ContainerBox box;                   // The container rectangular box
  
   private DrawCanvas canvas;                  // Custom canvas for drawing the box/ball
   private int canvasWidth;
   private int canvasHeight;
  
   /**
    * Constructor to create the UI components and init the game objects.
    * Set the drawing canvas to fill the screen (given its width and height).
    * 
    * @param width : screen width
    * @param height : screen height
    */
   public BallWorld(int width, int height) {
      canvasWidth = width;
      canvasHeight = height;
      
      // Initialize the balls list
      balls = new ArrayList<Ball>();
      
      // Create multiple balls with random properties
      Random rand = new Random();
      
      for (int i = 0; i < NUM_BALLS; i++) {
         int radius = rand.nextInt(20) + 10;  // Radius between 10-30
         int x = rand.nextInt(canvasWidth - radius * 2 - 10) + 5;  // Ensure ball starts within bounds
         int y = rand.nextInt(canvasHeight - radius * 2 - 10) + 5;
         int speed = rand.nextInt(8) + 3;  // Speed between 3-10
         int angleInDegree = rand.nextInt(360);
         
         // Create balls with different colors
         Color color;
         switch (i % 5) {
            case 0:
               color = Color.RED;
               break;
            case 1:
               color = Color.BLUE;
               break;
            case 2:
               color = Color.GREEN;
               break;
            case 3:
               color = Color.YELLOW;
               break;
            default:
               color = Color.MAGENTA;
         }
         
         balls.add(new Ball(x, y, radius, speed, angleInDegree, color));
      }
      
      // Initialize the Container to fill the screen
      box = new ContainerBox(0, 0, canvasWidth, canvasHeight, Color.BLACK, Color.WHITE);
     
      // Initialize the custom drawing panel
      canvas = new DrawCanvas();
      this.setLayout(new BorderLayout());
      this.add(canvas, BorderLayout.CENTER);
      
      // Handling window resize
      this.addComponentListener(new ComponentAdapter() {
         @Override
         public void componentResized(ComponentEvent e) {
            Component c = (Component)e.getSource();
            Dimension dim = c.getSize();
            canvasWidth = dim.width;
            canvasHeight = dim.height;
            // Adjust the bounds of the container to fill the window
            box.set(0, 0, canvasWidth, canvasHeight);
         }
      });
  
      // Start the ball bouncing
      bounce();
   }
   
   /** Start the ball bouncing. */
   public void bounce() {
      // Run the game logic in its own thread.
      Thread thread = new Thread() {
         public void run() {
            while (true) {
               // Calculate what happens next 
               update();
               // Refresh the display
               repaint();
               // Makes the program slow down so things can be drawn properly
               try {
                  Thread.sleep(1000 / UPDATE_RATE);
               } catch (InterruptedException ex) {}
            }
         }
      };
      thread.start();  // start the thread for graphics
   }
   
   /** 
    * One time-step. 
    * Update the objects, with collision detection and response
    */
   public void update() {
      // Move all balls and detect collisions with walls
      for (Ball ball : balls) {
         ball.moveOneStepWithCollisionDetection(box);
      }
      
      // Check for collisions between all pairs of balls
      for (int i = 0; i < balls.size(); i++) {
         for (int j = i + 1; j < balls.size(); j++) {
            balls.get(i).collides(balls.get(j));
         }
      }
   }
   
   /** The custom drawing panel for the bouncing ball (inner class). */
   class DrawCanvas extends JPanel {
      /** Custom drawing codes */
      @Override
      public void paintComponent(Graphics g) {
         super.paintComponent(g);    // Paint background
         // Draw the box
         box.draw(g);
         // Draw all the balls
         for (Ball ball : balls) {
            ball.draw(g);
         }
      }
  
      /** Called back to get the preferred size of the component. */
      @Override
      public Dimension getPreferredSize() {
         return (new Dimension(canvasWidth, canvasHeight));
      }
   }
}
