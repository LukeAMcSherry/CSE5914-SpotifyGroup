import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">

        Crazy? I was crazy once.
        They put me in a room.
        A rubber room.
        A rubber room with rats.
        They put me in a rubber room with rubber rats.
        Rubber rats? I hate rubber rats.
        They make me crazy.
        Crazy? I was crazy once.
        They put me in a room….

        <p>The current time is {currentTime}.</p>
      </header>
    </div>
  );
}

export default App;