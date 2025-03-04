import java.awt.*;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.io.IOException;
class DrawingPanel extends JPanel {
    public DrawingPanel() {
        setOpaque(false);
    }

//Update this to draw a *better* cow - do not modify the other functions    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

     /*   //body
        g.setColor(new Color(0xefefef));
        g.fillOval(10, 10, 500, 500);

        //head
        g.setColor(new Color(0x010203));
        g.drawOval(135, 50, 250, 250);

        //eyes
        g.fillOval(200,100,15,15);
        g.fillOval(300,100,15,15);

        //mouth
        g.setColor(new Color())
        yeah lol i give up
        */
    }
}

 //advanced
    //make a triangle/any other shape
    //g.drawPolygon(new int[] {1, 10, 20}, new int[] {1, 10, 20}, 3);
    //2D graphics so you can change rotation
    //Graphics2D g2 = (Graphics2D) g; //put at top of paintcomponent function (after super call)
    //g2.rotate(Math.toRadians(45)); //put BEFORE you draw
	

//Do not modify below this ---------------------------------------
/*public class CowFrames extends JFrame {
    public CowFrames() {
        init();
    }

    public void init() {
        setSize(600, 600);
        getContentPane().setBackground(Color.BLUE);

        DrawingPanel drawingPanel = new DrawingPanel();
        getContentPane().add(drawingPanel);

    }
}
*/

public class CowFrames extends JFrame {
    private BufferedImage cowImage;

    public CowFrames() {
        init();
    }
    
    public void init() {
        setSize(600, 600);
        setTitle("MOOOOOOOOOOOOOOOO");
        getContentPane().setBackground(Color.BLUE);

        try {
            cowImage = ImageIO.read(new File("./cow.jpg"));
        } catch (IOException e) {
            e.printStackTrace();
        }

        DrawingPanel drawingPanel = new DrawingPanel();
        getContentPane().add(drawingPanel);
    }

    private class DrawingPanel extends JPanel {
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.drawText
            if (cowImage != null) {
                int width = cowImage.getWidth();
                int height = cowImage.getHeight();
                double aspectRatio = (double) width / height;

                int panelWidth = getWidth();
                int panelHeight = getHeight();

                double scaleFactor = Math.min(panelWidth / (double) width, panelHeight / (double) height);

                int newWidth = (int) (scaleFactor * width);
                int newHeight = (int) (scaleFactor * height);

                int x = (panelWidth - newWidth) / 2;
                int y = (panelHeight - newHeight) / 2;

                g.drawImage(cowImage, x, y, newWidth, newHeight, null);
            }
        }
    }

}