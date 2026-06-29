import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Preview from './pages/Preview';
import Download from './pages/Download';
import History from './pages/History';
import './App.css';

function App() {
  return (
    <div className="app">
      <nav style={{background: 'white', padding: '1rem 2rem', display: 'flex', justifyContent: 'space-between'}}>
        <div><Link to="/" style={{fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea', textDecoration: 'none'}}>Taylrd</Link></div>
        <div>
          <Link to="/upload" style={{marginLeft: '1rem', color: '#555', textDecoration: 'none'}}>New Resume</Link>
          <Link to="/history" style={{marginLeft: '1rem', color: '#555', textDecoration: 'none'}}>History</Link>
        </div>
      </nav>
      
      <main style={{flex: 1, padding: '2rem'}}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/preview/:jobId" element={<Preview />} />
          <Route path="/download/:jobId" element={<Download />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </main>
      
      <footer style={{background: '#2d3748', color: 'white', textAlign: 'center', padding: '1rem'}}>
        <p>&copy; 2024 Taylrd - AI Resume Tailoring</p>
      </footer>
    </div>
  );
}

export default App;
