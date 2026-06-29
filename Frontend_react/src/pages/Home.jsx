import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div style={{textAlign: 'center', padding: '4rem'}}>
      <h1 style={{fontSize: '4rem', color: '#667eea', marginBottom: '1rem'}}>Taylrd</h1>
      <p style={{fontSize: '1.5rem', color: '#666'}}>AI-Powered Resume Generator</p>
      <Link to="/upload" style={{
        display: 'inline-block',
        marginTop: '2rem',
        padding: '1rem 2rem',
        background: '#667eea',
        color: 'white',
        textDecoration: 'none',
        borderRadius: '25px',
        fontSize: '1.2rem'
      }}>Get Started</Link>
    </div>
  );
}

export default Home;
