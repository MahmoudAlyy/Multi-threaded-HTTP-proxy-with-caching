import socket

server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
# Set the address to be reusable, to avoid waiting for a while if the program
# crashed while the socket was open.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the server address
server_socket.bind(("127.0.0.5", 11112))

# Start listening, this makes the socket a "welcome" socket
# that gives birth to a socket per each connecting client.
server_socket.listen()

print("Waiting for clients...")
# now try: curl -X GET http://127.0.0.1:11112 (in terminal)
# and see the connection in the code here.
client_socket, addr = server_socket.accept()
print("Client arrived...")

# read the incoming HTTP request.
data = client_socket.recv(128 * 1024)
print(f"Got [{len(data)}] bytes...\n")
print("*" * 50)
print(f"{data}\n")
print("*" * 50)
print(f"{data.decode()}")
print("*" * 50)

# Send a response.
client_socket.send(b"HTTP/1.0 200 OK\r\n\r\n")
client_socket.close()
server_socket.close()
