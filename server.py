import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        received_data = self.request.recv(2048)
        with open("page.html", "r") as f:
            html_string = f.read()

        with open("function.js", "r") as g:
            js_string = g.read()

        if received_data.decode().startswith("GET /function.js"):
            self.request.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Length:{len(js_string)}\r\nContent-Type: text/javascript; charset=utf-8\r\n\r\n{js_string}".encode()
            )
        if received_data.decode().startswith("GET /"):
            self.request.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Length:{len(html_string)}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html_string}".encode()
            )

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
