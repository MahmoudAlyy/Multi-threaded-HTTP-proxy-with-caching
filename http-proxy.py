import socket
import re
import threading
import time

pl = 80 #printing length for debugging
cache_map = {}


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
            return None, None, None, "400 Bad Request, Host header not provided"

    ### check if headers are  properly formatted
    for item in request_headers:
        if not (re.match(r'.*\: .*', item)):
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

    print("PROXY RESPONDED WITH AN ERROR TO ", client_address," : ", error_code,"\n")
    client_socket.sendall(error_msg)
    return


def my_recv(s):
    
    s.setblocking(0)
    s.settimeout(0.5)
    timeout = 3
    temp = b''
    response = b''

    begin = time.time()

    while True:
        #if u got a response break after timeout
        if len(response) != 0 and time.time() - begin > timeout:
            break
        
        #if u dont have response yet wait twice the timout
        elif time.time() - begin > timeout*2:
            return 0
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
    try :
        s.connect((host, port))
    except:
        print("ERROR CONNECTING TO HOST, PORT SPECIFIED")
        return
    s.sendall(packet)
    
    response = my_recv(s)
    s.close()
    if response == 0:
        print("ERROR NO RESPONSE FROM REMOTE SERVER")
        return 0
    print("RESPONSE BACK TO ",client_address," : ", response[0:pl],"\n")
    client_socket.sendall(response)
    return response


### if date is in their dont store in cache
def use_cache(request,client_socket):
    if request in cache_map.keys():
        response = cache_map[request]
        print("\n[From Cache] RESPONSE BACK TO ",client_socket.getpeername()," : ", response[0:pl],"\n")
        client_socket.sendall(response)
        return 1
    else :
        return 0


def store_cache(request, response):
    cache_map[request] = response
    return

def main(client_socket, client_address):

    buffer = b''
    while True:
        data = client_socket.recv(50*1024)
        buffer = buffer + data
        if buffer.find(b'\r\n\r\n') > 0 :
            print("RECEIVED FROM ",client_address," : ", buffer[0:pl])
            packet, host, port, error = validate(buffer)

            if error != "0" :
                error_response(error, client_socket, client_address)

            elif use_cache(packet,client_socket) == 0  :
                response = ok_response(packet, host, port, client_socket,client_address)
                if response != 0: # a response exist
                    store_cache(packet,response)

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
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.21", 2121))
    server_socket.listen(100)
    print("\nWaiting for clients...\n")

    acceptor()
