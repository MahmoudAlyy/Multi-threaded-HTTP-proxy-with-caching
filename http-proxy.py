import socket
import re
"""
GET /hypertext/WWW/TheProject.html HTTP/1.0
HOST: http://info.cern.ch


"""

"""
GET /docs/index.html HTTP/1.0
Host: www.nowhere123.com
Accept: image/gif, image/jpeg, */*
Accept-Language: en-us
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)


"""

# i need to check if uri is just a (/) there must be a hostname included
# curreltny i only support the get request for version 1.0
#validate
#Cache 200 responses


def handle (buffer):
    temp = buffer.split(b'\r\n')
    request_line = temp[0].decode()
    request_headers = []
    for item in temp[1:]:
        if len(item) !=0 :  
            request_headers.append(item.decode())
            
    ### CHECKING request line
    method, path, version = request_line.split()

    if method != "GET"  or version != "HTTP/1.0":
        print( "Not Implemented (501) for valid HTTP methods other than GET")
    
    if path[0] == "/":
        host_header_flag = False
        for item in request_headers:
            if item.find("Host:") != -1:
                host_header_flag = True
                url = item[6:] + path
                break
        if host_header_flag:
            print("bad request 400")
    
    

    ### Validate request header

    #[a-zA-z-]*\:.*
    ### check if headers are  properly formatted
    for item in request_headers:
        if not (re.match(r'.*\: .*', item)):
            print("header not properly formatted")



    #print(request_headers)
    main()
    



def main():

    print("mainnnnnnnnnnnnn")
    buffer = b''
    while True:      
        data = client_socket.recv(50*1024)
        buffer = buffer + data
        if buffer.find(b'\r\n\r\n') > 0 :
            #print(buffer)
            handle(buffer)
            buffer = b''
            ### still need to handle for sequetnil input


# #string = data.decode()
# #print(string)
# #print("******************************")
# print(data)

# for item in data.split(b'\r\n'):
#     print (item)
#     print("***********************")


if __name__ == "__main__":

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the address to be reusable, to avoid waiting for a while if the program
    # crashed while the socket was open.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set the server address
    server_socket.bind(("127.0.0.21", 2121))

    # Start listening, this makes the socket a "welcome" socket
    # that gives birth to a socket per each connecting client.
    server_socket.listen(10)
    print("Waiting for clients...")
    client_socket, addr = server_socket.accept()
    print("Client arrived...")
    main()
