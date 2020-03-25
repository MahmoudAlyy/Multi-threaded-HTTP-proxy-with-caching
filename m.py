import socket
import re
import threading
import time
"""
GET /hypertext/WWW/TheProject.html HTTP/1.0
HOST: http://info.cern.ch

GET http://info.cern.ch:80/hypertext/WWW/TheProject.html HTTP/1.1
Host: 



GET / HTTP/1.1
Host: www.google.com:80

GET www.google.com/ HTTP/1.1
Host: 

### this works


"""

"""
to get error

Get /dasdas HTTP/1.1
Host: www.google.com


"""


"""
GET /docs/index.html HTTP/1.0
Host: www.nowhere123.com
Accept: image/gif, image/jpeg, */*
Accept-Language: en-us
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)


"""

"""
GET www.nowhere123.com/docs/index.html HTTP/1.0 
Accept: image/gif, image/jpeg, */*
Accept-Language: en-us
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)


GET http://example.com:4028/docs/index.html HTTP/1.1


"""

"""
The absoluteURI form is REQUIRED when the request is being made to a proxy. The proxy is requested to forward the request or service it from a valid cache, and return the response. Note that the proxy MAY forward the request on to another proxy or directly to the server

specified by the absoluteURI. In order to avoid request loops, a proxy MUST be able to recognize all of its server names, including any aliases, local variations, and the numeric IP address. An example Request-Line would be:

       GET http://www.w3.org/pub/WWW/TheProject.html HTTP/1.1
To allow for transition to absoluteURIs in all requests in future versions of HTTP, all HTTP/1.1 servers MUST accept the absoluteURI form in requests, even though HTTP/1.1 clients will only generate them in requests to proxies.

The authority form is only used by the CONNECT method (section 9.9).

The most common form of Request-URI is that used to identify a resource on an origin server or gateway. In this case the absolute path of the URI MUST be transmitted (see section 3.2.1, abs_path) as the Request-URI, and the network location of the URI (authority) MUST be transmitted in a Host header field. For example, a client wishing to retrieve the resource above directly from the origin server would create a TCP connection to port 80 of the host "www.w3.org" and send the lines:

       GET /pub/WWW/TheProject.html HTTP/1.1
       Host: www.w3.org
followed by the remainder of the Request. Note that the absolute path cannot be empty; if none is present in the original URI, it MUST be given as "/" (the server root).
"""


#****
"""
A client MUST include a Host header field in all HTTP/1.1 request
   messages . If the requested URI does not include an Internet host
   name for the service being requested, then the Host header field MUST
   be given with an empty value. An HTTP/1.1 proxy MUST ensure that any
   request message it forwards does contain an appropriate Host header
   field that identifies the service being requested by the proxy. All
   Internet-based HTTP/1.1 servers MUST respond with a 400 (Bad Request)
   status code to any HTTP/1.1 request message which lacks a Host header
   field.
"""


# i need to check if uri is just a (/) there must be a hostname included
# curreltny i only support the get request for version 1.1
#validate
#Cache 200 responses
#need a try catch so to wont crash
#main() validate() -> error() , packet(). then will need to add multiaccess
#if input to proxy get ww.google,com:21/dasdasdas and output will be kza kza
"""
Accept from client:

GET http://www.princeton.edu/ HTTP/1.0
or
GET / HTTP/1.0
Host: www.princeton.edu
Send to remote server:
GET / HTTP/1.0
Host: www.princeton.edu
(Additional client specified headers, if any...)

Y? bec
A client MUST include a Host header field in all HTTP/1.1 request
   messages . If the requested URI does not include an Internet host
   name for the service being requested, then the Host header field MUST
   be given with an empty value. An HTTP/1.1 proxy MUST ensure that any
   request message it forwards does contain an appropriate Host header
   field that identifies the service being requested by the proxy. All
   Internet-based HTTP/1.1 servers MUST respond with a 400 (Bad Request)
   status code to any HTTP/1.1 request message which lacks a Host header
   field.
"""

#TODO
# read me add working links use info.cern a7sn
# add validation of website 
# caching
# make error message printssssssssssssssssssss
# my error stuff works (appears on webpage) but not on valid stuff maybe need to do multitaksing
# valideate port in host
# try an address u know wont reutnr stuff
# put image in readme
"""
After the response from the remote server is received, the proxy should send the response message (as-is) to the client via the appropriate socket.
 Once the transaction is complete, the proxy should close the connection to the client. Note: the proxy should terminate the connection to the remote
 server once the response has been fully received. For HTTP 1.0, the remote server will terminate the connection once the transaction is complete.
"""

pl = 100 #printing length for debugging

