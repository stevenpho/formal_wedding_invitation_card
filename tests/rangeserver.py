import os, re, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
class H(SimpleHTTPRequestHandler):
    def send_head(self):
        rng = self.headers.get('Range')
        path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().send_head()
        m = re.match(r'bytes=(\d*)-(\d*)', rng)
        size = os.path.getsize(path)
        s = int(m.group(1)) if m.group(1) else 0
        e = int(m.group(2)) if m.group(2) else size - 1
        e = min(e, size - 1)
        f = open(path, 'rb'); f.seek(s)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {s}-{e}/{size}')
        self.send_header('Content-Length', str(e - s + 1))
        self.end_headers()
        self._left = e - s + 1
        return f
    def copyfile(self, src, dst):
        left = getattr(self, '_left', None)
        if left is None: return super().copyfile(src, dst)
        while left > 0:
            b = src.read(min(65536, left))
            if not b: break
            dst.write(b); left -= len(b)
        self._left = None
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes'); super().end_headers()
os.chdir(sys.argv[1])
ThreadingHTTPServer(('0.0.0.0', int(sys.argv[2])), H).serve_forever()
