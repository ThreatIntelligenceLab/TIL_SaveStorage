#Made by Reza Rafati at ThreatIntelligenceLab.com
#Usage: #python run_server.py 
#Description: Starts quick webserver with upload form. Can be used to quickly move files from A to B. It creates the upload folder next to the location where the script is running. By default this runs on 127.0.0.1:8000. Change these details if needed at line 55.


from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os

UPLOAD_DIR = './uploads/'  # Directory to store uploaded files

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html>
                <body>
                <form method="post" enctype="multipart/form-data">
                <input type="file" name="upload" />
                <input type="submit" value="Upload" />
                </form>
                </body>
                </html>
            ''')
            return

        self.send_error(404)

    def do_POST(self):
        if self.path == '/':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            upload_file = form['upload']

            if upload_file.filename:
                file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
                with open(file_path, 'wb') as f:
                    f.write(upload_file.file.read())

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'File {upload_file.filename} uploaded successfully.'.encode())
                return

        self.send_error(404)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    run()
