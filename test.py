try:
    x = re.match(r'(.*:)([0-9]*)?')
    host_name = x.group(1)[0:-1]
    port = x.group(2)
except:

    pass
print(host_name)
print(port)
