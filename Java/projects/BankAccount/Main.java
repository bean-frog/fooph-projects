package projects.BankAccount;
import java.util.Scanner;
import projects.BankAccount.Utils;
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("V E R Y  S E C U R E  B A N K I N G ™ Java Edition");

        System.out.print("username: ");
        String username = scanner.nextLine();

        System.out.print("password: ");
        String password = scanner.nextLine();

        BankAccount user = new BankAccount(username, password);

        while (true) {
            System.out.println(Utils.formatAnsi("1. View Balance", "white", false));
            System.out.println(Utils.formatAnsi("2. Withdraw", "white", false));
            System.out.println(Utils.formatAnsi("3. Deposit", "white", false));
            System.out.println(Utils.formatAnsi("4. Exit", "white", false));

            System.out.print("Enter a number\n> ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    Utils.printInBox("" + user.getBalance());
                    break;
                case 2:
                    System.out.print("Enter an amount to withdraw\n> ");
                    user.withdraw(scanner.nextDouble());
                    break;
                case 3:
                    System.out.print("Enter an amount to deposit\n> ");
                    user.deposit(scanner.nextDouble());
                    break;
                case 4:
                    System.exit(0);
                    scanner.close();
                default:
                    System.out.println("Invalid choice");
            }
        }
    }
}
