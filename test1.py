import requests

url = "https://www.google.com"
res = requests.get(url)
print(res.status_code)
#print(res.text)