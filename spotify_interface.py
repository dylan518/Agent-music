import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

"""This module provides a simple interface to the Spotify API for searching and adding songs to a queue."""
class SpotifyInterface:
    _instance = None  # Singleton instance storage
    # The __new__ method is called to create a new instance of a class
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpotifyInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, client_id="5945bee02e274a7daf17a1f7569063f3", client_secret="a828cbcf4df443fa854acb8aef8d164b"):
        if not hasattr(self, '_initialized'):
            self.client_id = client_id
            self.client_secret = client_secret
            auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
            self.queue = []  # Initialize the song queue
            self._initialized = True
    
    def get_client_info(self):
        """Returns the Spotify client ID and secret."""
        return self.client_id, self.client_secret

    def search_track(self, track_name, artist_name=None):
        """Search for a track by name and optional artist name on Spotify."""
        search_query = f"track:{track_name}"
        if artist_name:
            search_query += f" artist:{artist_name}"

        results = self.spotify.search(q=search_query, type='track', limit=1)
        tracks = results.get('tracks', {}).get('items', [])

        if tracks:
            track = tracks[0]  # Assuming the first result is the best match
            return {
                'name': track['name'],
                'artist': ', '.join(artist['name'] for artist in track['artists']),
                'uri': track['uri']
            }
        return None
    
    def add_song_to_queue(self, track_name, artist_name=None):
        """Search for a song by name (and optional artist) and add it to the queue if found."""
        track_info = self.search_track(track_name, artist_name)
        if track_info:
            self.queue.append(track_info)
            return track_info
        return "Song not found."
    
    def remove_song_from_queue(self, track_name, artist_name=None):
        """Search for a song by name (and optional artist) in the queue and remove it if found."""
        track_info = self.search_track(track_name, artist_name)
        if track_info:
            # Attempt to find and remove the song from the queue
            for i, song in enumerate(self.queue):
                if song['uri'] == track_info['uri']:
                    return self.queue.pop(i)
        return "Song not found in queue."
    
    def get_queue(self):
        """Returns the current song queue."""
        return self.queue
