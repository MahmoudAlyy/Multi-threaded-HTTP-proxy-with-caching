import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ("127.0.0.21", 2121)
s.connect(server_addr)

