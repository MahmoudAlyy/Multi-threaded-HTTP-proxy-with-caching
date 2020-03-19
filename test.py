import re
txt ="http://www.princeton.edu/dsadasd"
text = "www.nowhere123.com:30/docs/index.html"
#x = re.match(r'https?:\/\/(.+?)(\/.*)', text)
#x = re.match(r'(https?:\/\/)?(.+?)(\/.*)', text)

x = re.match(r'(https?:\/\/)?(.+?)(:[0-9]*)?(\/.*)', text)

#(https:\/\/)?(http:\/\/)?(.+?)(:[0-9]*)?(\/.*)
# 1 https , 2 http , 3 host name , 4 port number , 5 relative path

# 2 host name, 3 prot number, 4 relative path
#Host: myhost.com:3244
print(x)

print(x.group(2))
print(x.group(4))
print(x.group(3)[1:])
