// Lightweight local dev server mimicking Vercel routing rules
// Zero external dependencies - works out of the box with built-in Node.js modules

const http = require('http');
const fs = require('fs');
const path = require('path');

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
  '.ics': 'text/calendar; charset=utf-8',
  '.mp4': 'video/mp4',
  '.m4a': 'audio/mp4',
  '.mp3': 'audio/mpeg'
};

function serveFile(req, res, filePath) {
  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';
    const range = req.headers.range;

    if (range) {
      const parts = range.replace(/bytes=/, '').split('-');
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stats.size - 1;
      const chunksize = (end - start) + 1;
      const file = fs.createReadStream(filePath, { start, end });
      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stats.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunksize,
        'Content-Type': contentType,
      });
      file.pipe(res);
    } else {
      res.writeHead(200, {
        'Content-Length': stats.size,
        'Accept-Ranges': 'bytes',
        'Content-Type': contentType,
      });
      fs.createReadStream(filePath).pipe(res);
    }
  });
}

const server = http.createServer((req, res) => {
  const reqUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname = reqUrl.pathname;

  // Admin Server Dashboard (Protected with PIN)
  if (pathname === '/admin-server' || pathname === '/admin-server.html') {
    return serveFile(req, res, path.join(ROOT_DIR, 'admin.html'));
  }

  // Redirect /admin to /admin-server
  if (pathname === '/admin') {
    res.writeHead(302, { 'Location': '/admin-server' });
    res.end();
    return;
  }

  // Root or /invite -> Graduation Invitation
  if (pathname === '/' || pathname === '/invite' || pathname === '/invite.html') {
    return serveFile(req, res, path.join(ROOT_DIR, 'index.html'));
  }

  // Serve static files in assets/ or root if they exist with an extension
  const potentialFile = path.join(ROOT_DIR, pathname);
  if (fs.existsSync(potentialFile) && fs.statSync(potentialFile).isFile()) {
    return serveFile(req, res, potentialFile);
  }

  // Rewrite any dynamic name route (e.g. /Minh-Khoa, /Trần-Đức-Hải) to index.html (Invitation)
  if (!pathname.includes('.')) {
    return serveFile(req, res, path.join(ROOT_DIR, 'index.html'));
  }

  // Fallback 404
  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('404 Not Found');
});

server.listen(PORT, () => {
  console.log(`\n======================================================`);
  console.log(`🎓 HCMUS Graduation Invite Server running locally!`);
  console.log(`🔒 Trang Quản trị (Admin):  http://localhost:${PORT}/admin-server`);
  console.log(`💌 Trang Chủ Thiệp Mời:     http://localhost:${PORT}`);
  console.log(`👉 Thiệp mời theo tên:      http://localhost:${PORT}/Minh-Khoa`);
  console.log(`======================================================\n`);
});
