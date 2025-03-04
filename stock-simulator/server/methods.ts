import axios from "axios";
import sqlite3 from "sqlite3";
import bcrypt from "bcrypt";
import { open } from "sqlite";
import Utils from './utils.ts'

// CS50 stock api response type
interface StockResponse {
  companyName: string;
  latestPrice: number;
  symbol: string;
}

// stock holding type (from db)
interface Holding {
  symbol: string,
  amount: number
}

class Stocks {
  private db: sqlite3.Database;
  private currentUser: string | null = null; // Tracks the logged-in user

  constructor() {
    this.db = new sqlite3.Database("./database.db", (err) => {
      if (err) {
        Utils.failure(`Error connecting to SQLite database: ${err.message}`)
      } else {
        Utils.success("Connected to SQLite database")
        this.initializeDatabase();
      }
    })
  }
  // Initialize database tables
  private initializeDatabase(): void {
    const createUsersTable = `
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance INTEGER DEFAULT 0
      )
    `;
    const createStocksTable = `
      CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        amount INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
      )
    `;
    this.db.run(createUsersTable);
    this.db.run(createStocksTable);
  }
  // check stock info
  public async getStockInfo(symbol: string):Promise<StockResponse | string> {
    const url = `https://finance.cs50.io/quote?symbol=${symbol.toUpperCase()}`
    try {
        const response = await axios.get<StockResponse>(url);
        Utils.success(`Found data for ${symbol.toUpperCase()}`)
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            if (error.response.status === 404) {
                Utils.warning(`Stock with symbol ${symbol} not found.`)
                return `Stock with symbol ${symbol} not found`;
            } else {
                Utils.failure(`Error fetching stock data: ${error}`)
                return `Error fetching stock data: ${error}`
            }
            
        } else {
            Utils.failure(`Unknown error occurred while fetching stock data: ${error}`)
            return `Unknown error occurred while fetchin stock data: ${error}`
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
            Utils.warning(`Tried to create account ${name} but username already exists.`)
            resolve("Username already exists");
          } else {
            Utils.failure(`Unable to create account for an unknown reason.`)
            reject("Error creating account");
          }
        } else {
          Utils.success(`Created account with name ${name}.`)
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
          Utils.warning(`Invalid username or password (name: ${name})`)
          resolve("401"); // 401 Unauthorized
        } else {
          const validPassword = await bcrypt.compare(pass, row.password);
          if (validPassword) {
            this.currentUser = name;
            Utils.success(`${name} logged in`)
            resolve("200"); // 200 OK
          } else {
            Utils.warning(`Invalid username or password (name: ${name})`)
            resolve("500"); // 500 Server Error
          }
        }
      });
    });
  }

  // Log out

  public logout(): string {
    if (!this.currentUser) {
        Utils.warning(`Received logout request, but no user is logged in`)
        return "You must be logged in";
    }
      let tempUserRef: any = this.currentUser;
      this.currentUser = null;
      Utils.success(`${tempUserRef} logged out`)
      return "Logged out successfully";

  }

  // Update balance
  public async updateBalance(amount: number): Promise<string> {
    if (!this.currentUser) {
        Utils.warning(`Received balance update request, but no user is logged in`)
        return "You must be logged in";
    }
    return new Promise((resolve, reject) => {
      const query = `UPDATE users SET balance = balance + ? WHERE username = ?`;
      this.db.run(query, [amount, this.currentUser], (err) => {
        if (err) {
            Utils.failure(`Error updating balance of ${this.currentUser}: ${err}`)
            reject("Error updating balance");
        } 
        else{
            Utils.success(`Added ${amount} to balance of ${this.currentUser}`)
            resolve("Balance updated");
        } 
      });
    })
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
  
    // Check if symbol is valid and get the price
    let stockData: StockResponse;
    try {
      const response = await axios.get<StockResponse>(`https://finance.cs50.io/quote?symbol=${symbol.toUpperCase()}`);
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
  
    const userId = await this.getUserId();
    if (typeof userId === "string") return userId; 
  
    // Retrieve user's current balance
    try {
      const balanceQuery = `SELECT balance FROM users WHERE id = ?`;
      const balance = await new Promise<number>((resolve, reject) => {
        this.db.get(balanceQuery, [userId], (err, row: any) => {
          if (err) {
          	Utils.failure(`Failed to retrieve user balance:  ${err.message}`)
            reject(`Failed to retrieve user balance: ${err.message}`);
          } else {
            resolve(row?.balance ?? 0);
          }
        });
      });
  
      if (balance < totalCost) {
        Utils.warning(`User ${userId} cannot afford ${amount} shares of ${symbol} at $${price} each.`);
        return Promise.reject(`You cannot afford ${amount} shares of ${symbol}`);
      }
  
      // Deduct the cost from user's balance
      const updateBalanceQuery = `UPDATE users SET balance = balance - ? WHERE id = ?`;
      await new Promise<void>((resolve, reject) => {
        this.db.run(updateBalanceQuery, [totalCost, userId], (err) => {
          if (err) {
          	Utils.failure(`Failed to update user balance: ${err.message}`)
            reject(`Failed to update user balance: ${err.message}`);
          } else {
            resolve();
          }
        });
      });
  
      // Add or update the stock entry
      const stockQuery = `
        INSERT INTO stocks (user_id, symbol, amount)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, symbol)
        DO UPDATE SET amount = amount + excluded.amount
      `;
      await new Promise<void>((resolve, reject) => {
        this.db.run(stockQuery, [userId, symbol, amount], (err) => {
          if (err) {
          	Utils.failure(`Failed to update stock records: ${err.message}`)
            reject(`Failed to update stock records: ${err.message}`);
          } else {
            resolve();
          }
        });
      });
  
      return `Bought ${amount} shares of ${symbol} at $${price} each for a total of $${totalCost.toFixed(2)}`;
    } catch (error) {
      Utils.failure(`Error processing stock purchase: ${error}`);
      return Promise.reject(`Error buying stock: ${error}`);
    }
  }

  // Sell stocks
  public async sellStock(symbol: string, amount: number): Promise<string> {
    if (!this.currentUser) {
        Utils.warning(`Received stock sale request, but no user is logged in`)
        return "You must be logged in";
    }
    const userId = await this.getUserId();
    if (typeof userId === "string") return userId; // Error case

    return new Promise((resolve, reject) => {
      const query = `
        UPDATE stocks
        SET amount = amount - ?
        WHERE user_id = ? AND symbol = ? AND amount >= ?
      `;
      this.db.run(query, [amount, userId, symbol, amount], (err) => {
        if (err) reject("Error selling stock");
        else resolve(`Sold ${amount} of ${symbol}`);
      });
    });
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
            Utils.warning(`Tried to get user id, but no user is logged in`)
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
