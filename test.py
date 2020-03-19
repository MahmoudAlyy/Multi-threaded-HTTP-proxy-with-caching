import re
txt ="http://www.princeton.edu/dsadasd"
text = "www.nowhere123.com/docs/index.html"
#x = re.match(r'https?:\/\/(.+?)(\/.*)', text)
#x = re.match(r'(https?:\/\/)?(.+?)(\/.*)', text)

x = re.match(r'(https?: \/\/)?(.+?)(: .*)?(\/ .*)', text)
# 2 host name, 3 prot number, 4 relative path
#Host: myhost.com:3244

print(x.group(2))
print(x.group(3))
