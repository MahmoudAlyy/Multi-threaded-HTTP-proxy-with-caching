import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting...")

# Connect to our HTTP server, make sure the server is already running.
client_socket.connect(("127.0.0.5", 11112))
print("Connected, sending request...")

# Send an HTTP request to get an image
client_socket.send(b"GET www/secret.png HTTP/1.0\r\n\r\n")
print("Sent request...")

# Wait for the socket to process the request, note that
# in real life you don't need to put any code to wait.
# but our case is an exception because we're calling another
# process in the same OS so things happen way fast.
#time.sleep(0.7)

# Receive the reply
data = client_socket.recv(4096)

# Extract the HTTP header (request line + headers) and body.
header, body = data.split(b'\r\n\r\n')

print("*" * 50)
print(f"H:[{len(header)}] bytes\nB:[{len(body)}] bytes...\n")
print(header.decode())
print("*" * 50)
client_socket.close()
