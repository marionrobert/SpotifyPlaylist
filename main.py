import requests
from bs4 import BeautifulSoup

specialdate = input("Which special date do you want to travel to ? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{specialdate}/"

response = requests.get(URL)
# print(response.status_code)
data = response.content
# print(data)
