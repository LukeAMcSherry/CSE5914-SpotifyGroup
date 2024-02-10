import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Auth from "./Auth";
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
    <BrowserRouter>

      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Crazy? I was crazy once.
            They put me in a room.
            A rubber room.
            A rubber room with rats.
            They put me in a rubber room with rubber rats.
            Rubber rats? I hate rubber rats.
            They make me crazy.
            Crazy? I was crazy once.
            They put me in a room….
          </p>
          <p>The currentTime is {currentTime}</p>
          <Routes>
            <Route path='/spotify' element={<Auth />}></Route>
          </Routes>
        </header>
      </div>
    </BrowserRouter>
  );
}

export default App;
