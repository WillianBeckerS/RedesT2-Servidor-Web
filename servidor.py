# import socket programming library
import socket
from pathlib import Path
import os
import pickle

# import thread module
from _thread import *
import threading
from utils import compute_sha256


print_lock = threading.Lock()

# thread function
def threaded(client: socket.socket):
    data = client.recv(4096)
    message = data.decode()

    palavras = message.split()

    file_data = convert_file_to_protocol(palavras[1])
    print(file_data)
    client.send(file_data)
    client.close()

def convert_file_to_protocol(file_name):
    file_path = f'./files_server{file_name}'
    try:
        with open(file_path, 'rb') as file:
            file_as_path = Path(file.name)
            file_content = file.read()
            file_checksum = compute_sha256(file_content)
            file_size = file_as_path.stat().st_size

        return b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file_content

    except FileNotFoundError:
        print(f'File {file_path} not found')
        return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"

def Main():
    host = "127.0.1.1"

    #host = "10.0.2.15"

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12346
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname_ex(hostname)
    print("socket binded to port", port)
    print(f"Server IP is {ip_address}")

    # put the socket into listening mode
    socket_server.listen(5)
    print(f"socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        client, addr = socket_server.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (client,))
    socket_server.close()


if __name__ == '__main__':
    Main()
