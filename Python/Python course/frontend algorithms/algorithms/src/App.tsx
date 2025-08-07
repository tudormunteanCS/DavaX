import { useState } from 'react';
import './App.css';

function App() {
  const [number, setNumber] = useState<number | ''>('');
  const [result, setResult] = useState<number | string>('');
  const baseUrl = 'http://127.0.0.1:5050';
  
  const handlePow = async () => {
    if (number === '' || number < 0) return;
    try {
      console.log(`Calculating power for: ${number}`);
      const response = await fetch(`${baseUrl}/pow?number=${number}`);
      console.log(`Response: ${response}`);
      const data = await response.json();
      console.log(data);
      setResult(data.result);
    } catch (error) {
      setResult('Error computing power');
    }
  };

  const handleFibonacci = async () => {
    if (number === '' || number < 0) {
      setResult('Invalid input');
      return;
    }
    try {
      console.log(`Calculating Fibonacci for: ${number}`);
      const response = await fetch(`${baseUrl}/fib?number=${number}`);
      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      setResult('Error fetching Fibonacci');
    }
  };

  const handleFactorial = async () => {
    if (number === '' || number < 0) {
      setResult('Invalid input');
      return;
    }
    try {
      console.log(`Calculating factorial for: ${number}`);
      const response = await fetch(`${baseUrl}/fact?number=${number}`);
      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      setResult('Error fetching factorial');
    }
  };

  return (
    <div className="app-container">
      <input
        type="number"
        value={number}
        onChange={e => setNumber(e.target.value === '' ? '' : Number(e.target.value))}
        placeholder="Enter a number"
      />
      <div className="buttons">
        <button onClick={handlePow}>Power²</button>
        <button onClick={handleFibonacci}>Fibonacci</button>
        <button onClick={handleFactorial}>Factorial</button>
      </div>
      <div className="result">Result: {result}</div>
    </div>
  );
}

export default App;