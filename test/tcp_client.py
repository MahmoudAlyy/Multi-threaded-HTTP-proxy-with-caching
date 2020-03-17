import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ("127.0.0.5", 50000)
# New!, TCP is a stream protocol; it needs
# to be connected first.
client_socket.connect(server_addr)


client_socket.send(b"1234567890")

# rec = client_socket.recv(512)
# print(rec)
