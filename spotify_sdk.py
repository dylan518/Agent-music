class SpotifySDK:
    """A class to interact with the Spotify Web Playback SDK."""

    def __init__(self, access_token):
        """Initializes the SpotifySDK with the provided access token."""
        self.access_token = access_token

    def play_track(self, track_uri, device_id=None):
        """Starts playing the selected track URI on the specified device using the Web Playback SDK."""
        # This method should be implemented in the front end using the Spotify Web Playback SDK.
        # The backend should only provide track URIs to the front end.
        pass  # No backend logic, purely frontend implementation
