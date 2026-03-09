import requests

url = "https://en.wikipedia.org/api/rest_v1/page/summary/OpenAI"
r = requests.get(url)
print(r.json())