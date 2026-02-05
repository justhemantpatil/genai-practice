import { useState, memo } from 'react';
import './NetworkPanel.css';

function NetworkPanel() {
    const [logs, setLogs] = useState([]);
    const [status, setStatus] = useState('Online');

    const addLog = (msg) => {
        setLogs(prev => [`[${new Date().toLocaleTimeString()}] ${msg}`, ...prev].slice(0, 10));
    };

    // Function 1: Ping Server
    const handlePingServer = () => {
        addLog('Pinging gateway...');

        // Nested Function 1
        const handleProcessResponse = (latency) => {
            // Deeply Nested Function 2
            const handleAnalyzeJitter = (lat) => {
                return lat < 10 ? 'Stable' : 'Jitter Detected';
            };

            const quality = handleAnalyzeJitter(latency);
            addLog(`Reply from gateway: time=${latency}ms | Network ${quality}`);
        };

        setTimeout(() => {
            handleProcessResponse(Math.floor(Math.random() * 50));
        }, 600);
    };

    // Function 2: Deep Packet Inspection
    const handleScanPackets = () => {
        addLog('Starting Deep Packet Inspection...');

        const handleDecryptLayer = (layer) => {
            const handleVerifySignature = (sig) => {
                return sig === 'valid';
            };

            if (handleVerifySignature('valid')) {
                return `Layer ${layer} Decrypted`;
            }
            return `Layer ${layer} Failed`;
        };

        setTimeout(() => {
            const result = handleDecryptLayer(1);
            addLog(result);
        }, 800);
    };

    // Function 3: Flush DNS
    const handleFlushDNS = () => {
        addLog('Flushing DNS Cache...');
        setTimeout(() => addLog('DNS Resolver Cache Flushed'), 400);
    };

    // Function 4: Trace Route
    const handleTraceRoute = () => {
        addLog('Tracing route to 8.8.8.8...');

        // Recursive mock
        const handleHop = (hopCount) => {
            if (hopCount > 3) {
                addLog('Trace Complete: 4 hops');
                return;
            }
            addLog(`Hop ${hopCount}: 192.168.1.${hopCount * 10}`);
            setTimeout(() => handleHop(hopCount + 1), 500);
        };

        handleHop(1);
    };

    // Function 5: Toggle Connection
    const handleToggleConnection = () => {
        const newStatus = status === 'Online' ? 'Offline' : 'Online';
        setStatus(newStatus);
        addLog(`Network Interface changed to ${newStatus}`);
    };

    return (
        <div className="network-panel">
            <div className="network-header">
                <h3>Network Diagnostics</h3>
                <span className={`status-indicator status-${status.toLowerCase()}`}>
                    {status}
                </span>
            </div>

            <div className="log-console">
                {logs.length === 0 ? <div style={{ opacity: 0.5 }}>Ready to monitor...</div> : logs.map((log, i) => (
                    <div key={i} className="log-entry">{log}</div>
                ))}
            </div>

            <div className="network-controls">
                <button className="net-btn" onClick={handlePingServer}>
                    <span>📡</span> Ping Gateway
                </button>
                <button className="net-btn" onClick={handleScanPackets}>
                    <span>🔍</span> Inspect Packets
                </button>
                <button className="net-btn" onClick={handleTraceRoute}>
                    <span>🛣️</span> Trace Route
                </button>
                <button className="net-btn" onClick={handleFlushDNS}>
                    <span>🗑️</span> Flush DNS
                </button>
                <button className="net-btn" onClick={handleToggleConnection}>
                    <span>🔌</span> {status === 'Online' ? 'Disconnect' : 'Connect'}
                </button>
            </div>
        </div>
    );
}

export default memo(NetworkPanel);
