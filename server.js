// Lightweight local dev server mimicking Vercel routing rules
// Zero external dependencies - works out of the box with built-in Node.js modules

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;
const ROOT_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.ics': 'text/calendar; charset=utf-8'
};

function serveFile(res, filePath) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  let pathname = parsedUrl.pathname;

  // Root or /admin -> Admin Dashboard
  if (pathname === '/' || pathname === '/admin' || pathname === '/index.html') {
    return serveFile(res, path.join(ROOT_DIR, 'index.html'));
  }

  // /invite -> Sample Invitation
  if (pathname === '/invite' || pathname === '/invite.html') {
    return serveFile(res, path.join(ROOT_DIR, 'invite.html'));
  }

  // Serve static files in assets/ or root if they exist with an extension
  const potentialFile = path.join(ROOT_DIR, pathname);
  if (fs.existsSync(potentialFile) && fs.statSync(potentialFile).isFile()) {
    return serveFile(res, potentialFile);
  }

  // Rewrite any dynamic name route (e.g. /Minh-Khoa, /Trần-Đức-Hải) to invite.html
  // Exclude favicon or obvious file extensions
  if (!pathname.includes('.')) {
    return serveFile(res, path.join(ROOT_DIR, 'invite.html'));
  }

  // Fallback 404
  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('404 Not Found');
});

server.listen(PORT, () => {
  console.log(`\n======================================================`);
  console.log(`🎓 HCMUS Graduation Invite Server running locally!`);
  console.log(`👉 Trang Quản trị (Admin):  http://localhost:${PORT}`);
  console.log(`👉 Thiệp mời thử nghiệm:    http://localhost:${PORT}/Minh-Khoa`);
  console.log(`======================================================\n`);
});
