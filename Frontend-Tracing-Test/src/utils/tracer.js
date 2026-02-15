const logs = [];
const functionUUIDs = {}; // Maps function names to their persistent UUIDs
let currentExecutionContext = null;

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



/* -------------------------------
   HTTP instrumentation (fetch)
-------------------------------- */

(function instrumentFetch() {
    if (!window.fetch) return;

    const originalFetch = window.fetch;

    window.fetch = async function (input, init = {}) {
        const method = (init.method || 'GET').toUpperCase();
        const url =
            typeof input === 'string'
                ? input
                : input && input.url
                ? input.url
                : '';

        if (currentExecutionContext && logs.length > 0) {
            const lastLog = logs[logs.length - 1];
            lastLog.http_method = method;
            lastLog.http_url = url;
        }

        return originalFetch.apply(this, arguments);
    };
})();


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
        currentExecutionContext = {
            fnName,
            lexicalParent,
            fileName,
            componentName
        };

        const logEntry = {
            timestamp: new Date().toISOString(),
            caller_function: lexicalParent || '',
            callee_function: fnName || '',
            caller_uuid: getOrCreateUUID(lexicalParent),
            callee_uuid: getOrCreateUUID(fnName),
            file: fileName || 'unknown',
            component: componentName || 'unknown',
            http_method: '',
            http_url: ''
        };

        logs.push(logEntry);
        console.log(`[Trace] ${lexicalParent || '(root)'} -> ${fnName}`);

        try {
            return fn.apply(this, args);
        } finally {
            currentExecutionContext = null;
        }
    };
}

function exportLogs() {
    if (logs.length === 0) return;

    const headers = [
        "Timestamp",
        "Caller_Function",
        "Callee_Function",
        "Caller_UUID",
        "Callee_UUID",
        "File",
        "Component",
        "HTTP_Method",
        "HTTP_URL"
    ];

    const rows = logs.map(log => [
        log.timestamp,
        log.caller_function,
        log.callee_function,
        log.caller_uuid,
        log.callee_uuid,
        log.file,
        log.component,
        log.http_method,
        log.http_url
    ].map(v => `"${String(v || '').replace(/"/g, '""')}"`)
    .join(",")
    );
    const csvContent = [headers.join(","), ...rows].join("\n");

    if (import.meta.env.DEV) {
        navigator.sendBeacon('/__save-trace', csvContent);
    } else {
        console.warn("Tracing save is only supported in Dev mode with local server.");
    }
}

// Auto-export on app close / refresh
window.addEventListener("beforeunload", exportLogs);
