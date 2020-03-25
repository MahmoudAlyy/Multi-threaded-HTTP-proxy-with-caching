# Multi-Threaded HTTP proxy with caching
Implementation of multi-threaded HTTP proxy server that accepts a GET request and makes it on behalf of the client. The HTTP proxy returns the response if succeeded to the client and cache it, an 400 for Bad request (Realtive Url is provided with no Host header, Headers not properly formatted) and an 501 for methods other than GET. 

Once the proxy has parsed the URL, it can make a connection to the requested host (using the appropriate remote port, or the default of 80 if none is specified) and send the HTTP request for the appropriate resource. The proxy always send the request in the relative URL + Host header format regardless of how the request was received from the client.
#
Accept from client:  
GET www.google.com/ HTTP/1.1  
Or   
GET www.google.com/ HTTP/1.1    
Host:  
or  
GET / HTTP/1.1  
Host: www.google.com  

Send to remote server:  
GET / HTTP/1.1  
Host: www.google.com  
(Additional client specified headers, if any...)
# 
Handles port number provided in Path or in the Host header  
Accept from client:  
GET http://info.cern.ch:80/hypertext/WWW/TheProject.html HTTP/1.1

Send to remote sever:  
GET /hypertext/WWW/TheProject.html HTTP/1.1  
Host: info.cern.ch:80   
#
Configured Firefox to use it as its web proxy on 127.0.0.21 : 2121  
Tested Websites :    
http://www.apache.org/   
http://info.cern.ch
http://www.columbia.edu/~fdc/sample.html  
http://www.csszengarden.com/  
http://eng.alexu.edu.eg/  

# ScreenShot

![Imgur](https://i.imgur.com/3lFPceF.png)






