import { useState, memo } from 'react';
import './AsyncPanel.css';

function AsyncPanel() {
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    // Async Function 1: Fetch User Data
    const handleFetchUserData = async () => {
        setIsLoading(true);
        setResults([{ label: 'Status', value: 'Fetching user data...' }]);

        // Nested async function
        const handleAuthenticateUser = async () => {
            await new Promise(resolve => setTimeout(resolve, 800));

            // Deeply nested async function
            const handleValidateToken = async () => {
                await new Promise(resolve => setTimeout(resolve, 500));
                return { valid: true, token: 'abc123xyz' };
            };

            const tokenData = await handleValidateToken();
            return { authenticated: tokenData.valid, userId: 'user_42' };
        };

        try {
            const authResult = await handleAuthenticateUser();
            setResults([
                { label: 'User ID', value: authResult.userId },
                { label: 'Authenticated', value: authResult.authenticated ? 'Yes' : 'No' },
                { label: 'Timestamp', value: new Date().toISOString() }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // Async Function 2: Load Database Records
    const handleLoadRecords = async () => {
        setIsLoading(true);
        setResults([{ label: 'Status', value: 'Loading database records...' }]);

        const handleQueryDatabase = async () => {
            await new Promise(resolve => setTimeout(resolve, 1000));

            const handleFilterResults = async (records) => {
                await new Promise(resolve => setTimeout(resolve, 300));
                return records.filter(r => r.active);
            };

            const rawRecords = [
                { id: 1, name: 'Record A', active: true },
                { id: 2, name: 'Record B', active: false },
                { id: 3, name: 'Record C', active: true }
            ];

            return await handleFilterResults(rawRecords);
        };

        try {
            const records = await handleQueryDatabase();
            setResults(records.map(r => ({ label: r.name, value: `ID: ${r.id}` })));
        } finally {
            setIsLoading(false);
        }
    };

    // Async Function 3: Process Payment
    const handleProcessPayment = async () => {
        setIsLoading(true);
        setResults([{ label: 'Status', value: 'Processing payment...' }]);

        const handleVerifyPayment = async () => {
            await new Promise(resolve => setTimeout(resolve, 600));

            const handleEncryptData = async (data) => {
                await new Promise(resolve => setTimeout(resolve, 400));
                return btoa(JSON.stringify(data)); // Simple base64 encoding
            };

            const encrypted = await handleEncryptData({ amount: 99.99, currency: 'USD' });
            return { success: true, transactionId: encrypted.substring(0, 12) };
        };

        try {
            const paymentResult = await handleVerifyPayment();
            setResults([
                { label: 'Transaction ID', value: paymentResult.transactionId },
                { label: 'Status', value: paymentResult.success ? 'Success' : 'Failed' },
                { label: 'Amount', value: '$99.99' }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    // Async Function 4: Cascade Async Calls
    const handleCascadeAsync = async () => {
        setIsLoading(true);
        setResults([{ label: 'Status', value: 'Starting cascade...' }]);

        const handleStepOne = async () => {
            await new Promise(resolve => setTimeout(resolve, 300));

            const handleStepTwo = async () => {
                await new Promise(resolve => setTimeout(resolve, 300));

                const handleStepThree = async () => {
                    await new Promise(resolve => setTimeout(resolve, 300));
                    return 'All steps completed';
                };

                return await handleStepThree();
            };

            return await handleStepTwo();
        };

        try {
            const result = await handleStepOne();
            setResults([
                { label: 'Cascade Result', value: result },
                { label: 'Steps', value: '3 levels deep' }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="async-panel">
            <div className="async-header">
                <h3>Async Operations</h3>
                <span className={`loading-indicator ${isLoading ? 'status-loading' : 'status-ready'}`}>
                    {isLoading ? 'Loading...' : 'Ready'}
                </span>
            </div>

            <div className="result-display">
                {results.length === 0 ? (
                    <div style={{ opacity: 0.5, textAlign: 'center', paddingTop: '2rem' }}>
                        No data yet. Click a button to test async tracing.
                    </div>
                ) : (
                    results.map((item, i) => (
                        <div key={i} className="result-item">
                            <span className="result-label">{item.label}:</span>
                            <span className="result-value">{item.value}</span>
                        </div>
                    ))
                )}
            </div>

            <div className="async-controls">
                <button
                    className="async-btn"
                    onClick={handleFetchUserData}
                    disabled={isLoading}
                >
                    <span>👤</span> Fetch User
                </button>
                <button
                    className="async-btn"
                    onClick={handleLoadRecords}
                    disabled={isLoading}
                >
                    <span>📊</span> Load Records
                </button>
                <button
                    className="async-btn"
                    onClick={handleProcessPayment}
                    disabled={isLoading}
                >
                    <span>💳</span> Process Payment
                </button>
                <button
                    className="async-btn"
                    onClick={handleCascadeAsync}
                    disabled={isLoading}
                >
                    <span>⚡</span> Cascade Async
                </button>
            </div>
        </div>
    );
}

export default memo(AsyncPanel);
