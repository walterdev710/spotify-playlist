import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lxml
from dotenv import find_dotenv, load_dotenv
import os

date_inp = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date_inp}/"

env_path = find_dotenv()
load_dotenv(env_path)
MY_SPOTIFY_ID = os.getenv("SPOTIFY_ID")
MY_SPOTIFY_SECRET = os.getenv("SPOTIFY_SEC")
REDIRECTING_URI = "http://localhost"
SPOTIFY = "https://api.spotify.com/v1/me"

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECTING_URI,
        client_id=MY_SPOTIFY_ID,
        client_secret=MY_SPOTIFY_SECRET,    
        show_dialog=True,
        cache_path=".cache"
    )
)
user_id = sp.current_user()["id"]



response = requests.get(url=URL)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "lxml")
music_titles = soup.find_all(name="h3", id="title-of-a-story")


list_titles = []

for music_title in music_titles:
    title = music_title.getText()
    stripped = title.strip()
    list_titles.append(stripped)
    

song_uris = []
year = date_inp.split("-")[0]
for song in list_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)        
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")
        
print(song_uris)

play_list =sp.user_playlist_create(user=user_id,name=f"{date_inp} Billboard 100", public=False )
print(play_list)

sp.user_playlist_add_tracks(user=user_id, playlist_id=play_list["id"], tracks=song_uris)

