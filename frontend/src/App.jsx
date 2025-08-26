import { useState, useEffect } from 'react';

// This is the main component for our application
function App() {
  // We create "state" variables to hold our data.
  // When these change, the component will automatically re-render.
  const [analysisData, setAnalysisData] = useState(null); // Will hold the data from the backend
  const [isLoading, setIsLoading] = useState(true);      // True while we are fetching data
  const [error, setError] = useState(null);              // Will hold any error message

  // This "useEffect" hook is a special function that runs after the component is first rendered.
  // It's the perfect place to fetch data.
  useEffect(() => {
    const getAnalysis = async () => {
      try {
        // Fetch data from the backend server running on localhost:5000
        const response = await fetch('http://127.0.0.1:5000/api/analyze', {
          method: 'POST', // Use a POST request as defined in our backend
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setAnalysisData(data); // Success! Save the data to our state.
      } catch (e) {
        setError(e.message); // If an error occurs, save the error message.
      } finally {
        setIsLoading(false); // Whether it succeeded or failed, we are done loading.
      }
    };

    getAnalysis(); // Call the function to start the data fetching process.
  }, []); // The empty array [] tells React to run this effect only once.

  // --- This is the JSX that defines what the user sees ---

  // 1. If we are still loading, show a simple message.
  if (isLoading) {
    return <div>Loading Analysis...</div>;
  }

  // 2. If an error occurred, show the error message.
  if (error) {
    return <div>Error fetching data: {error}</div>;
  }

  // 3. If loading is finished and there's no error, display the data.
  return (
    <div>
      <h1>CertifyAI Document Analysis</h1>

      <h2>Health Score: {analysisData.healthScore}/100</h2>

      <div>
        <h3>Summary</h3>
        <p><strong>Parties:</strong> {analysisData.summary.parties}</p>
        <p><strong>Agreement Type:</strong> {analysisData.summary.agreementType}</p>
        <p><strong>Key Dates:</strong> {analysisData.summary.keyDates}</p>
        <p><strong>Financials:</strong> {analysisData.summary.financials}</p>
      </div>

      <div>
        <h3>Action Items</h3>
        <ul>
          {analysisData.actionItems.map((item, index) => (
            <li key={index}>
              <strong>{item.risk}:</strong> {item.text}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;