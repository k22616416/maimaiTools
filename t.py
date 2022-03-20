import os
import json

fileName = "test.json"
file = open(fileName, "r+")
try:
    with file as f:
        data = json.load(f)
except:
    print("error")
    exit()


file.close()
print(type(data))


author = 'test2'
username = 'user2'
passwd = 'passwd2'

jsonString = '{"'+author+'": {"username": "' + \
    username+'","password": "'+passwd+'"}}'
# jsonString = str.format('{"{0}": {\r\n"username": "{1}",\r\n"password": "{2}"\r\n}}',author, username, passwd)
jsonString = json.loads(jsonString)
for i in data:
    if i == jsonString:
        print('重複')
        exit()
print(jsonString)
data.append(jsonString)

file = open(fileName, "w+")
json.dump(data, file)
file.close()

# jsonFile = open('test.json', 'a+')
# n = jsonFile.read()
# print(n)
# old = json.loads(n)
# print(old)
