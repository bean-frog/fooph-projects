import React, { useState } from 'react'
import axios from 'axios'
import { useEffect } from 'react'
import { themeChange } from 'theme-change'
import { BrowserRouter as Router, Routes, Link, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Login from './components/Login'
import Register from './components/Register'
import Home from './components/Home'

const OldApp = () => {
  useEffect(() => {
    themeChange(false)
  }, [])

  const [message, setMessage] = useState('') // General message display
  const [balance, setBalance] = useState(null) // Display balance

  const handleResponse = (res) => {
    setMessage(res.data || 'Operation successful')
  }

  const handleError = (err) => {
    setMessage(err.response?.data || 'Something went wrong')
  }

  // API endpoints
  const api = axios.create({
    baseURL: 'http://127.0.0.1:8080',
  })

  return (
    <div className="p-5 min-h-screen bg-base-100">
      <h1 className="mb-5 text-3xl font-bold text-center text-primary">
        Endpoint Test
      </h1>
      <select data-choose-theme>
        <option value="sunset">Sunset(Default)</option>
        <option value="dark">Dark</option>
        <option value="synthwave">Synthwave</option>
        <option value="black">Black</option>
        <option value="pastel">Pastel</option>
        <option value="luxury">Luxury</option>
        <option value="nord">Nord</option>
      </select>
      {/* Parent container with flex-wrap */}
      <div className="flex flex-wrap gap-4 justify-center">
        {/* Shared message */}
        <div className="mb-4 w-full text-center">
          <div className="alert alert-info">{message}</div>
        </div>
        {/* Check stock info */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Get Stock Info</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              const { symbol } = e.target.elements
              try {
                const res = await api.get(`/stock/${symbol.value}`) // Corrected: Pass `symbol` in the URL
                setMessage(res.data.latestPrice)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <input
              required
              type="text"
              name="symbol"
              placeholder="Symbol"
              className="mb-2 w-full input input-bordered"
            />
            <button className="w-full btn btn-primary">Submit</button>
          </form>
        </section>
        {/* Create Account */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Create Account</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              const { name, pass } = e.target.elements
              try {
                const res = await api.post('/createAccount', {
                  name: name.value,
                  pass: pass.value,
                })
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <input
              required
              type="text"
              name="name"
              placeholder="Username"
              className="mb-2 w-full input input-bordered"
            />
            <input
              required
              type="password"
              name="pass"
              placeholder="Password"
              className="mb-2 w-full input input-bordered"
            />
            <button className="w-full btn btn-primary">Create Account</button>
          </form>
        </section>

        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">get holdings</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              try {
                const res = await api.get('/getHoldings')
                console.log(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <button className="w-full btn btn-accent">get holdings</button>
          </form>
        </section>
        {/* Login */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Login</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              const { name, pass } = e.target.elements
              try {
                const res = await api.post('/login', {
                  name: name.value,
                  pass: pass.value,
                })
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <input
              required
              type="text"
              name="name"
              placeholder="Username"
              className="mb-2 w-full input input-bordered"
            />
            <input
              required
              type="password"
              name="pass"
              placeholder="Password"
              className="mb-2 w-full input input-bordered"
            />
            <button className="w-full btn btn-accent">Login</button>
          </form>
        </section>

        {/* Logout */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Logout</h2>
          <button
            className="w-full btn btn-warning"
            onClick={async () => {
              try {
                const res = await api.get('/logout')
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            Logout
          </button>
        </section>

        {/* Balance */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Manage Balance</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              const { amount } = e.target.elements
              try {
                const res = await api.post('/balance', {
                  amount: parseInt(amount.value),
                })
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <input
              required
              type="number"
              name="amount"
              placeholder="Amount"
              className="mb-2 w-full input input-bordered"
            />
            <button className="mb-2 w-full btn btn-success">
              Update Balance
            </button>
          </form>
          <button
            className="w-full btn btn-info"
            onClick={async () => {
              try {
                const res = await api.get('/balance')
                setBalance(res.data)
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            View Balance
          </button>
          {balance !== null && (
            <p className="mt-2 text-center">Balance: ${balance}</p>
          )}
        </section>

        {/* Buy Stocks */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Buy Stocks</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              const { symbol, amount } = e.target.elements
              try {
                const res = await api.post('/buy', {
                  symbol: symbol.value,
                  amount: parseInt(amount.value),
                })
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <input
              required
              type="text"
              name="symbol"
              placeholder="Stock Symbol"
              className="mb-2 w-full input input-bordered"
            />
            <input
              required
              type="number"
              name="amount"
              placeholder="Amount"
              className="mb-2 w-full input input-bordered"
            />
            <button className="w-full btn btn-primary">Buy</button>
          </form>
        </section>

        {/* Sell Stocks */}
        <section className="flex-1 min-w-[300px] p-4 border border-base-300 rounded-lg bg-neutral text-neutral-content">
          <h2 className="mb-2 text-xl font-bold">Sell Stocks</h2>
          <form
            onSubmit={async (e) => {
              e.preventDefault()
              const { symbol, amount } = e.target.elements
              try {
                const res = await api.post('/sell', {
                  symbol: symbol.value,
                  amount: parseInt(amount.value),
                })
                handleResponse(res)
              } catch (err) {
                handleError(err)
              }
            }}
          >
            <input
              required
              type="text"
              name="symbol"
              placeholder="Stock Symbol"
              className="mb-2 w-full input input-bordered"
            />
            <input
              required
              type="number"
              name="amount"
              placeholder="Amount"
              className="mb-2 w-full input input-bordered"
            />
            <button className="w-full btn btn-secondary">Sell</button>
          </form>
        </section>
      </div>
    </div>
  )
}

export default OldApp
