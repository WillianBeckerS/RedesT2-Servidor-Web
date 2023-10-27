# import socket programming library
import socket
from pathlib import Path
import os
import pickle
import datetime
from zoneinfo import ZoneInfo

# import thread module
from _thread import *
import threading

# thread function
def threaded(client: socket.socket):
    data = client.recv(4096)
    message = data.decode()

    request_headers = message.split()
    print(request_headers)

    file_data = convert_file_to_protocol(request_headers[1])
    client.send(file_data)
    client.close()

def convert_file_to_protocol(file_name):
    file_path = f'./files_server{file_name}'
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_size = len(file_content)

            last_modified_timestamp = os.path.getmtime(file_path)
            last_modified_date = datetime.datetime.fromtimestamp(last_modified_timestamp, ZoneInfo("Etc/GMT")).strftime('%a, %d %b %Y %H:%M:%S GMT')

            if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = "image/jpeg"
            elif file_path.endswith('.png'):
                content_type = "image/png"
            elif file_path.endswith('.html'):
                content_type = "text/html"
            else:
                content_type = "application/octet-stream"

            headers = [
                "HTTP/1.1 200 OK",
                f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
                f"Last-Modified: {last_modified_date}",
                f"Server: ServidorTCPPython/1.0",
                f"Content-Type: {content_type}",
                f"Content-Length: {file_size}",
                "Connection: close",
                "\r\n"
            ]

            header = "\r\n".join(headers)
            return header.encode() + file_content

    except FileNotFoundError:
        print(f'File {file_path} not found')
        file_path = f'./error/404.html'
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_size = len(file_content)

            last_modified_timestamp = os.path.getmtime(file_path)
            last_modified_date = datetime.datetime.fromtimestamp(last_modified_timestamp, ZoneInfo("Etc/GMT")).strftime('%a, %d %b %Y %H:%M:%S GMT')

            headers = [
                "HTTP/1.1 404 Not Found",
                f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
                f"Last-Modified: {last_modified_date}",
                "Server: ServidorTCPPython/1.0",
                "Content-Type: text/html",
                f"Content-Length: {file_size}",
                "Connection: close",
                "\r\n"
            ]
            header = "\r\n".join(headers)
            return header.encode() + file_content

def Main():
    host = "127.0.0.1"

    #host = "10.0.2.15"

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname_ex(hostname)
    print("socket binded to port", port)
    print(f"Server IP is {ip_address[2]}")

    # put the socket into listening mode
    socket_server.listen(5)
    print(f"socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        client, addr = socket_server.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (client,))
    socket_server.close()


if __name__ == '__main__':
    Main()
