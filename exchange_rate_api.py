import requests
import json

url = 'APİ'

response = requests.get(url) #request urlden veri çeker 
data = response.json()

# print(data)


