import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Upload() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !jobDesc) {
      setError('Please provide both resume and job description');
      return;
    }
    
    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDesc);

    try {
      const res = await axios.post('http://localhost:5001/api/upload', formData);
      if (res.data.success) {
        navigate(`/preview/${res.data.job_id}`);
      } else {
        setError(res.data.error || 'Upload failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{maxWidth: '800px', margin: '0 auto'}}>
      <h2>Create Tailored Resume</h2>
      {error && <div style={{color: 'red', padding: '1rem', background: '#fee', borderRadius: '8px', marginBottom: '1rem'}}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div style={{marginBottom: '1rem'}}>
          <label style={{display: 'block', marginBottom: '0.5rem', fontWeight: 'bold'}}>Resume File</label>
          <input type="file" accept=".pdf,.docx,.txt" onChange={(e) => setFile(e.target.files[0])} required />
        </div>
        
        <div style={{marginBottom: '1rem'}}>
          <label style={{display: 'block', marginBottom: '0.5rem', fontWeight: 'bold'}}>Job Description</label>
          <textarea 
            value={jobDesc} 
            onChange={(e) => setJobDesc(e.target.value)}
            placeholder="Paste the job description here..."
            rows="10"
            style={{width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ddd'}}
            required
          />
        </div>
        
        <button type="submit" disabled={loading} style={{
          padding: '1rem 2rem',
          background: loading ? '#ccc' : '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          fontSize: '1rem',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}>
          {loading ? 'Processing...' : 'Generate Resume'}
        </button>
      </form>
    </div>
  );
}

export default Upload;
