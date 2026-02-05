import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default function saveTracePlugin() {
    return {
        name: 'save-trace-server',
        configureServer(server) {
            server.middlewares.use((req, res, next) => {
                // Check if the URL starts with /__save-trace
                if (req.method === 'POST' && (req.url.startsWith('/__save-trace') || req.originalUrl?.startsWith('/__save-trace'))) {
                    console.log(`[Save-Trace] Received request on ${req.url}`);
                    let body = '';
                    req.on('data', chunk => {
                        body += chunk.toString();
                    });
                    req.on('end', () => {
                        try {
                            // Save to a directory named 'tracing-logs' in the same folder as this plugin
                            const logDir = path.resolve(__dirname, 'tracing-logs');
                            if (!fs.existsSync(logDir)) {
                                fs.mkdirSync(logDir, { recursive: true });
                            }

                            const filename = `trace_session_${Date.now()}.csv`;
                            const filePath = path.join(logDir, filename);

                            fs.writeFile(filePath, body, (err) => {
                                if (err) {
                                    console.error('[Save-Trace] Failed to save trace log:', err);
                                    res.statusCode = 500;
                                    res.end('Error saving');
                                } else {
                                    console.log(`[Save-Trace] Successfully saved logs to: ${filePath}`);
                                    res.statusCode = 200;
                                    res.setHeader('Access-Control-Allow-Origin', '*');
                                    res.end('Saved');
                                }
                            });
                        } catch (err) {
                            console.error('[Save-Trace] Unexpected error:', err);
                            res.statusCode = 500;
                            res.end('Error');
                        }
                    });
                } else {
                    next();
                }
            });
        }
    };
}
