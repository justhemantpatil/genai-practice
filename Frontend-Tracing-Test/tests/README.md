# Frontend Tracing Test Suite

This directory contains automated Selenium tests for the Frontend Tracing system.

## Prerequisites

```bash
pip install selenium
```

You'll also need ChromeDriver installed and in your PATH.

## Test Files

### 1. `test_app_dashboard.py`
- **Components**: App + Dashboard
- **Actions**:
  - App: Toggle Glow, System Alert
  - Dashboard: Refresh Data, Upload Logs
- **Focus**: Basic component interaction and nested functions

### 2. `test_dashboard_network.py`
- **Components**: Dashboard + NetworkPanel
- **Actions**:
  - Dashboard: Optimize, Settings
  - NetworkPanel: Ping Gateway, Trace Route
- **Focus**: Recursive functions and network diagnostics

### 3. `test_network_async.py`
- **Components**: NetworkPanel + AsyncPanel
- **Actions**:
  - NetworkPanel: Inspect Packets, Flush DNS
  - AsyncPanel: Fetch User, Process Payment
- **Focus**: Async function tracing

### 4. `test_comprehensive.py`
- **Components**: All (App, Dashboard, NetworkPanel, AsyncPanel)
- **Actions**: Multiple interactions across all components
- **Focus**: Full system integration test

## Running Tests

### Prerequisites
1. Start the dev server in a separate terminal:
   ```bash
   npm run dev
   ```

2. Ensure the server is running on `http://localhost:5175`

### Run Individual Tests
```bash
# Test 1: App + Dashboard
python tests/test_app_dashboard.py

# Test 2: Dashboard + Network
python tests/test_dashboard_network.py

# Test 3: Network + Async
python tests/test_network_async.py

# Test 4: Comprehensive
python tests/test_comprehensive.py
```

### Run All Tests
```bash
# Windows
for %f in (tests\test_*.py) do python %f

# Linux/Mac
for test in tests/test_*.py; do python "$test"; done
```

## Output

Each test will:
1. Navigate to the app
2. Perform interactions with 2+ components
3. Trigger CSV export (via page refresh)
4. Verify CSV file was created
5. Rename CSV to match test name
6. Display CSV statistics

### Expected Output
```
============================================================
Running: test_app_dashboard_interaction
============================================================

→ Navigating to app...
→ Clicking 'Toggle Glow' in App component...
→ Clicking 'System Alert' in App component...
→ Clicking 'Refresh Data' in Dashboard component...
→ Clicking 'Upload Logs' in Dashboard component...
→ Refreshing page to trigger CSV export...
✓ CSV renamed to: tracing-logs/test_app_dashboard_interaction.csv
✓ Test PASSED: CSV generated (2048 bytes)

Total rows in CSV: 15
First 5 lines of CSV:
  Timestamp,Caller_Function,Callee_Function,Caller_UUID,Callee_UUID,File,Component
  2026-02-05T11:52:00Z,App,handleMagicGlow,uuid-app-123,uuid-handleMagicGlow-456,App.jsx,App
  ...
```

## CSV Files

After running tests, you'll find renamed CSV files in `tracing-logs/`:
- `test_app_dashboard_interaction.csv`
- `test_dashboard_network_interaction.csv`
- `test_network_async_interaction.csv`
- `test_comprehensive_all_components.csv`

## Troubleshooting

### ChromeDriver not found
```bash
# Install ChromeDriver
# Windows: Download from https://chromedriver.chromium.org/
# Mac: brew install chromedriver
# Linux: sudo apt-get install chromium-chromedriver
```

### Server not running
Make sure `npm run dev` is running before executing tests.

### CSV not generated
Check that `save-trace-plugin.js` is properly configured in `vite.config.js`.

### Element not found
Verify button text matches exactly (case-sensitive).
