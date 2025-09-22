import requests

url = "https://en.wikipedia.org/w/api.php"

# query = GET
# 
params = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnnamespace": 0,
    "rnlimit": 1
}

headers = {
    "User-Agent": "progettino-flask/1.0 (esteban.storelli@samtrevano.ch)"
}

response = requests.get(url, params=params, headers=headers)

data = response.json()
pages = data["query"]["pages"]
# .values() = dizionario di tutte le pagine
#
page = next(iter(pages.values()))

print(page["extract"])