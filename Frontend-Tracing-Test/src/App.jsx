import { useState } from 'react'
import Dashboard from './components/Dashboard/Dashboard';
import NetworkPanel from './components/NetworkPanel/NetworkPanel';
import AsyncPanel from './components/AsyncPanel/AsyncPanel';
import './App.css'

function App() {
  const [status, setStatus] = useState('System Standby');
  const [isGlowing, setGlowing] = useState(false);

  // Function 1: Magic Glow - Visual change
  const handleMagicGlow = () => {
    setGlowing(!isGlowing);
    setStatus(!isGlowing ? 'Glow Activated' : 'Glow Deactivated');
  };

  // Function 2: Data Stream - Async simulation
  const handleDataStream = () => {
    setStatus('Initializing Stream...');
    setTimeout(() => {
      setStatus('Stream Active: Decoding packets...');
      setTimeout(() => {
        setStatus('Data Stream Connected [Secure]');
      }, 1500);
    }, 1000);
  };

  // Function 3: System Alert - Instant feedback
  const handleSystemAlert = () => {
    const alerts = ['Breach Detected', 'Updates Available', 'Battery Low', 'Network Error'];
    const randomAlert = alerts[Math.floor(Math.random() * alerts.length)];
    setStatus(`ALERT: ${randomAlert}`);
  };

  // Function 4: Pulse Check - Diagnostic
  const handlePulseCheck = () => {
    setStatus('Running Diagnostics...');
    let pulseCount = 0;
    const interval = setInterval(() => {
      pulseCount++;
      setStatus(`Pulse Check: ${pulseCount}/3 passed`);
      if (pulseCount >= 3) {
        clearInterval(interval);
        setStatus('System Healthy. All Systems Go.');
      }
    }, 800);
  };

  return (
    <main className={`glass-card ${isGlowing ? 'glow-active' : ''}`} style={{
      boxShadow: isGlowing ? '0 0 50px var(--primary-glow)' : ''
    }}>
      <h1 className="title">Control Deck</h1>
      <p className="subtitle">Interactive React Interface</p>

      <div className="button-grid">
        <button className="btn-premium" onClick={handleMagicGlow}>
          <span>✨</span> Toggle Glow
        </button>

        <button className="btn-premium" onClick={handleDataStream}>
          <span>📡</span> Connect Stream
        </button>

        <button className="btn-premium" onClick={handleSystemAlert}>
          <span>⚠️</span> System Alert
        </button>

        <button className="btn-premium" onClick={handlePulseCheck}>
          <span>❤️</span> Pulse Check
        </button>
      </div>

      <div className="feedback-area">
        {status}
      </div>

      <Dashboard />
      <NetworkPanel />
      <AsyncPanel />
    </main>
  )
}

export default App
