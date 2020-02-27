import React from 'react';

import './App.css';

import SensorDisplay from './components/SensorDisplay';

function App() {
  return (
    <div className="App">
      <header className="App-header">Meat curing chamber monitor</header>
      <SensorDisplay></SensorDisplay>
    </div>
  );
}

export default App;
