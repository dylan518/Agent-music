import time
from spotify_interface import SpotifyHelper

class SpotifyQueue:
    """A class to manage a queue of Spotify tracks and play them in sequence."""

    def __init__(self, spotify_helper):
        """
        Initializes the Spotify queue.

        Args:
            spotify_helper: Instance of SpotifyHelper.
        """
        self.spotify_helper = spotify_helper
        self.queue = []
        self.current_track_index = 0

    def add_to_queue(self, track_uri):
        """Adds a track to the queue by URI."""
        # Retrieve track duration from Spotify
        track_info = self.spotify_helper.spotify.track(track_uri)
        duration_ms = track_info['duration_ms']
        self.queue.append({'uri': track_uri, 'duration': duration_ms})

    def play_next_track(self):
        """Plays the next track in the queue if available."""
        if self.current_track_index < len(self.queue):
            track_info = self.queue[self.current_track_index]
            track_uri = track_info['uri']
            self.spotify_helper.play_song(track_uri)
            # Sleep for the duration of the current track
            time.sleep(track_info['duration'] / 1000.0)
            self.current_track_index += 1
        else:
            print("End of queue reached or no tracks in queue.")

    def play_queue(self):
        """Plays through the entire queue of tracks."""
        while self.current_track_index < len(self.queue):
            self.play_next_track()

if __name__ == '__main__':
    # Example usage:
    spotify_helper = SpotifyHelper('your_client_id', 'your_client_secret', 'your_access_token')
    spotify_queue = SpotifyQueue(spotify_helper)

    # Add some test URIs to the queue
    spotify_queue.add_to_queue('spotify:track:4iV5W9uYEdYUVa79Axb7Rh')
    spotify_queue.add_to_queue('spotify:track:1301WleyT98MSxVHPZCA6M')

    # Play through the queue
    spotify_queue.play_queue()
