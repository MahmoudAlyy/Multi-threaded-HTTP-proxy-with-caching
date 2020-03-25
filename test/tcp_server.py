import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("127.0.0.5", 50000)
server_socket.bind(server_addr)



server_socket.listen(10)
print("Waiting for clients...")

while True:
    client_socket, addr = server_socket.accept()
    print("client socket:\nSource:",client_socket.getsockname(),"\nDest:", client_socket.getpeername())
    while True:
        msg = client_socket.recv(2)
        if len(msg) == 0 :
            break
        print(msg.decode())

    #client_socket.send(b"1234567890")  # Send a reply
    #client_socket.close()


