import axios from "axios";
import sqlite3 from "sqlite3";
import bcrypt from "bcrypt";
import Database from "./db.ts";
import Utils from "./utils.ts";

// CS50 stock api response type
interface StockResponse {
  companyName: string;
  latestPrice: number;
  symbol: string;
}

// stock holding type (from db)
interface Holding {
  symbol: string;
  amount: number;
}

class Stocks {
  private db: sqlite3.Database;
  private currentUser: string | null = null; // Tracks the logged-in user

  constructor() {
    // Use the Database class for the SQLite connection.
    const database = new Database();
    this.db = database.db;
  }

  // Check stock info
  public async getStockInfo(symbol: string): Promise<StockResponse | string> {
    const url = `https://finance.cs50.io/quote?symbol=${symbol.toUpperCase()}`;
    try {
      const response = await axios.get<StockResponse>(url);
      Utils.success(`Found data for ${symbol.toUpperCase()}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        if (error.response.status === 404) {
          Utils.warning(`Stock with symbol ${symbol} not found.`);
          return `Stock with symbol ${symbol} not found`;
        } else {
          Utils.failure(`Error fetching stock data: ${error}`);
          return `Error fetching stock data: ${error}`;
        }
      } else {
        Utils.failure(`Unknown error occurred while fetching stock data: ${error}`);
        return `Unknown error occurred while fetchin stock data: ${error}`;
      }
    }
  }

  // Create a new account
  public async createAccount(name: string, pass: string): Promise<string> {
    const hashedPassword = await bcrypt.hash(pass, 10);
    return new Promise((resolve, reject) => {
      const query = `INSERT INTO users (username, password) VALUES (?, ?)`;
      this.db.run(query, [name, hashedPassword], (err) => {
        if (err) {
          if (err.message.includes("UNIQUE")) {
            Utils.warning(`Tried to create account ${name} but username already exists.`);
            resolve("Username already exists");
          } else {
            Utils.failure(`Unable to create account for an unknown reason.`);
            reject("Error creating account");
          }
        } else {
          Utils.success(`Created account with name ${name}.`);
          resolve("Account created successfully");
        }
      });
    });
  }

  // Log in
  public async login(name: string, pass: string): Promise<string> {
    return new Promise((resolve, reject) => {
      const query = `SELECT id, password FROM users WHERE username = ?`;
      this.db.get(query, [name], async (err, row: any) => {
        if (err || !row) {
          Utils.warning(`Invalid username or password (name: ${name})`);
          resolve("401"); // 401 Unauthorized
        } else {
          const validPassword = await bcrypt.compare(pass, row.password);
          if (validPassword) {
            this.currentUser = name;
            Utils.success(`${name} logged in`);
            resolve("200"); // 200 OK
          } else {
            Utils.warning(`Invalid username or password (name: ${name})`);
            resolve("500"); // 500 Server Error
          }
        }
      });
    });
  }

  // Log out
  public logout(): string {
    if (!this.currentUser) {
      Utils.warning(`Received logout request, but no user is logged in`);
      return "You must be logged in";
    }
    const tempUserRef = this.currentUser;
    this.currentUser = null;
    Utils.success(`${tempUserRef} logged out`);
    return "Logged out successfully";
  }

  // Update balance
  public async updateBalance(amount: number): Promise<string> {
    if (!this.currentUser) {
      Utils.warning(`Received balance update request, but no user is logged in`);
      return "You must be logged in";
    }
    return new Promise((resolve, reject) => {
      const query = `UPDATE users SET balance = balance + ? WHERE username = ?`;
      this.db.run(query, [amount, this.currentUser], (err) => {
        if (err) {
          Utils.failure(`Error updating balance of ${this.currentUser}: ${err}`);
          reject("Error updating balance");
        } else {
          Utils.success(`Added ${amount} to balance of ${this.currentUser}`);
          resolve("Balance updated");
        }
      });
    });
  }

  // View balance
  public async getBalance(): Promise<{ balance?: number; error?: string }> {
    if (!this.currentUser) {
      Utils.warning(`Received balance request, but no user is logged in`);
      return { error: "You must be logged in" };
    }
    return new Promise((resolve) => {
      const query = `SELECT balance FROM users WHERE username = ?`;
      this.db.get(query, [this.currentUser], (err, row: any) => {
        if (err || !row) {
          console.error("Error retrieving balance:", err);
          resolve({ error: "Error retrieving balance" });
        } else {
          resolve({ balance: row.balance });
        }
      });
    });
  }

  // Buy stocks
  public async buyStock(symbol: string, amount: number): Promise<string> {
    if (!this.currentUser) {
      Utils.warning(`Received stock purchase request, but no user is logged in`);
      return "You must be logged in";
    }

    // Check if symbol is valid and retrieve the current price.
    let stockData: StockResponse;
    try {
      const response = await axios.get<StockResponse>(
        `https://finance.cs50.io/quote?symbol=${symbol.toUpperCase()}`
      );
      if (response.status !== 200 || !response.data) {
        Utils.warning(`Invalid stock symbol: ${symbol}`);
        return `Invalid stock symbol: ${symbol}`;
      }
      stockData = response.data;
    } catch (error) {
      Utils.warning(`Failed to fetch stock data for symbol: ${symbol}. Error: ${error}`);
      return `Could not retrieve stock data for symbol: ${symbol}`;
    }

    const price = stockData.latestPrice;
    const totalCost = price * amount;

    // Retrieve the current user's ID.
    let userId: number | string;
    try {
      userId = await this.getUserId();
      if (typeof userId === "string") return userId;
    } catch (err) {
      return "Error retrieving user ID";
    }

    // Retrieve user's current balance.
    let currentBalance: number;
    try {
      const balanceQuery = `SELECT balance FROM users WHERE id = ?`;
      currentBalance = await new Promise<number>((resolve, reject) => {
        this.db.get(balanceQuery, [userId], (err, row: any) => {
          if (err) {
            reject(`Failed to retrieve user balance: ${err.message}`);
          } else {
            resolve(row?.balance ?? 0);
          }
        });
      });
    } catch (err) {
      return typeof err === "string" ? err : "Error retrieving balance";
    }

    if (currentBalance < totalCost) {
      Utils.warning(`User ${userId} cannot afford ${amount} shares of ${symbol} at $${price} each.`);
      return `You cannot afford ${amount} shares of ${symbol}`;
    }

    // Deduct the cost from the user's balance.
    try {
      const updateBalanceQuery = `UPDATE users SET balance = balance - ? WHERE id = ?`;
      await new Promise<void>((resolve, reject) => {
        this.db.run(updateBalanceQuery, [totalCost, userId], (err) => {
          if (err) {
            reject(`Failed to update user balance: ${err.message}`);
          } else {
            resolve();
          }
        });
      });
    } catch (err) {
      return typeof err === "string" ? err : "Error updating balance";
    }

    // Add or update the stock holding.
    try {
      const stockQuery = `
        INSERT INTO stocks (user_id, symbol, amount)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, symbol)
        DO UPDATE SET amount = amount + excluded.amount
      `;
      await new Promise<void>((resolve, reject) => {
        this.db.run(stockQuery, [userId, symbol, amount], (err) => {
          if (err) {
            reject(`Failed to update stock records: ${err.message}`);
          } else {
            resolve();
          }
        });
      });
    } catch (err) {
      return typeof err === "string" ? err : "Error updating stock records";
    }

    return `Bought ${amount} shares of ${symbol} at $${price} each for a total cost of $${totalCost.toFixed(2)}`;
  }

