package projects.BouncingBalls;
/*
 * Ball class with proper collision detection and response
 * - Handles wall bouncing
 * - Handles ball-to-ball collisions with physics-based responses
 */

import java.awt.*;
import java.awt.geom.Rectangle2D;
import java.util.Formatter;

public class Ball {
   public double x, y;           // Ball's center x and y
   public double speedX, speedY; // Ball's speed per step in x and y
   public double radius;       
   private Color color; 

   /**
    * Constructor to create the ball and it's attributes.
    * 
    * @param x : x coordinate of the center of the ball
    * @param y : y coordinate of the center of the ball
    * @param radius : radius of the ball
    * @param speed : speed the ball will move (converted to x and y components later)
    * @param angleInDegree : direction ball will initially move
    * @param color : color of the ball
    */
   public Ball(double x, double y, double radius, double speed, double angleInDegree, Color color) {
      //Notice the 'global' variables have the same name as the parameters.
      //Use the .this keyword to signify the 'global' variable
      this.x = x;   
      this.y = y;
      // Convert (speed, angle) to (x, y)
      this.speedX = (speed * Math.cos(Math.toRadians(angleInDegree)));
      this.speedY = (-speed * Math.sin(Math.toRadians(angleInDegree)));
      this.radius = radius;
      this.color = color;
   }

    /** 
    * Update the graphics on the screen
    * 
    * @param g: Graphics object 
    */
   public void draw(Graphics g) {
      g.setColor(color);
      g.fillOval((int) x, (int) y, (int)(2 * radius), (int)(2 * radius));
   }
   
   /** 
    * Move, check for collisions and react accordingly if collision occurs.
    * 
    * @param box: the container (obstacle) for this ball. 
    */
   public void moveOneStepWithCollisionDetection(ContainerBox box) {
      // Get the ball's bounds, accounting for the ball's edge rather than center
      double ballMinX = x;
      double ballMinY = y;
      double ballMaxX = x + 2 * radius;
      double ballMaxY = y + 2 * radius;
      
      // Move the ball
      x += speedX;
      y += speedY;
      
      // Check collision with the container's boundaries
      // Check left boundary
      if (ballMinX + speedX < box.minX) {
         speedX = -speedX; // Reflect along x direction
         x = box.minX; // Re-position the ball at the boundary
      } 
      // Check right boundary
      else if (ballMaxX + speedX > box.maxX) {
         speedX = -speedX;
         x = box.maxX - 2 * radius;
      }
      
      // Check top boundary
      if (ballMinY + speedY < box.minY) {
         speedY = -speedY;
         y = box.minY;
      } 
      // Check bottom boundary
      else if (ballMaxY + speedY > box.maxY) {
         speedY = -speedY;
         y = box.maxY - 2 * radius;
      }
   }

   public void collides(Ball b2) {
      // Calculate distance between ball centers
      double dx = (x + radius) - (b2.x + b2.radius);
      double dy = (y + radius) - (b2.y + b2.radius);
      double distance = Math.sqrt(dx * dx + dy * dy);
      
      // Check if the balls are colliding (if distance is less than sum of radii)
      if (distance < radius + b2.radius) {
         // Calculate the collision unit vector
         double nx = dx / distance;
         double ny = dy / distance;
         
         // Calculate relative velocity
         double dvx = b2.speedX - speedX;
         double dvy = b2.speedY - speedY;
         
         // Calculate velocity along the unit normal
         double velocityAlongNormal = dvx * nx + dvy * ny;
         
         // Don't proceed if balls are moving away from each other
         if (velocityAlongNormal > 0) {
            return;
         }
         
         // Calculate impulse (conservation of momentum)
         double impulse = -2.0 * velocityAlongNormal;
         
         // Calculate new velocities
         speedX -= impulse * nx;
         speedY -= impulse * ny;
         b2.speedX += impulse * nx;
         b2.speedY += impulse * ny;
         
         // Move balls apart to prevent sticking
         double overlap = radius + b2.radius - distance;
         x -= overlap * nx * 0.5;
         y -= overlap * ny * 0.5;
         b2.x += overlap * nx * 0.5;
         b2.y += overlap * ny * 0.5;
      }
   }
   
   /** Return the magnitude of speed. */
   public double getSpeed() {
      return Math.sqrt(speedX * speedX + speedY * speedY);
   }
   
   /** Return the direction of movement in degrees (counter-clockwise). */
   public double getMoveAngle() {
      return Math.toDegrees(Math.atan2(-speedY, speedX));
   }
}
