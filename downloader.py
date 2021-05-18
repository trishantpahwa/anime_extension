import requests
from json import loads

data = {}
with open('naruto-dub-.json', 'r') as f:
    data = loads(f.read())

def download(name, url):
    r = requests.get(url, allow_redirects=True)
    open('naruto/' + name, 'wb').write(r.content)

for key, value in data.items():
    if int(key) > 100:
        download(key + '.mp4', value)
