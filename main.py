import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# SPOTIFY_CLIENT_ID = ffd3501644e84195b76e8a28d554ab07
# SPOTIFY_CLIENT_SECRET = d52d2a56ccaa4ae682c677c7b44dcef

specialdate = input("Which special date do you want to travel to ? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{specialdate}/"

response = requests.get(URL)
# print(response.status_code)
web_data = response.content
# print(web_data)

soup = BeautifulSoup(web_data, "html.parser")
# print(soup.prettify())

all_songs = soup.select("li #title-of-a-story")
# print(len(all_songs))

all_song_titles = [song.getText().replace("\n", "").replace("\t", "") for song in all_songs]
# print(all_song_titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(sp)
print(user_id)