def validate(buffer):

    temp = buffer.split(b'\r\n')
    request_line = temp[0].decode()
    request_headers = []
    for item in temp[1:]:
        if len(item) != 0:
            request_headers.append(item.decode())

    ### CHECKING request line
    try:
        method, path, version = request_line.split()
    except:
        return None, None, None, "400 Bad Request 133"

    if method != "GET"  or not( re.match(r'http/',version.lower()) ):
        return None, None, None, "501 Not Implemented"

    port = 80       # set default port

    ### if full path is provided will split to relative URL + Host header
    if path[0] != "/":
        x = re.match(r'(https?:\/\/)?(.+?)(:[0-9]*)?(\/.*)', path)
        #2 host name, 3 port number, 4 relative path

        if x.group(2):
            host_name = x.group(2)
            host_header = host_name
        if x.group(3):
            port = x.group(3)[1:]
            host_header = host_name + x.group(3)

        relative_url = x.group(4)

        ### see if request header was provided if yes remove it
        for item in request_headers:
            if item.lower().find("host:") != -1:
                request_headers.remove(item)
                break

        ### add the host header
        host_header = "Host: "+host_header
        request_headers.insert(0,host_header)
        path = relative_url

    ### if realtive url is provided then there must exist a host header
    else:
        host_header_flag = False
        for item in request_headers:
            if item.lower().find("host:") != -1:
                host_name = item[6:]
                ### try to extract port number if provided
                try:
                    x = re.match(r'(.*:)([0-9]*)?',host_name)
                    host_name = x.group(1)[0:-1]
                    port = x.group(2)
                except:
                    pass
                host_header_flag = True
                break
        if not host_header_flag:
            print("400 Bad Request, Host header not provided")
            return None, None, None, "400 Bad Request, Host header not provided"

    ### check if headers are  properly formatted
    for item in request_headers:
        if not (re.match(r'.*\: .*', item)):
            print("400 header not properly formatted")
            return None, None, None, "400 Bad Request, Header Not properly formatted"

    space = b' '
    crlf = b'\r\n'
    packet = method.encode() + space + path.encode() + \
        space + version.encode() + crlf
    for item in request_headers:
        packet = packet + item.encode() + crlf
    packet = packet + crlf

    return packet, host_name, int(port), "0"


def error_response(error_code, client_socket, client_address):

    html = f"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
    <html><head>
    <title>{error_code}</title>
    </head><body>
    <h1>PROXY ERROR</h1>
    <p>{error_code}.<br />
    </p>
    </body></html>"""

    size = str(len(html.encode()))
    crlf = b'\r\n'

    error_msg = b'HTTP/1.0 ' + error_code.encode() + crlf + b'Content-Type: text/html; charset=UTF-8' + \
        crlf + b'Content-Length: '+size.encode() + crlf + crlf

    error_msg = error_msg + html.encode() + b'\n'

    print("PROXY ERROR RESPONSE BACK TO ", client_address," : ", error_code,"\n")
    client_socket.send(error_msg)
    return


def my_recv(s):
    
    s.setblocking(0)
    s.settimeout(0.5)
    timeout = 0.5
    temp = b''
    response = b''

    begin = time.time()

    while True:
        if len(response) != 0 and time.time() - begin > timeout:
            break

        elif time.time() - begin > timeout*2:
            break

        try:    
            temp = s.recv(10000)
            if len(temp) != 0:
                response = response + temp
                begin = time.time()
        except:    
            pass

    return response


def ok_response(packet, host, port, client_socket,client_address):

    print("SENDING REQUEST OF ",client_address," : ",packet[0:pl],"\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(packet)
    
    response = my_recv(s)
    s.close()
    print("RESPONSE BACK TO ",client_address," : ", response[0:pl],"\n")
    client_socket.sendall(response)
    return


def main(client_socket, client_address):

    buffer = b''
    while True:
        data = client_socket.recv(50*1024)
        buffer = buffer + data
        if buffer.find(b'\r\n\r\n') > 0:
            print("RECEIVED FROM ",client_address," : ", buffer[0:pl])
            packet, host, port, error = validate(buffer)

            if error != "0":
                error_response(error, client_socket, client_address)
            else:
                ok_response(packet, host, port, client_socket,client_address)
            client_socket.close()
            break


def acceptor():
    temp = 0
    while True:
        client_socket, client_address = server_socket.accept()
        x = threading.Thread(target=main, args=(client_socket,client_address))
        x.start()


if __name__ == "__main__":

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the address to be reusable, to avoid waiting for a while if the program
    # crashed while the socket was open.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set the server address
    server_socket.bind(("127.0.0.21", 2121))

    server_socket.listen(100)
    print("Waiting for clients...\n")

    acceptor()
