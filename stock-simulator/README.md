# stock-simulator

This program simulates stock trades with real stock data.

`./client`: Client webapp built with React and Tailwind <br/>
`./server`: Server written in Rust, with a sqlite3 database.

## Description
Using realtime price data from Yahoo, this app allows you to trade stocks with a virtual portfolio.
Users can create an account with a name and password, which is hashed and stored in a sqlite database on the server.
