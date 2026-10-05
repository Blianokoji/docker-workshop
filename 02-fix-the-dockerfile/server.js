const http = require('http');
const os = require('os');

const PORT = 3000;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ status: 'ok' }));
  }

  res.writeHead(200, { 'Content-Type': 'application/json' });
  const payload = {
    message: '🎉 Congratulations! You fixed the Dockerfile and containerized this app!',
    container_info: {
      hostname: os.hostname(),
      platform: os.platform(),
      architecture: os.arch(),
      node_version: process.version,
      uptime_seconds: Math.floor(process.uptime()),
      total_memory_mb: Math.round(os.totalmem() / 1024 / 1024),
      free_memory_mb: Math.round(os.freemem() / 1024 / 1024)
    },
    timestamp: new Date().toISOString()
  };
  res.end(JSON.stringify(payload, null, 2));
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`[INFO] Server running on http://0.0.0.0:${PORT}`);
  console.log(`[INFO] Container Hostname: ${os.hostname()}`);
});