import json
import ast
author = "12342142131"
username = '13"21321'
passwd = '3213213'
username = username.replace("'", "\\'").replace('"', '\\"')
js = '{\
        "discordID": "'+author + '",\
        "valuse": {\
            "username": "'+username+'",\
            "password": "'+passwd+'"\
    }}'
print(js)
print(json.loads((js)))
