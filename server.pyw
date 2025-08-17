from flask import Flask, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SPOTIFY_CLIENT_ID = "32cb09be3eda43068429665877f6b2ee"
SPOTIFY_CLIENT_SECRET = "a528c93b03a5481b8841f4191b298425"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing"
))

def get_current_song():
    """Hakee tällä hetkellä soitettavan kappaleen Spotifysta"""
    current_track = sp.currently_playing()
    if current_track and current_track["item"]:
        artist = current_track["item"]["artists"][0]["name"]
        song = current_track["item"]["name"]
        album_cover = current_track["item"]["album"]["images"][0]["url"]
        return {"song": song, "artist": artist, "albumCover": album_cover}
    return {"song": "Ei soitettavaa kappaletta", "artist": "", "albumCover": ""}

@app.route('/song')
def song():
    return jsonify(get_current_song())

if __name__ == '__main__':
    app.run(port=5000, debug=True)