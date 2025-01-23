import socket
import os
import json


def read_data():
    if os.path.exists("data.json"):
        with open("data.json","r") as f:
            return json.load(f)   #convert json to python and return dictionary
    return {}

def write_data(data):
    with open("data.json","w") as f:
        json.dump(data,f)  #convert python to json and write to file 



def handle_request(connection_socket):
    request = connection_socket.recv(1024).decode('utf-8')
    print(f"Request received:\n{request}")
    
    # Split the request into method and resource
    request_lines = request.splitlines()
    method, resource, _ = request_lines[0].split()

    data_store=read_data() #at first empty dictionary, if later contains filled dictonaries


    if method == 'GET':
        # Return the current data in the "data_store"
        response = f"""HTTP/1.1 200 OK
Content-Type: application/json

{json.dumps(data_store)}"""
    
    if method=='PUT':
        #first we need data to put so write one dictionary
        data_store["name"]="Mouli"
        write_data(data_store) #call write data to write this dic into the json file
        response ="""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>PUT Method</title>
    </head>
    <body>
        <h1>PUT Method: Data successfully updated!</h1>
    </body>
</html>"""
    elif method=='DELETE':
        if 'name' in data_store:
            del data_store["name"]
            write_data(data_store)
            response ="""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>DELETE Method</title>
    </head>
    <body>
        <h1>DELETE Method: Data successfully deleted!</h1>
    </body>
</html>"""
        else:
             response = """HTTP/1.1 404 Not Found
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>DELETE Method</title>
    </head>
    <body>
        <h1>DELETE Method: No data to delete.</h1>
    </body>
</html>"""
    else:
        response =  """HTTP/1.1 405 Method Not Allowed
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>The HTTP method you used is not allowed on this server.</p>
    </body>
</html>"""
    connection_socket.sendall(response.encode('utf-8'))
    connection_socket.close()


def start_server():
    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server to the localhost and port 9090
    server.bind(('0.0.0.0', 9091))
    server.listen(5)
    
    print("HTTP Server started on port 9091...")
    
    while True:
        # Accept incoming client connections
        connection_socket, addr = server.accept()
        print(f"Connection from {addr}")
        
        # Handle the request from the client
        handle_request(connection_socket)

# Start the server
start_server()
