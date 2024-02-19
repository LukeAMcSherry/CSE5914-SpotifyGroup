import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './App.css';
import Header from './components/Header';
import Home from './views/Home';
import Playlist from './views/Playlist';
import Callback from './views/Callback';


function App() {

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/playlist' element={<Playlist />} />
        <Route path='/callback' element={<Callback />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
