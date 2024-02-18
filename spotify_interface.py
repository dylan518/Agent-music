import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from fuzzywuzzy import process
import re
import requests

class SpotifyHelper:
    # Class to manage interactions with the Spotify API
    
    def __init__(self, client_id="5945bee02e274a7daf17a1f7569063f3", client_secret="a828cbcf4df443fa854acb8aef8d164b"):
        # Initialize the helper with Spotify API credentials
        
        self.client_id = client_id
        self.client_secret = client_secret
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotify = spotipy.Spotify(auth_manager=auth_manager)
        self.redirect_uri = "http://localhost:3000/callback"  # Match this URI with the one set in the Spotify API Dashboard
        self.playlist_id = None 
        self.access_token = None
    
    def set_user_id(self, user_id):
        # Set the user ID for the current session
        self.user_id = user_id
    
    def set_access_token(self, access_token):
        # Set the access token for the current session
        self.access_token = access_token
    
    def get_access_token(self):
        # Get the current session's access token
        return self.access_token
    
    def set_playlist_id(self, playlist_id):
        # Set the playlist ID for the current session
        self.playlist_id = playlist_id
    
    def create_playlist(self, playlist_name):
        # Create a new playlist with the given name for the current user
        try:
            playlist = self.spotify.user_playlist_create(self.spotify.current_user()['id'], playlist_name)
            self.set_playlist_id(playlist['id'])
            return playlist['id']
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None

    def search_track(self, track_name, artist_name=None):
        # Search for a track by name and optional artist name on Spotify
        search_query = f"track:{track_name}"
        if artist_name:
            search_query += f" artist:{artist_name}"

        all_tracks = self.spotify.search(q=track_name, type='track')['tracks']['items']
        if all_tracks:
            best_match = process.extractOne(track_name, [track['name'] for track in all_tracks])
            if best_match[1] >= 80:
                track_uri = all_tracks[0]['uri']

                track_code_pattern = re.compile(r'spotify:track:([a-zA-Z0-9]+)')
                match = track_code_pattern.search(track_uri)

                if match:
                    return match.group(1)
                else:
                    return None
        else:
            return None

    def add_song_to_playlist(self, playlist_id, track_uri):
        # Add a song by URI to the given Spotify playlist
        self.spotify.playlist_add_items(playlist_id, items=[track_uri])

    def remove_song_from_playlist(self, playlist_id, track_uri):
        # Remove a song by URI from the given Spotify playlist
        self.spotify.playlist_remove_all_occurrences_of_items(playlist_id, items=[track_uri]) 

    def get_songs_from_playlist(self, playlist_id):
        # Retrieve a list of tracks from the given Spotify playlist
        results = self.spotify.playlist_items(playlist_id)
        tracks = results['items']

        songs = []

        while tracks:
            for item in tracks:
                track = item['track']
                track_name = track['name']
                artist_name = track['artists'][0]['name']  # Assuming the first artist
                songs.append((track_name, artist_name))

            tracks = self.spotify.next(results)

        return songs

    def play_song(self, track_uri):
        # Prepare track information for playing on the front-end using Spotify Web Playback SDK
        # This method does not play the song directly but returns the track URI for handling by the front-end.
        return track_uri
    
    def get_access_token(self):
        # Get the current session's access token
        return self.access_token

    def exchange_code_for_token(self, code):
        # Exchange an authorization code for an access token
        token_endpoint = "https://accounts.spotify.com/api/token"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(token_endpoint, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.set_access_token(token_data)
            return token_data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error during token exchange: {http_err}")
        except Exception as err:
            print(f"Unexpected error during token exchange: {err}")

        return None
