import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [lyrics, setLyrics] = useState('');

  useEffect(() => {
    const getLyrics = async () => {
      try {
        const response = await fetch('/lyrics', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          // Update the song title and artist here
          body: JSON.stringify({ title: 'Believer', artist: 'Imagine Dragons' }),
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setLyrics(data.lyrics);
      } catch (error) {
        console.error('Failed to fetch lyrics:', error);
      }
    };

    getLyrics();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* Update the song title and artist in the header */}
        <h1>Lyrics for "Believer" by Imagine Dragons</h1>
        <p style={{ whiteSpace: 'pre-wrap' }}>{lyrics}</p>
      </header>
    </div>
  );
}

export default App;
