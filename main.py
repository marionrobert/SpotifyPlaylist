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

# get the uri of each song from spotify
song_uris = []
year = specialdate.split("-")[0]

for song in all_song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(song_uris)


# create a spotify playlist
playlist_name = input("How do you want to name your SPOTIFY playlist?\n")
playlist_description = input("Add a description to your playlist or press enter:\n")
playlist = sp.user_playlist_create(user=user_id, name=f"{playlist_name}", public=False, collaborative=False, description=f"{playlist_description}")
playlist_url = playlist["external_urls"]['spotify']
print(f"Here is the link to access your playlist: {playlist_url}")

# add all songs to the playlist thank to their uri
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)