import socket
import time
import concurrent.futures as pool

host_ip = "Insert IP here"

#Creates a thread for each client so that server doesn't freeze
def clientThread(client, host):
    name = client.recv(1024).decode('utf-8')
    print(f"{name} connected")
    broadcast_all(f"{name} connected".encode('utf-8'))
    
    # client.send("Welcome to the chat".encode('utf-8'))
    
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            msg = f"<{name}> {msg}"
            
            print(msg)
            broadcast(msg, client)
            
        except:
            remove(client)
            break
           
#Broadcasts a message to everybody except the sender 
def broadcast(msg, conn):
    for client in list_of_clients:
        if client != conn:
            try:
                client.send(msg.encode('utf-8'))
            except:
                client.close()
                remove(client)
                
def broadcast_all(msg):
    for i in list_of_clients:
        i.send(msg)

#Removes a client if they disconnect
def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

#Keeps check of who is connected and their sockets
list_of_clients = []
executor = pool.ThreadPoolExecutor()
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9191

#Setup server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

print("Starting to listen")
server.listen(100)

while True:
    conn, ip = server.accept()
    list_of_clients.append(conn)
    
    executor.submit(clientThread, conn, server)
    
    