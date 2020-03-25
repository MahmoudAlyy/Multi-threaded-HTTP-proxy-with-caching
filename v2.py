import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("www.google.com", 443))
s.sendall(b'CONNECT www.google.com:443 HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0\r\nProxy-Connection: keep-alive\r\nConnection: keep-alive\r\nHost: www.google.com:443\r\n\r\n')
response = s.recv(4096)
print(response)
#print (response.decode())

s.close



