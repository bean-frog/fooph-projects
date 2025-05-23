package projects.BankAccount;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;
import projects.BankAccount.Utils.*;
class BankAccount {
    private static class Account {
        String username;
        String passhash;
        double balance;

        Account(String username, String passhash, double balance) {
            this.username = username;
            this.passhash = passhash;
            this.balance = balance;
        }
    }

    private static List<Account> accounts = new ArrayList<>();
    private static final double WITHDRAW_LIMIT = 3000;
    private String authUser = null;

    static {
        // passwords shown in plaintext for demonstration purposes
        accounts.add(new Account("user1", hashPw("password"), 1.0));
        accounts.add(new Account("user2", hashPw("123456"), 2.0));
        accounts.add(new Account("user3", hashPw("verysecure"), 3.0));
    }

    public BankAccount(String name, String password) {
        for (Account account : accounts) {
            if (account.username.equals(name) && account.passhash.equals(hashPw(password))) {
                Utils.printInBox("Welcome, " + name);
                this.authUser = name;
                return;
            }
        }
        Utils.printInBox(Utils.formatAnsi("Bad username or password.", "red", true));
    }

    public Double getBalance() {
        if (authUser == null) {
            Utils.printInBox(Utils.formatAnsi("No authenticated user.", "red", true));
            return null;
        }
        for (Account account : accounts) {
            if (account.username.equals(authUser)) {
                return account.balance;
            }
        }
        return null;
    }

    public void withdraw(double amount) {
        if (authUser == null) {
            Utils.printInBox(Utils.formatAnsi("No authenticated user.", "red", true));
            return;
        }
        if (amount > WITHDRAW_LIMIT) {
            Utils.printInBox(Utils.formatAnsi(amount + " is above the withdraw limit." + "(limit: " + WITHDRAW_LIMIT + ")" , "red", true));
            return;
        }
        for (Account account : accounts) {
            if (account.username.equals(authUser)) {
                if (account.balance - amount < 0) {
                    Utils.printInBox("You don't have that much money you brokie.\n Balance: " + account.balance + "\n Attempted withdrawal: " + amount);
                } else {
                    account.balance -= amount;
                    Utils.printInBox(Utils.formatAnsi("New Balance: ", "green", true) + account.balance);
                }
                return;
            }
        }
    }

    public void deposit(double amount) {
        if (authUser == null) {
            Utils.printInBox(Utils.formatAnsi("No authenticated user.", "red", true));
            return;
        }
        for (Account account : accounts) {
            if (account.username.equals(authUser)) {
                account.balance += amount;
                Utils.printInBox(Utils.formatAnsi("New Balance: ", "green", true) + account.balance);
                return;
            }
        }
    }

    private static String hashPw(String pw) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(pw.getBytes());
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                hexString.append(String.format("%02x", b));
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Error hashing password", e);
        }
    }
}
