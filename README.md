# Multi-Threaded HTTP proxy with caching
Implementation of multi-threaded HTTP proxy server that accepts a GET request and makes it on behalf of the client. The HTTP proxy returns the response if succeeded to the client and cache it, an 400 for Bad request (Realtive Url is provided with no Host header, Headers not properly formatted) and an 501 for methods other than GET. 

Once the proxy has parsed the URL, it can make a connection to the requested host (using the appropriate remote port, or the default of 80 if none is specified) and send the HTTP request for the appropriate resource. The proxy always send the request in the relative URL + Host header format regardless of how the request was received from the client.
#
Accept from client:  
GET http://eng.alexu.edu.eg/ HTTP/1.0  
Or  
GET / HTTP/1.0  
Host: eng.alexu.edu.eg

Send to remote server:  
GET / HTTP/1.0  
Host: eng.alexu.edu.eg  
(Additional client specified headers, if any...)
# 
Handles port number provided in Path or in the Host header  
Accept from client:  
GET http://info.cern.ch:80/hypertext/WWW/TheProject.html HTTP/1.1

Send to remote sever:  
GET /hypertext/WWW/TheProject.html HTTP/1.1  
Host: info.cern.ch:80  





