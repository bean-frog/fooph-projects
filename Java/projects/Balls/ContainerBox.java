package projects.Balls;

/*
 * You do not need to alter anything in this Class.
 *
 * A rectangular container box, containing the bouncing ball.  
 */

import java.awt.*;

public class ContainerBox {
   int minX, maxX, minY, maxY;  
   private Color colorFilled;  
   private Color colorBorder;   
   
   /** Constructor */
   public ContainerBox(int x, int y, int width, int height, Color colorFilled, Color colorBorder) {
      minX = x;
      minY = y;
      maxX = x + width - 1;
      maxY = y + height - 1;
      this.colorFilled = colorFilled;
      this.colorBorder = colorBorder;
   }
   
   /** Set or reset the boundaries of the box. */
   public void set(int x, int y, int width, int height) {
      minX = x;
      minY = y;
      maxX = x + width - 1;
      maxY = y + height - 1;
   }

   /** Draw itself using the given graphic context. */
   public void draw(Graphics g) {
      g.setColor(colorFilled);
      g.fillRect(minX, minY, maxX - minX - 1, maxY - minY - 1);
      g.setColor(colorBorder);
      g.drawRect(minX, minY, maxX - minX - 1, maxY - minY - 1);
   }
}
