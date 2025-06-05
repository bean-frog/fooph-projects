package projects.Balls;
import java.awt.*;
import java.util.Random;
// makes a square of a random size and pos
public class Square {
   public int x, y, size;
   private Color color;

   public Square(int canvasWidth, int canvasHeight) {
      Random rand = new Random();
      this.size = 40 + rand.nextInt(30); // 40–70 px
      this.x = rand.nextInt(canvasWidth - size);
      this.y = rand.nextInt(canvasHeight - size);
      this.color = Color.RED;
   }

   public void draw(Graphics g) {
      g.setColor(color);
      g.fillRect(x, y, size, size);
   }
}
