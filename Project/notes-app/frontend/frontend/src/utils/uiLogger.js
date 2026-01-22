import api from "../api/axios";

// Track logged events to prevent excessive logging of the same event
const loggedEvents = new Map();
const LOG_DEDUP_WINDOW = 100; // ms - don't log same event twice within 100ms

export function sendUILog(logData) {
  // Create a unique key for this log event
  const eventKey = `${logData.event || logData.function}:${logData.file}:${logData.line}`;
  
  // Check if we've logged this event recently
  const lastLogTime = loggedEvents.get(eventKey);
  const now = Date.now();
  
  if (lastLogTime && (now - lastLogTime) < LOG_DEDUP_WINDOW) {
    // Skip this log - same event logged too recently
    return;
  }
  
  // Update the timestamp for this event
  loggedEvents.set(eventKey, now);
  
  // Log to browser console for debugging
  console.log("[UI_TRACE]", logData);
  
  // Send to backend with retry logic
  const sendLog = async () => {
    try {
      await api.post("/ui-logs", {
        ...logData,
        timestamp: new Date().toISOString(),
        url: window.location.href
      });
    } catch (err) {
      console.error("[UI_TRACE_ERROR]", err.message);
      // Retry once after 500ms
      setTimeout(() => {
        try {
          api.post("/ui-logs", {
            ...logData,
            timestamp: new Date().toISOString(),
            url: window.location.href,
            retried: true
          }).catch(() => {});
        } catch (e) {}
      }, 500);
    }
  };
  
  // Fire-and-forget but ensure it runs
  sendLog();
}
