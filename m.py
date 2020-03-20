import socket
import re
"""
GET /hypertext/WWW/TheProject.html HTTP/1.0
HOST: http://info.cern.ch


GET / HTTP/1.1
Host: www.google.com

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
# my error stuff works (appears on webpage) but not on valid stuff maybe need to do multitaksing


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
        #print("ERORR format enterd is worng")
        return None, None, None, "400 Bad Request"

    # #TODO want to seprate them so we can see both error messages
    # if not (method == "GET" and version == "HTTP/1.1"):
    #     #print( "Not Implemented (501) method or version")
    #     return None, None, None, "501 Not Implemented"

    #print(path)
    ### if full path is provided will split to relative URL + Host header
    if path[0] != "/" and method == "GET":
        x = re.match(r'(https?:\/\/)?(.+?)(:[0-9]*)?(\/.*)', path)
        #2 host name, 3 prot number, 4 relative path

        # not used for now
        #x = re.match(r'(https:\/\/)?(http:\/\/)?(.+?)(:[0-9]*)?(\/.*)', path)
        # 1 https , 2 http , 3 host name , 4 port number , 5 relative path

        if x.group(2):
            host_name = x.group(2)
            host_header = host_name
        port = 80  # set default port
        if x.group(3):
            port = x.group(3)[1:]
            host_header = host_name + x.group(3)

        relative_url = x.group(4)

    ### FOR COONECT?b'CONNECT
    if path[0] != "/" and method == "CONNECT":
        x = re.match(r'(https?:\/\/)?(.+?)(:[0-9]*)', path)
        #2 host name, 3 prot number, 4 relative path

        # not used for now
        #x = re.match(r'(https:\/\/)?(http:\/\/)?(.+?)(:[0-9]*)?(\/.*)', path)
        # 1 https , 2 http , 3 host name , 4 port number , 5 relative path

        if x.group(2):
            host_name = x.group(2)
            host_header = host_name
        port = 80  # set default port
        if x.group(3):
            port = x.group(3)[1:]
            host_header = host_name + x.group(3)

        #relative_url = x.group(4)


        ### see if request header was provided if yes remove it
        for item in request_headers:
            if item.find("Host:") != -1:
                request_headers.remove(item)
                break

        ### add the host header
        host_header = "Host: "+host_header
        request_headers.append(host_header)
        if method == "GET":
            path = relative_url

    ### if realtive url is provided then there must exist a host header
    else:
        host_header_flag = False
        for item in request_headers:
            if item.find("Host:") != -1:
                host_header_flag = True
                break
        if not host_header_flag:
            #print("bad request 400 missing host name")
            return None, None, None, "400 Bad Request"

    ### Validate request header
    ### check if headers are  properly formatted
    for item in request_headers:
        if not (re.match(r'.*\: .*', item)):
            #print("400 header not properly formatted")
            return None, None, None, "400 Bad Request"

#    print(method,path,version)
#    print(request_headers)

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
    #TODO add content lenght later butw will try without it for naw

    size = str(len(html.encode()))
    crlf = b'\r\n'

    error_msg = b'HTTP/1.1 ' + error_code.encode() + crlf + b'Content-Type: text/html; charset=UTF-8' + crlf + b'Content-Length: '+size.encode() + crlf + crlf

    error_msg = error_msg + html.encode() + b'\n'
    print(error_msg)
    

    ### TESTTTTTTTTTTTTT
    by = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nReferrer-Policy: no-referrer\r\nContent-Length: 1567\r\nDate: Fri, 20 Mar 2020 15:34:45 GMT\r\n\r\n<!DOCTYPE html>\n<html lang=en>\n  <meta charset=utf-8>\n  <meta name=viewport content="initial-scale=1, minimum-scale=1, width=device-width">\n  <title>Error 404 (Not Found)!!1</title>\n  <style>\n    *{margin:0;padding:0}html,code{font:15px/22px arial,sans-serif}html{background:#fff;color:#222;padding:15px}body{margin:7% auto 0;max-width:390px;min-height:180px;padding:30px 0 15px}* > body{background:url(//www.google.com/images/errors/robot.png) 100% 5px no-repeat;padding-right:205px}p{margin:11px 0 22px;overflow:hidden}ins{color:#777;text-decoration:none}a img{border:0}@media screen and (max-width:772px){body{background:none;margin-top:0;max-width:none;padding-right:0}}#logo{background:url(//www.google.com/images/branding/googlelogo/1x/googlelogo_color_150x54dp.png) no-repeat;margin-left:-5px}@media only screen and (min-resolution:192dpi){#logo{background:url(//www.google.com/images/branding/googlelogo/2x/googlelogo_color_150x54dp.png) no-repeat 0% 0%/100% 100%;-moz-border-image:url(//www.google.com/images/branding/googlelogo/2x/googlelogo_color_150x54dp.png) 0}}@media only screen and (-webkit-min-device-pixel-ratio:2){#logo{background:url(//www.google.com/images/branding/googlelogo/2x/googlelogo_color_150x54dp.png) no-repeat;-webkit-background-size:100% 100%}}#logo{display:inline-block;height:54px;width:150px}\n  </style>\n  <a href=//www.google.com/><span id=logo aria-label=Google></span></a>\n  <p><b>404.</b> <ins>That\xe2\x80\x99s an error.</ins>\n  <p>The requested URL <code>/dsadas</code> was not found on this server.  <ins>That\xe2\x80\x99s all we know.</ins>\n'
    #client_socket.send(by)

    client_socket.send(error_msg)
    return


def ok_response(packet, host, port, client_socket):
     print(packet,host,port)
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((host, port))
     s.sendall(packet)
     response = s.recv(6400)
     s.close()
     print("RESPONSE : ", response)
     client_socket.sendall(response)
     return


def main():

    print("1************************MAIN**********************************\n")
    buffer = b''
    while True:
        client_socket, client_address = server_socket.accept()
        print("Client : ",client_address, " has arrived")
        #print("*IN WHILE*")
        data = client_socket.recv(50*1024)
        buffer = buffer + data
        if buffer.find(b'\r\n\r\n') > 0:
            print("RECEIVED : ", buffer)
            print(100*"~")
            packet, host, port, error = validate(buffer)
            #if error != "0":
                #print("~~~~~~~~~~~~~~ERROR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #error_response(error, client_socket, client_address)
            #else:
            #print("TEST")
            ok_response(packet, host, port, client_socket)
            buffer = b''
            print("\n2************************MAIN**********************************\n")


if __name__ == "__main__":

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the address to be reusable, to avoid waiting for a while if the program
    # crashed while the socket was open.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set the server address
    server_socket.bind(("127.0.0.21", 2121))

    # Start listening, this makes the socket a "welcome" socket
    # that gives birth to a socket per each connecting client.
    server_socket.listen(100)
    print("Waiting for clients...")
   
    main()
