import React from 'react';
import { useParams, Link } from 'react-router-dom';

function Download() {
  const { jobId } = useParams();
  
  return (
    <div style={{maxWidth: '800px', margin: '0 auto', padding: '2rem', textAlign: 'center'}}>
      <h2>Download Your Files</h2>
      <p style={{color: '#666', marginBottom: '2rem'}}>Job ID: {jobId}</p>
      
      <div style={{display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '2rem'}}>
        <a href={`http://localhost:5001/api/download/${jobId}?type=tex`} style={{
          padding: '1.5rem 2rem',
          background: '#667eea',
          color: 'white',
          textDecoration: 'none',
          borderRadius: '8px',
          fontSize: '1.1rem'
        }}>📄 Download .tex (Source)</a>
        
        <a href={`http://localhost:5001/api/download/${jobId}?type=pdf`} style={{
          padding: '1.5rem 2rem',
          background: '#48bb78',
          color: 'white',
          textDecoration: 'none',
          borderRadius: '8px',
          fontSize: '1.1rem'
        }}>📑 Download PDF</a>
      </div>
      
      <div style={{marginTop: '2rem'}}>
        <Link to="/upload" style={{
          padding: '1rem 2rem',
          background: '#edf2f7',
          color: '#667eea',
          textDecoration: 'none',
          borderRadius: '8px',
          display: 'inline-block'
        }}>+ Create Another Resume</Link>
      </div>
    </div>
  );
}

export default Download;
