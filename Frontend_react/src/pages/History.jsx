import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function History() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:5001/api/history')
      .then(res => {
        setFiles(res.data.files || []);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{textAlign: 'center', padding: '4rem'}}>Loading...</div>;

  return (
    <div style={{maxWidth: '800px', margin: '0 auto', padding: '2rem'}}>
      <h2>Your Resumes</h2>
      
      {files.length === 0 ? (
        <div style={{textAlign: 'center', padding: '4rem', background: '#f5f5f5', borderRadius: '8px'}}>
          <p>No resumes yet.</p>
          <Link to="/upload" style={{color: '#667eea', fontSize: '1.1rem'}}>Create your first resume →</Link>
        </div>
      ) : (
        files.map(f => (
          <div key={f.job_id} style={{
            padding: '1.5rem',
            marginBottom: '1rem',
            background: 'white',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <strong style={{fontSize: '1.1rem'}}>{f.filename}</strong>
              <div style={{fontSize: '0.9rem', color: '#666', marginTop: '0.5rem'}}>
                {new Date(f.created * 1000).toLocaleString()} • {f.size_kb} KB
              </div>
            </div>
            <Link to={`/preview/${f.job_id}`} style={{
              padding: '0.5rem 1rem',
              background: '#667eea',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '4px'
            }}>View →</Link>
          </div>
        ))
      )}
    </div>
  );
}

export default History;
