import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [walletData, setWalletData] = useState([]);
  const [totalPortfolioValue, setTotalPortfolioValue] = useState(0);

  useEffect(() => {
    // Fetch data from the backend or MongoDB here
    // For the sake of this example, I'm going to use mock data

    const mockData = [
      { asset: 'BTC', balance: 1.5, value: 50000 },
      { asset: 'ETH', balance: 10, value: 2000 },
      { asset: 'NEO', balance: 50, value: 50 },

    ];

    setWalletData(mockData);
    const totalValue = mockData.reduce((acc, data) => acc + data.value, 0);
    setTotalPortfolioValue(totalValue);
  }, []);

  return (
    <div className="app">
      <h1>Wallet Balances</h1>
      <h2>Total Portfolio Value: ${totalPortfolioValue.toFixed(2)}</h2>
      <table>
        <thead>
          <tr>
            <th>Asset</th>
            <th>Balance</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {walletData.map(data => (
            <tr key={data.asset}>
              <td>{data.asset}</td>
              <td>{data.balance}</td>
              <td>${data.value.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
