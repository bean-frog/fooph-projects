package projects.Balls;
import java.awt.*;
import java.awt.geom.Rectangle2D;

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
   // Used to determine how to reflect off the walls of the screen
public void moveOneStepWithCollisionDetection(ContainerBox box) {
   x += speedX;
   y += speedY;

   // Wall collision
   if (x - radius < box.minX) {
      speedX = Math.abs(speedX);
      x = box.minX + radius;
   } else if (x + radius > box.maxX) {
      speedX = -Math.abs(speedX);
      x = box.maxX - radius;
   }

   if (y - radius < box.minY) {
      speedY = Math.abs(speedY);
      y = box.minY + radius;
   } else if (y + radius > box.maxY) {
      speedY = -Math.abs(speedY);
      y = box.maxY - radius;
   }
}
public void collides(Ball b2) {
   double dx = b2.x - this.x;
   double dy = b2.y - this.y;
   double dist = Math.sqrt(dx * dx + dy * dy);
   double minDist = this.radius + b2.radius;

   if (dist < minDist && dist != 0) {
      // normalize direction 
      double nx = dx / dist;
      double ny = dy / dist;

      // dot product of velocity and normalized
      double v1n = speedX * nx + speedY * ny;
      double v2n = b2.speedX * nx + b2.speedY * ny;

      double m1 = v2n;
      double m2 = v1n;

      speedX += (m1 - v1n) * nx;
      speedY += (m1 - v1n) * ny;
      b2.speedX += (m2 - v2n) * nx;
      b2.speedY += (m2 - v2n) * ny;

      
      double speed = getSpeed();
      double angle = Math.atan2(speedY, speedX);
      speedX = speed * Math.cos(angle);
      speedY = speed * Math.sin(angle);

      double b2Speed = b2.getSpeed();
      double b2Angle = Math.atan2(b2.speedY, b2.speedX);
      b2.speedX = b2Speed * Math.cos(b2Angle);
      b2.speedY = b2Speed * Math.sin(b2Angle);

      // Separate overlapping balls
      double overlap = 0.5 * (minDist - dist + 1);
      this.x -= overlap * nx;
      this.y -= overlap * ny;
      b2.x += overlap * nx;
      b2.y += overlap * ny;
   }
}

public void collides(Square s) {
   Rectangle2D square = new Rectangle2D.Double(s.x, s.y, s.size, s.size);
   Rectangle2D ballBounds = new Rectangle2D.Double(x - radius, y - radius, 2 * radius, 2 * radius);

   if (square.intersects(ballBounds)) {
      double cx = s.x + s.size / 2.0;
      double cy = s.y + s.size / 2.0;
      double dx = (x + radius) - cx;
      double dy = (y + radius) - cy;
      double angle = Math.atan2(dy, dx);

      double speed = getSpeed();
      speedX = speed * Math.cos(angle);
      speedY = speed * Math.sin(angle);

      // put ball outside of square to stop sticking
      if (dx != 0 || dy != 0) {
         x += Math.signum(dx) * 2;
         y += Math.signum(dy) * 2;
      }
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