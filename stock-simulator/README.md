# stock-simulator

This program simulates stock trades with real stock data. <br />

Inspired by the CS50 "Finance" project. Thanks to Prof. Malan and the CS50 authors/contributors for the idea and stock value API.

`./client`: Client webapp built with React and Tailwind <br/>
`./server`: Server written in Typescript, with a sqlite3 database.

## Description
Using realtime price data, this app allows you to trade stocks with a virtual portfolio.
Users can create an account with a name and password, which is hashed and stored in a sqlite database on the server.

## Description (code/logic)
- client
    - The client is a simple React application styled with Tailwind CSS and DaisyUI.
    - In its current state, the client uses JSX, but may be rewritten in TSX to match the server
- server
    - The server is split across 4 files. `index.ts` is the entrypoint where the webserver and its endpoints are established, then bound to methods which are stored separately.
    - `stocks.ts` contains a class `Stocks` which stores the auth session and methods for authentication, stock querying, and database manipulation.
    - `db.ts` contains a class `Database` which initializes and stores a connection to the sqlite database.
    - `utils.ts` just has some fancy logging functions that wrap console.log with ANSI escape codes


