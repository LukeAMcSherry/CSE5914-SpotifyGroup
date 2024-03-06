import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './App.css';
import Header from './components/Header';
import Home from './views/Home';
import FollowArtist from './views/FollowArtist';
import Callback from './views/Callback';
import Playlist from './views/Playlist';


function App() {

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/follow-artist' element={<FollowArtist />} />
        <Route path='/callback' element={<Callback />} />
        <Route path='/playlist' element={<Playlist />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
