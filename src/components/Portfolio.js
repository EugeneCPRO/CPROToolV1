import React, { useState, useEffect } from 'react';

function Portfolio() {
  const [portfolioData, setPortfolioData] = useState([]);
  const [totalValue, setTotalValue] = useState('Unknown');

  useEffect(() => {
    // Replace this with code to fetch data from your backend
    // Example:
    fetch('/api/portfolio')
      .then((response) => response.json())
      .then((data) => {
        setPortfolioData(data);
        // Calculate and set total portfolio value
        const total = data.reduce((acc, item) => acc + item.value, 0);
        setTotalValue(formatValue(total));
      });
  }, []);

  const formatValue = (value) => {
    if (typeof value === 'number') {
      return `$${value.toFixed(2)}`;
    } else {
      return 'Unknown';
    }
  };

  return (
    <div>
      <h2>Total Portfolio Value: {totalValue}</h2>
      <table>
        <thead>
          <tr>
            <th>Asset</th>
            <th>Balance</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {portfolioData.map((item, index) => (
            <tr key={index}>
              <td>{item.asset}</td>
              <td>{item.balance}</td>
              <td>{formatValue(item.value)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Portfolio;
