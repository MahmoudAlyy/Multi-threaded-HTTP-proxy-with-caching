import re

print(re.match(r'[a-zA-z-]*\:.*', "Accept-Encoding: gzip, deflate"))
print(re.match(r'.*\: .*', "Accept-Encoding: gzip, deflate"))


line = "Cats are smarter than dogs"

matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

print(matchObj)
