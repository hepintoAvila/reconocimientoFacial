import React, { useState } from 'react';
import './App.css';

function App() {
    const [name, setName] = useState('');

    const handleNameChange = (event) => {
        setName(event.target.value);
    };

    const runScript = (script, params = {}) => {
        fetch(`http://localhost:5000/run/${script}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params),
        })
            .then(response => response.text())
            .then(result => alert(result))
            .catch(error => alert('Error executing script'));
    };

    const handleCaptureImages = () => {
        if (!name) {
            alert('Please enter your name.');
            return;
        }
        runScript('capture_images.py', { name });
    };

    return (
        <div className="App">
            <h1>Facial Recognition System</h1>
            <div>
                <input
                    type="text"
                    placeholder="Enter your name"
                    value={name}
                    onChange={handleNameChange}
                />
                <button onClick={handleCaptureImages}>Capture Images</button>
                <button onClick={() => runScript('train_model.py')}>Train Model</button>
                <button onClick={() => runScript('recognize_faces.py')}>Recognize Faces</button>
            </div>
            <div className="video-container">
                <h2>Video Feed</h2>
                <img src="http://localhost:5001/video_feed" alt="Video Feed" />
            </div>
        </div>
    );
}

export default App;
