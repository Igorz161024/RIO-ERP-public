const http = require('http');
const port = 8001;

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Node server is running\n');
});

server.listen(port, () => {
  console.log(`Server running at http://0.0.0.0:${port}/`);
});
