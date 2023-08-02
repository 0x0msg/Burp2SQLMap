from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        raw_request = self.rfile.read(content_length)
        print("Received HTTP Request:")
        print(raw_request.decode('utf-8'))

        # Save the received HTTP request to a file
        with open("file.txt", "w") as file:
            file.write(raw_request.decode('utf-8'))

        self.send_response(200)
        self.end_headers()

        # Get the current directory path
        current_dir = os.getcwd()
        run_sqlmap_in_sql_py(current_dir)

def run_sqlmap_in_sql_py(current_dir):
    try:
        sqlmap_cmd = f'python3 sql.py "{current_dir}"'
        process = Popen(sqlmap_cmd, shell=True)
        print("SQLMap is running...")
    except Exception as e:
        print("Error running SQLMap:", e)

def run_server(server_address, handler_class):
    httpd = HTTPServer(server_address, handler_class)
    print(f"Starting server on {server_address[0]}:{server_address[1]}...")
    httpd.serve_forever()

if __name__ == '__main__':
    server_address = ('localhost', 8888)  # Change the address and port as needed
    run_server(server_address, RequestHandler)
