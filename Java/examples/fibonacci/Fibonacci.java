package examples.fibonacci;
public class Fibonacci {
    public long num1;
    private long num2;
    public Fibonacci() {
        num1 = 1;
        num2 = 2;
    }
    public long nextFib() {
        long num3 = num2;
        num2+=num1;
        num1=num3;
        return num2;

    }
}