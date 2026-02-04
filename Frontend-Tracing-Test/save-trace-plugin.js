
import fs from 'fs';
import path from 'path';

export default function saveTracePlugin() {
    return {
        name: 'save-trace-server',
        configureServer(server) {
            server.middlewares.use('/__save-trace', (req, res, next) => {
                if (req.method === 'POST') {
                    let body = '';
                    req.on('data', chunk => {
                        body += chunk.toString();
                    });
                    req.on('end', () => {
                        const logDir = path.resolve(process.cwd(), 'tracing-logs');
                        if (!fs.existsSync(logDir)) {
                            fs.mkdirSync(logDir);
                        }

                        const filename = `trace_session_${Date.now()}.csv`;
                        const filePath = path.join(logDir, filename);

                        fs.writeFile(filePath, body, (err) => {
                            if (err) {
                                console.error('Failed to save trace log:', err);
                                res.statusCode = 500;
                                res.end('Error');
                            } else {
                                console.log(`[Trace] Saved logs to ${filePath}`);
                                res.statusCode = 200;
                                res.end('Saved');
                            }
                        });
                    });
                } else {
                    next();
                }
            });
        }
    };
}
