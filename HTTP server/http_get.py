import socket

def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9090))
    server.listen(5)
    print("HTTP server started on port 8080")

    while True:
        connection_socket,addr=server.accept()
        print(f"connection from {addr}")
        handle_request(connection_socket)


def handle_request(connection_socket):
    request = connection_socket.recv(1024).decode('utf-8')
    print(f'Request received: \n{request}')
    response = """HTTP/1.1 200 OK
                    Content-Type: text/html

                    <!DOCTYPE html>
                    <html>
                        <head>
                            <title>My Simple HTTP Server</title>
                        </head>
                        <body>
                            <h1>Welcome to My Simple HTTP Server!</h1>
                            <p>This is a basic example of an HTTP server written in Python.</p>
                        </body>
                    </html>"""
    connection_socket.sendall(response.encode('utf-8'))
    connection_socket.close()
if __name__ == "__main__":
    start_server()
