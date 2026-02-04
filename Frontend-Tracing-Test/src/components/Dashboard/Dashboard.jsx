import { useState, memo } from 'react';
import './Dashboard.css';

function Dashboard() {
    const [metrics, setMetrics] = useState({
        cpu: 45,
        memory: 62,
        network: 12
    });
    const [lastAction, setLastAction] = useState('Idle');

    // Function 1: Refresh Data
    const handleRefreshData = () => {
        // Nested helper function to demonstrate deep tracing
        const handleCalculateStats = () => {
            return {
                cpu: Math.floor(Math.random() * 100),
                memory: Math.floor(Math.random() * 100),
                network: Math.floor(Math.random() * 100)
            };
        };

        setLastAction('Refreshing Data...');
        // Simulate API call
        setTimeout(() => {
            setMetrics(handleCalculateStats());
            setLastAction('Data Refreshed');
        }, 500);
    };

    // Function 2: Upload Logs
    const handleUploadLogs = () => {
        setLastAction('Uploading Logs...');
        setTimeout(() => {
            setLastAction('Logs Uploaded Successfully');
        }, 1200);
    };

    // Function 3: Toggle Settings (Simulation)
    const handleToggleSettings = () => {
        const modes = ['Dark', 'Light', 'Auto', 'High Contrast'];
        const nextMode = modes[Math.floor(Math.random() * modes.length)];
        setLastAction(`Settings Changed: Access Mode set to ${nextMode}`);
    };

    // Function 4: Run Optimization
    const handleRunOptimization = () => {
        setLastAction('Optimizing Database...');
        let progress = 0;
        const interval = setInterval(() => {
            progress += 25;
            if (progress >= 100) {
                clearInterval(interval);
                setLastAction('Optimization Complete: +15% Performance');
            } else {
                setLastAction(`Optimizing... ${progress}%`);
            }
        }, 300);
    };

    // Function 5: User Logout
    const handleUserLogout = () => {
        setLastAction('Signing out...');
        setTimeout(() => {
            setLastAction('User Signed Out (Simulation)');
        }, 800);
    };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h2>System Dashboard</h2>
                <span style={{ color: '#94a3b8' }}>{lastAction}</span>
            </div>

            <div className="metrics-grid">
                <div className="metric-card">
                    <div className="metric-value">{metrics.cpu}%</div>
                    <div className="metric-label">CPU Usage</div>
                </div>
                <div className="metric-card">
                    <div className="metric-value">{metrics.memory}%</div>
                    <div className="metric-label">Memory</div>
                </div>
                <div className="metric-card">
                    <div className="metric-value">{metrics.network}ms</div>
                    <div className="metric-label">Latency</div>
                </div>
            </div>

            <div className="controls-row">
                <button className="action-btn primary" onClick={handleRefreshData}>
                    ↻ Refresh Data
                </button>
                <button className="action-btn" onClick={handleUploadLogs}>
                    ⬆ Upload Logs
                </button>
                <button className="action-btn" onClick={handleToggleSettings}>
                    ⚙ Settings
                </button>
                <button className="action-btn success" onClick={handleRunOptimization}>
                    ⚡ Optimize
                </button>
                <button className="action-btn danger" onClick={handleUserLogout}>
                    ← Logout
                </button>
            </div>
        </div>
    );
}

export default memo(Dashboard);
