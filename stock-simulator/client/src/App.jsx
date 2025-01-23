import React, { useState } from 'react';

function App() {
  const [symbol, setSymbol] = useState('');
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSymbolChange = (event) => {
    setSymbol(event.target.value);
  };

  const handleSearch = async () => {
    if (!symbol) {
      setError('Please enter a stock symbol');
      return;
    }

    setLoading(true);
    setError(null);
    setStockData(null);

    try {
      const response = await fetch(`http://127.0.0.1:8080/stock/${symbol.toUpperCase()}`);
      if (response.ok) {
        const data = await response.json();
        setStockData(data);
      } else {
        setError('Stock not found or error fetching data');
      }
    } catch (err) {
      setError('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-base-200">
      <div className="w-full max-w-lg p-6 bg-base-100 shadow-md rounded-lg">
        <h1 className="text-3xl font-bold text-center mb-6 text-primary">Stock Lookup</h1>

        <div className="mb-4">
          <input
            type="text"
            value={symbol}
            onChange={handleSymbolChange}
            placeholder="Enter stock symbol (e.g., AAPL)"
            className="input input-bordered w-full p-3 text-xl rounded-md border-2 border-base-300 focus:border-primary focus:outline-none"
          />
        </div>

        <div className="mb-4 flex justify-center">
          <button
            onClick={handleSearch}
            disabled={loading}
            className="btn btn-primary w-full md:w-auto"
          >
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>

        {error && <div className="alert alert-error mb-4">{error}</div>}

        {stockData && (
          <div className="mt-6 p-4 bg-base-200 border-2 border-base-300 rounded-md">
            <h2 className="text-2xl font-semibold text-center text-accent">
              {stockData.companyName} ({stockData.symbol})
            </h2>
            <p className="text-lg mt-2 text-base-content">Price: ${stockData.latestPrice}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
