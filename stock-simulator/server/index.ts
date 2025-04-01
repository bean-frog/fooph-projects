import express, { Request, Response } from "express";
import cors from "cors";
import Stocks from "./stocks";

// express init
const app = express();
const PORT = 8080;
app.use(cors());
app.use(express.json());

const stocks = new Stocks();

// Routes

//stock info -> StockResponse
app.get("/stock/:symbol", async(req: Request, res: Response) => {
    const result = await stocks.getStockInfo(req.params.symbol)
    res.send(result)
})

// create account
app.post("/createAccount", async (req: Request, res: Response) => {
  const { name, pass } = req.body;
  const result = await stocks.createAccount(name, pass);
  res.send(result);
});

// log in
app.post("/login", async (req: Request, res: Response) => {
  const { name, pass } = req.body;
  const result = await stocks.login(name, pass);
 res.sendStatus(parseInt(result))
});

// log out
app.get("/logout", (req: Request, res: Response) => {
  const result = stocks.logout();
  res.send(result);
});

// add balance to current user 
app.post("/balance", async (req: Request, res: Response) => {
  const { amount } = req.body;
  const result = await stocks.updateBalance(amount);
  res.send(result);
});

// get balance of current user
app.get("/balance", async (req: Request, res: Response) => {
  const result = await stocks.getBalance();
  if (result.error) {
      res.status(500).json(result); // 500 server error
  } else {
      res.json(result);
  }
});

// buy stocks
app.post("/buy", async (req: Request, res: Response) => {
  const { symbol, amount } = req.body;
  const result = await stocks.buyStock(symbol, parseInt(amount));
  res.send(result);
});

// sell stocks
app.post("/sell", async (req: Request, res: Response) => {
  const { symbol, amount } = req.body;
  const result = await stocks.sellStock(symbol, parseInt(amount));
  res.send(result);
});

//get stock holdings
app.get("/getHoldings", async (req: Request, res: Response) => {
  const result = await stocks.getHoldings();
  res.send(result)
})

// ping
app.get("/ping", async (req:Request, res:Response) => {
  console.log("pinged")
  res.send("200")
})

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on http://127.0.0.1:${PORT}`);
});
