import { Link } from 'react-router'
import { useState, useEffect } from 'react'
const Dashboard = ({ auth, api }) => {
  const [balance, setBalance] = useState(0)
  const [holdingValue, setHoldingValue] = useState(0)
  const [error, setError] = useState(null)
  const [priceResult, setPriceResult] = useState(0)
  const [stockCheckAmount, setSCA] = useState(1)
  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await api.get('/balance')
        if (
          response.data.balance !== null ||
          response.data.balance !== undefined
        ) {
          setBalance(response.data.balance)
        } else {
          setBalance(0)
        }
      } catch (err) {
        setError('Failed to fetch balance')
        console.error(err)
      }
    }
    const getHoldingValue = async() => {
      try {
        const response = await api.get('/getHoldings')
        response.data.forEach( async item => {
          const priceRes = await api.get(`/stock/${item.symbol}`)
          const price = priceRes.data.balance
          setHoldingValue(holdingValue + (item.amount * price))
        });
      } catch (err) {
        console.error(err)
      }
    }
    fetchBalance()
    getHoldingValue()
  }, [])
  return (
    <div className="flex flex-col justify-center items-center w-screen h-screen">
      {auth ? (
        <div className="flex flex-row justify-center items-center w-screen h-full">
          <div className="flex flex-col w-1/2 h-full">
            <div className="flex flex-col items-center mt-12 w-full h-2/5 border-r-2 border-b border-solid border-primary">
              <div className="flex flex-col gap-4 justify-center items-center mt-4 w-full h-full">
                <div className="rounded-md border shadow stats border-primary">
                  <div className="stat">
                    <div className="stat-title text-secondary">Balance</div>
                    <div className="stat-value">${balance == null ? "0.00" : balance.toFixed(2)}</div>
                  </div>
                </div>
                <div className="rounded-md border shadow stats border-primary">
                  <div className="stat">
                    <div className="stat-title text-secondary">
                      Value of holdings
                    </div>
                    <div className="stat-value">${holdingValue.toFixed(2)}</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex flex-col justify-center w-full h-full border-t border-r-2 border-solid border-primary">
              <section className="flex-1 min-w-[300px] p-4 text-neutral-content">
                <h2 className="mb-2 text-xl font-bold">Check stock price</h2>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault()
                    const { symbol, amount } = e.target.elements
                    try {
                      const res = await api.get(`/stock/${symbol.value}`, {
                        symbol: symbol.value,
                      })
                      setPriceResult(res.data)
                      setSCA(amount.value)
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
                    placeholder="1"
                    className="mb-2 w-full input input-bordered"
                  />
                  {priceResult !== 0 ? (
                    <>
                      <h1 className="text-xl font-bold text-primary">
                        {priceResult.companyName}
                      </h1>
                      <h1 className="text-xl text-secondary">
                        $
                        {(priceResult.latestPrice * stockCheckAmount).toFixed(
                          2
                        )}
                      </h1>
                    </>
                  ) : null}
                  <button className="w-full btn btn-primary">
                    Check Price
                  </button>
                </form>
              </section>
              <div className="flex flex-row justify-center items-center w-full h-full">
                <section className="flex-1 min-w-[300px] p-4 text-neutral-content">
                  <h2 className="mb-2 text-xl font-bold">Buy Stocks</h2>
                  <form
                    onSubmit={async (e) => {
                      e.preventDefault()
                      const { symbol, amount } = e.target.elements
                      try {
                        const res = await api.post('/buy', {
                          symbol: symbol.value,
                        })
                        console.log(res)
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
                    <button className="w-full btn btn-primary">Buy</button>
                  </form>
                </section>

                {/* Sell Stocks */}
                <section className="flex-1 min-w-[300px] p-4 text-neutral-content">
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
                        console.log(res)
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
                    <button className="w-full btn btn-primary">Sell</button>
                  </form>
                </section>
              </div>
            </div>
          </div>
          <div className="flex flex-col justify-center items-center w-1/2 h-full">
            holdings
          </div>
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
