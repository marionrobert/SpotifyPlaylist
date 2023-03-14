import requests
from bs4 import BeautifulSoup

specialdate = input("Which special date do you want to travel to ? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{specialdate}/"

response = requests.get(URL)
# print(response.status_code)
web_data = response.content
# print(web_data)

soup = BeautifulSoup(web_data, "html.parser")
# print(soup.prettify())

all_songs = soup.select("li #title-of-a-story")
print(len(all_songs))

all_song_titles = [song.getText() for song in all_songs]
print(all_song_titles)
