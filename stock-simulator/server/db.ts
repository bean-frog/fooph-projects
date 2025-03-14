import sqlite3 from "sqlite3";
import Utils from "./utils.ts";

class Database {
  public db: sqlite3.Database;

  constructor() {
    this.db = new sqlite3.Database("./database.db", (err) => {
      if (err) {
        Utils.failure(`Error connecting to SQLite database: ${err.message}`);
      } else {
        Utils.success("Connected to SQLite database");
        this.initializeDatabase();
      }
    });
  }

  // Initialize database tables
  private initializeDatabase(): void {
    const createUsersTable = `
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance INTEGER NOT NULL DEFAULT 0
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
}

export default Database;
