import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

function Preview() {
  const { jobId } = useParams();
  const [latex, setLatex] = useState('Loading...');
  const [pdfUrl, setPdfUrl] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`http://localhost:5001/api/latex/${jobId}`)
      .then(res => {
        if (res.data.latex) {
          setLatex(res.data.latex);
        } else {
          setLatex('Error: No LaTeX content found');
        }
      })
      .catch(err => {
        setLatex('Error fetching LaTeX: ' + err.message);
      });
  }, [jobId]);

  const generatePDF = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`http://localhost:5001/api/generate-pdf/${jobId}`);
      if (res.data.success) {
        setPdfUrl(res.data.pdf_url);
      } else {
        alert('PDF generation failed: ' + (res.data.error || 'Unknown error'));
      }
    } catch (err) {
      alert('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{maxWidth: '1000px', margin: '0 auto', padding: '2rem'}}>
      <h2>Preview Resume</h2>
      <p>Job ID: {jobId}</p>
      
      <div style={{
        background: '#1a202c', 
        color: '#e2e8f0', 
        padding: '1rem', 
        borderRadius: '8px', 
        marginBottom: '1rem',
        maxHeight: '400px',
        overflow: 'auto'
      }}>
        <pre style={{margin: 0, fontSize: '0.8rem', whiteSpace: 'pre-wrap'}}>{latex}</pre>
      </div>
      
      <div style={{marginTop: '1rem'}}>
        {pdfUrl ? (
          <div>
            <a href={pdfUrl} download style={{
              padding: '1rem 2rem',
              background: '#48bb78',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '8px',
              marginRight: '1rem',
              display: 'inline-block'
            }}>Download PDF</a>
            <iframe src={pdfUrl} style={{width: '100%', height: '500px', marginTop: '1rem'}} title="PDF Preview" />
          </div>
        ) : (
          <button onClick={generatePDF} disabled={loading} style={{
            padding: '1rem 2rem',
            background: loading ? '#ccc' : '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            marginRight: '1rem',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}>
            {loading ? 'Generating PDF...' : 'Generate PDF'}
          </button>
        )}
        
        <Link to={`/download/${jobId}`} style={{
          padding: '1rem 2rem',
          background: '#718096',
          color: 'white',
          textDecoration: 'none',
          borderRadius: '8px',
          display: 'inline-block'
        }}>Continue to Download →</Link>
      </div>
    </div>
  );
}

export default Preview;
