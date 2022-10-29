import socket
import concurrent.futures as pool
import sys

def receive_message(conn):
    while True:
        try:
            msg = conn.recv(2048).decode('utf-8')
            print(msg)
        except:
            print("Server down")
            sys.exit()

HOST_IP = "Insert IP here"
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9191
executor = pool.ThreadPoolExecutor()

name = input("What should be your user name ?\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST_IP, PORT))

server.send(name.encode('utf-8'))

executor.submit(receive_message, server)

while True:
    msg = input('')
    server.send(msg.encode('utf-8'))

