const logs = [];
const functionUUIDs = {}; // Maps function names to their persistent UUIDs

function generateUUID() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
        return crypto.randomUUID();
    }
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

function getOrCreateUUID(functionName) {
    if (!functionName) return '';
    if (!functionUUIDs[functionName]) {
        functionUUIDs[functionName] = generateUUID();
    }
    return functionUUIDs[functionName];
}

/**
 * Wraps a function to log its execution context with Caller/Callee info.
 * @param {Function} fn - The actual function to execute
 * @param {string} fnName - Name of the function (this is the CALLER)
 * @param {string} fileName - File where it's defined
 * @param {string} componentName - Component it belongs to
 * @param {string} lexicalParent - Name of the parent function (this is the CALLEE)
 */
export function trace(fn, fnName, fileName, componentName, lexicalParent) {
    return function (...args) {
        // lexicalParent is the parent function (CALLER - where this function is defined)
        // fnName is this function (CALLEE - the function being called)

        const logEntry = {
            timestamp: new Date().toISOString(),
            caller_function: lexicalParent || '',
            callee_function: fnName || '',
            caller_uuid: getOrCreateUUID(lexicalParent),
            callee_uuid: getOrCreateUUID(fnName),
            file: fileName || 'unknown',
            component: componentName || 'unknown'
        };

        logs.push(logEntry);
        console.log(`[Trace] ${lexicalParent || '(root)'} -> ${fnName}`);

        return fn.apply(this, args);
    };
}

export function exportLogs() {
    if (logs.length === 0) {
        console.warn('[Trace] No logs to export');
        return Promise.resolve(false);
    }

    const headers = [
        "Timestamp",
        "Caller_Function",
        "Callee_Function",
        "Caller_UUID",
        "Callee_UUID",
        "File",
        "Component"
    ];

    const rows = logs.map(log => [
        log.timestamp,
        log.caller_function,
        log.callee_function,
        log.caller_uuid,
        log.callee_uuid,
        log.file,
        log.component
    ].join(","));

    const csvContent = [headers.join(","), ...rows].join("\n");

    if (import.meta.env.DEV) {
        console.log(`[Trace] Exporting ${logs.length} logs via sendBeacon`);
        
        // Use sendBeacon for async send
        const sent = navigator.sendBeacon('/__save-trace', csvContent);
        
        if (sent) {
            console.log('[Trace] Beacon sent successfully');
        } else {
            console.error('[Trace] Beacon failed, trying fetch as fallback');
            // Fallback to fetch if sendBeacon fails
            return fetch('/__save-trace', {
                method: 'POST',
                body: csvContent,
                keepalive: true
            }).then(() => {
                console.log('[Trace] Saved via fetch');
                return true;
            }).catch(err => {
                console.error('[Trace] Failed to save:', err);
                return false;
            });
        }
        return Promise.resolve(sent);
    } else {
        console.warn("Tracing save is only supported in Dev mode with local server.");
        return Promise.resolve(false);
    }
}

export function getLogCount() {
    return logs.length;
}

// Auto-export on app close / refresh
window.addEventListener("beforeunload", exportLogs);

// Make exportLogs available globally for Selenium tests
if (typeof window !== 'undefined') {
    window.__exportTraceLogs = exportLogs;
    window.__getTraceLogCount = getLogCount;
}
