import requests
import certifi

response = requests.get("https://twitter.com", verify=certifi.where())
print(response.status_code)