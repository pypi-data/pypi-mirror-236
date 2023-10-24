from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi

class RequestHandler(BaseHTTPRequestHandler):
    UPLOAD_DIR = os.getcwd()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        files = os.listdir(self.UPLOAD_DIR)

        message = ''
        message += """
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>文件分享</title>
                            <style>
                                hr {
                                    color: red;
                                    background-color: red;
                                    height: 2px;
                                    border: none;
                                }
                                body {
                                font-size:120%;
                                }
                                input {
                                font-size:120%;
                                }
                            </style>

                    </head>
                <body>
                    <input type='file' name='file'>
                        <input type='submit'>
                        </form>
                    <hr>
                    <ul>
                """
        message += f'<h3>{self.UPLOAD_DIR}</h3>'

        for file in files:
            message += f"<li><a href='/download/{file}'>{file}</a></li>"
        message += "</ul></body></html>"

        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        if 'file' in form:
            file_item = form['file']

            if file_item.filename:
                with open(os.path.join(self.UPLOAD_DIR, file_item.filename), 'wb') as f:
                    f.write(file_item.file.read())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'File uploaded successfully')
                return
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'No file found')

    def do_DOWNLOAD(self, filename):
        file_path = os.path.join(self.UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename={filename}')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')

    def do_GET_DOWNLOAD(self):
        path_parts = self.path.split('/')
        if len(path_parts) == 3 and path_parts[1] == 'download':
            filename = path_parts[2]
            self.do_DOWNLOAD(filename)

    def do_GET_FILES(self):
        self.do_GET()

    def do_POST_FILES(self):
        self.do_POST()

if __name__ == '__main__':
    PORT = 8003
    server = HTTPServer(('localhost', PORT), RequestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()