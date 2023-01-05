import re

with open('qqq.txt', 'r') as file:
    data = file.read()


q = r'"file_id": "\S*"'
res = re.findall(q, data)
file_id = res[-1].split(' ')[-1].strip('"')