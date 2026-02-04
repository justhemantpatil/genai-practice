const logs = [];

/**
 * Wraps a function to log its execution context.
 * @param {Function} fn - The actual function to execute
 * @param {string} fnName - Name of the function
 * @param {string} fileName - File where it's defined
 * @param {string} componentName - Component it belongs to
 */
export function trace(fn, fnName, fileName, componentName) {
    return (...args) => {
        const logEntry = {
            timestamp: new Date().toISOString(),
            function: fnName || 'anonymous',
            file: fileName || 'unknown',
            component: componentName || 'unknown'
        };

        logs.push(logEntry);
        console.log(`[Trace] Invoked ${fnName} in ${componentName} (${fileName})`);

        return fn(...args);
    };
}

function exportLogs() {
    if (logs.length === 0) return;

    const headers = ["Timestamp", "Function", "File", "Component"];
    const rows = logs.map(log => [
        log.timestamp,
        log.function,
        log.file,
        log.component
    ].join(","));

    const csvContent = [headers.join(","), ...rows].join("\n");

    // Send to Vite dev server middleware
    if (import.meta.env.DEV) {
        navigator.sendBeacon('/__save-trace', csvContent);
    } else {
        console.warn("Tracing save is only supported in Dev mode with local server.");
    }
}

// Auto-export on app close / refresh
window.addEventListener("beforeunload", exportLogs);
