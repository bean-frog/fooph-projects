import { Link } from 'react-router'
import { useState, useEffect } from 'react'

const Dashboard = ({ auth, api }) => {
  const [balance, setBalance] = useState(0)
  const [holdingValue, setHoldingValue] = useState(0)
  const [holdings, setHoldings] = useState([])
  const [error, setError] = useState(null)
  const [priceResult, setPriceResult] = useState(null)
  const [stockCheckAmount, setSCA] = useState(1)

  // Fetch balance from backend
  const fetchBalance = async () => {
    try {
      const response = await api.get('/balance')
      const fetchedBalance =
        response.data.balance == null ? 0 : response.data.balance
      setBalance(fetchedBalance)
    } catch (err) {
      setError('Failed to fetch balance')
      console.error(err)
    }
  }

  // Fetch holdings and calculate their total value.
  const fetchHoldings = async () => {
    try {
      const response = await api.get('/getHoldings')
      const holdingsList = response.data || []
      // Use Promise.all to fetch latest prices for each holding concurrently.
      const updatedHoldings = await Promise.all(
        holdingsList.map(async (item) => {
          const priceRes = await api.get(`/stock/${item.symbol}`)
          const latestPrice = priceRes.data.latestPrice
          return {
            ...item,
            latestPrice,
            value: item.amount * latestPrice,
          }
        })
      )
      // Sum up total holding value.
      const totalValue = updatedHoldings.reduce(
        (acc, curr) => acc + curr.value,
        0
      )
      setHoldings(updatedHoldings)
      setHoldingValue(totalValue)
    } catch (err) {
      console.error(err)
    }
  }

  // Call the data fetching functions on component mount.
  useEffect(() => {
    fetchBalance()
    fetchHoldings()
  }, [])

  // Refresh both balance and holdings
  const refreshData = async () => {
    await fetchBalance()
    await fetchHoldings()
  }

  return (
    <div className="flex flex-col justify-center items-center p-4 w-screen min-h-screen bg-base-200">
      {auth ? (
        <div className="w-full">
          <div className="flex flex-col gap-4 lg:flex-row">
            {/* Left Panel: Stats & Actions */}
            <div className="flex flex-col gap-4 w-full lg:w-1/2">
              {/* Stats */}
              <div className="flex flex-col gap-4 lg:flex-row">
                <div className="rounded-md border shadow stats border-primary">
                  <div className="stat">
                    <div className="stat-title text-secondary">Balance</div>
                    <div className="stat-value">${balance.toFixed(2)}</div>
                  </div>
                 
                </div>

                <div className="rounded-md border shadow stats border-primary">
                  <div className="stat">
                    <div className="stat-title text-secondary">
                      Value of Holdings
                    </div>
                    <div className="stat-value">${holdingValue.toFixed(2)}</div>
                  </div>
                </div>

                <div className="rounded-md border shadow stats border-primary">
                  <div className="stat">
                    <div className="stat-title text-secondary">Add to balance</div>
                    <div className="flex flex-row space-x-2">
                    {[100, 1000, 10000].map((amount) => (
                      <button
                        key={amount}
                        className="btn btn-sm btn-primary"
                        onClick={async () => {
                          try {
                            await api.post('/balance', { amount })
                            console.log(`Added $${amount} to balance`)
                          } catch (error) {
                            console.error('Failed to update balance:', error)
                          }
                          await refreshData()
                        }}
                      >
                        ${amount}
                      </button>
                    ))}
                    </div>
                  </div>
                </div>

              </div>

              {/* Check Stock Price */}
              <div className="p-4 rounded-md border shadow-md card bg-base-100 border-primary">
                <h2 className="mb-4 text-xl font-bold card-title text-secondary">
                  Check Stock Price
                </h2>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault()
                    const { symbol, amount } = e.target.elements
                    try {
                      const res = await api.get(`/stock/${symbol.value}`)
                      setPriceResult(res.data)
                      setSCA(amount.value || 1)
                    } catch (err) {
                      console.error(err)
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
                    type="number"
                    name="amount"
                    placeholder="Amount"
                    className="mb-2 w-full input input-bordered"
                    defaultValue={1}
                  />
                  {priceResult && (
                    <div className="mb-2">
                      <h3 className="text-xl font-bold text-primary">
                        {priceResult.companyName}
                      </h3>
                      <p className="text-secondary">
                        $
                        {(priceResult.latestPrice * stockCheckAmount).toFixed(
                          2
                        )}
                      </p>
                    </div>
                  )}
                  <button type="submit" className="w-full btn btn-primary">
                    Check Price
                  </button>
                </form>
              </div>

              {/* Buy Stocks */}
              <div className="p-4 rounded-md border shadow-md card bg-base-100 border-primary">
                <h2 className="mb-4 text-xl font-bold card-title text-secondary">
                  Buy Stocks
                </h2>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault()
                    const { symbol, amount } = e.target.elements
                    try {
                      await api.post('/buy', {
                        symbol: symbol.value,
                        amount: parseInt(amount.value),
                      })
                      await refreshData()
                    } catch (err) {
                      console.error(err)
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
                  <button type="submit" className="w-full btn btn-primary">
                    Buy
                  </button>
                </form>
              </div>

              {/* Sell Stocks */}
              <div className="p-4 rounded-md border shadow-md card bg-base-100 border-primary">
                <h2 className="mb-4 text-xl font-bold card-title text-secondary">
                  Sell Stocks
                </h2>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault()
                    const { symbol, amount } = e.target.elements
                    try {
                      await api.post('/sell', {
                        symbol: symbol.value,
                        amount: parseInt(amount.value),
                      })
                      await refreshData()
                    } catch (err) {
                      console.error(err)
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
                  <button type="submit" className="w-full btn btn-primary">
                    Sell
                  </button>
                </form>
              </div>
            </div>

            {/* Right Panel: Holdings List */}
            <div className="w-full lg:w-1/2">
              <div className="p-4 rounded-md border shadow-md card bg-base-100 border-primary">
                <h2 className="mb-4 text-xl font-bold card-title text-secondary">
                  Your Holdings
                </h2>
                {holdings.length === 0 ? (
                  <p className="text-neutral">No holdings to display.</p>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="table w-full">
                      <thead>
                        <tr>
                          <th>Symbol</th>
                          <th>Amount</th>
                          <th>Price</th>
                          <th>Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        {holdings.map((item) => (
                          <tr key={item.symbol}>
                            <td>{item.symbol}</td>
                            <td>{item.amount}</td>
                            <td>${item.latestPrice.toFixed(2)}</td>
                            <td>${item.value.toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </div>
          {error && (
            <div className="mt-4 shadow-lg alert alert-error">
              <div>{error}</div>
            </div>
          )}
        </div>
      ) : (
        <div className="min-h-screen hero bg-base-200">
          <div className="text-center hero-content">
            <div className="max-w-md">
              <h1 className="text-3xl font-bold">Uh oh!</h1>
              <p className="py-6">
                You're trying to access the dashboard, but no user is logged in.
              </p>
              <Link to="/" className="btn btn-primary">
                Back to Login
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
