import requests
try:
    response = requests.post("https://labs.selfmade.ninja/api/app/authorize")
except requests.ConnectionError as r:
    print("Internal")
