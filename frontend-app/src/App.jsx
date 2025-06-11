import React, { useState, useRef } from 'react';
import Spinner from './Spinner';

export default function App() {
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');
  const [stdout, setStdout] = useState('');
  const [images, setImages] = useState([]);
  const [plotType, setPlotType] = useState('');
  const fileInputRef = useRef(null);

  const handleUpload = () => {
    const file = fileInputRef.current.files[0];
    if (!file) return;

  const allowedTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    if (!allowedTypes.includes(file.type)) {
      setStatus('Only CSV and XLSX files are allowed.');
      return;
    }

    setUploading(true);
    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('plot_type', plotType);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8000/analyze/');

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        setStatus(`Upload progress: ${percent}%`);
      }
    };

    xhr.onload = () => {
      try {
        const res = JSON.parse(xhr.responseText);
        const ws = new WebSocket(`ws://localhost:8000/ws/${res.task_id}`);

        ws.onmessage = (event) => {
          setStatus(event.data);
          if (event.data === 'Analysis complete.') {
            setUploading(false);
          }
        };

        setStdout(typeof res.stdout === 'string' ? res.stdout : JSON.stringify(res.stdout, null, 2));
        setImages(res.images);
      } catch (error) {
        setStatus("Error parsing response");
        setUploading(false);
      }
    };

    xhr.onerror = () => {
      setStatus("Upload failed");
      setUploading(false);
    };

    xhr.send(formData);
  };

  const renderStdout = () => {
    const lines = typeof stdout === 'string' ? stdout.split('\n') : [];
    return lines.map((line, idx) => (
      <pre key={idx} className="text-xs whitespace-pre-wrap font-mono mb-1">
        {line}
      </pre>
    ));
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start py-10 px-4 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6 text-center">Dataset Analysis </h1>

      <div className="w-full max-w-2xl flex flex-col items-center justify-center gap-4 mb-6">
        <input type="file" ref={fileInputRef} className="border p-2 text-sm w-full" />
        <select
          onChange={(e) => setPlotType(e.target.value)}
          className="border p-2 text-sm w-full"
        >
          <option value="">Select Plot Type</option>
          <option value="line">Line Plot</option>
          <option value="bar">Bar Chart</option>
          <option value="scatter">Scatter Plot</option>
          <option value="scatter">Histogram</option>
        </select>
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
        >
          {uploading ? 'Processing...' : 'Upload & Analyze'}
        </button>
      </div>

      <div className="mt-2 text-gray-700 text-sm text-center">
        <strong>Status:</strong> {status}
      </div>

      {uploading && (
        <div className="mt-4 flex justify-center">
          <Spinner />
        </div>
      )}

      {stdout && (
        <div className="mt-8 w-full max-w-4xl">
          <h2 className="text-lg font-semibold mb-3 border-b pb-1 text-center">Analysis Summary </h2>
          <div className="bg-white p-3 rounded shadow overflow-x-auto max-h-[400px] border text-xs">
            {renderStdout()}
          </div>
        </div>
      )}
     {images.length > 0 && (
      <div className="mt-8 w-full max-w-6xl flex flex-col items-center">
        <h2 className="text-lg font-semibold mb-3 border-b pb-1 text-center">
          Generated Plots
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6 w-full justify-items-center">
          {images.map((img, idx) => (
            <div key={idx} className="rounded overflow-hidden shadow bg-white p-2 flex justify-center">
              <img
                src={`http://localhost:8000${img}`}
                alt={`Plot ${idx}`}
                className="w-[520px] h-[420px] object-contain"
              />
            </div>
          ))}
        </div>
      </div>
    )}

    </div>
  );
}
