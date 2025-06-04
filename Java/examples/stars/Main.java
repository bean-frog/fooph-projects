package examples.stars;
import examples.stars.Star;
public class Main {
    public static void main(String[] args) {
        Star star1 = new Star(5);
        star1.printStars();
        star1.printRowsOfStars();
        star1.cross();
        star1.printSolidDiamond();
    }
}