  // Sell stocks
  public async sellStock(symbol: string, amount: number): Promise<string> {
    if (!this.currentUser) {
      Utils.warning(`Received stock sale request, but no user is logged in`);
      return "You must be logged in";
    }

    let userId: number | string;
    try {
      userId = await this.getUserId();
      if (typeof userId === "string") return userId;
    } catch (err) {
      return "Error retrieving user ID";
    }

    // Verify the user has enough shares to sell.
    try {
      await new Promise<void>((resolve, reject) => {
        const holdingQuery = `SELECT amount FROM stocks WHERE user_id = ? AND symbol = ?`;
        this.db.get(holdingQuery, [userId, symbol], (err, row: any) => {
          if (err) {
            reject("Error retrieving holding");
          } else if (!row || row.amount < amount) {
            reject("Not enough shares to sell");
          } else {
            resolve();
          }
        });
      });
    } catch (err) {
      return typeof err === "string" ? err : "Error retrieving holding";
    }

    // Retrieve the latest stock price.
    let stockData: StockResponse;
    try {
      const response = await axios.get<StockResponse>(
        `https://finance.cs50.io/quote?symbol=${symbol.toUpperCase()}`
      );
      if (response.status !== 200 || !response.data) {
        Utils.warning(`Invalid stock symbol: ${symbol}`);
        return `Invalid stock symbol: ${symbol}`;
      }
      stockData = response.data;
    } catch (error) {
      Utils.warning(`Failed to fetch stock data for symbol: ${symbol}. Error: ${error}`);
      return `Could not retrieve stock data for symbol: ${symbol}`;
    }

    const price = stockData.latestPrice;
    const revenue = price * amount;

    // Update holdings
    try {
      await new Promise<void>((resolve, reject) => {
        const updateHoldingsQuery = `
          UPDATE stocks
          SET amount = amount - ?
          WHERE user_id = ? AND symbol = ? AND amount >= ?
        `;
        this.db.run(updateHoldingsQuery, [amount, userId, symbol, amount], (err) => {
          if (err) reject("Error selling stock");
          else resolve();
        });
      });
    } catch (err) {
      return typeof err === "string" ? err : "Error selling stock";
    }

    // Update the user's balance with the revenue from the sale.
    try {
      await new Promise<void>((resolve, reject) => {
        const updateBalanceQuery = `UPDATE users SET balance = balance + ? WHERE id = ?`;
        this.db.run(updateBalanceQuery, [revenue, userId], (err) => {
          if (err) reject("Error updating balance after sale");
          else resolve();
        });
      });
    } catch (err) {
      return typeof err === "string" ? err : "Error updating balance after sale";
    }

    return `Sold ${amount} shares of ${symbol} at $${price} each for a total revenue of $${revenue.toFixed(2)}`;
  }

  public async getHoldings(): Promise<Holding[] | string> {
    if (!this.currentUser) {
      Utils.warning(`Received holdings request, but no user is logged in`);
      return "You must be logged in";
    }

    const userId = await this.getUserId();
    if (typeof userId === "string") return userId;

    return new Promise((resolve, reject) => {
      const query = `SELECT symbol, amount FROM stocks WHERE user_id = ?`;
      this.db.all(query, [userId], (err, rows: Holding[]) => {
        if (err) {
          Utils.failure(`Error retrieving holdings for user ${userId}: ${err.message}`);
          reject("Error retrieving holdings");
        } else {
          Utils.success(`Retrieved holdings for user ${userId}`);
          resolve(rows);
        }
      });
    });
  }

  // Helper to get the current user's ID
  private getUserId(): Promise<number | string> {
    return new Promise((resolve, reject) => {
      if (!this.currentUser) {
        Utils.warning(`Tried to get user id, but no user is logged in`);
        return resolve("You must be logged in");
      }
      const query = `SELECT id FROM users WHERE username = ?`;
      this.db.get(query, [this.currentUser], (err, row: any) => {
        if (err || !row) reject("Error retrieving user ID");
        else resolve(row.id);
      });
    });
  }
}

export default Stocks;
