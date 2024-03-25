import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './App.css';
import Header from './components/Header';
import Home from './views/Home';
import Playlist from './views/Playlist';
import Callback from './views/Callback';
import Features from './views/Features';
import About from './views/About';




function App() {

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/playlist' element={<Playlist />} />
        <Route path='/callback' element={<Callback />} />
        <Route path='/features' element={<Features />} />
        <Route path='/about' element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
