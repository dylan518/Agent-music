from langchain.tools import tool
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from spotify_interface import SpotifyInterface
class CustomAgent():

    @tool
    @staticmethod
    def add_song_to_queue(song_name:str):
        """Adds songs to Spotify queue. Decide which songs should be added to queue

        Args:
            name of song:Name of Spotify spotify song to add to queue.
        """
        spotify = SpotifyInterface()
        return "Song added to queue:"+str(spotify.add_song_to_queue(song_name))
    
    @tool
    @staticmethod
    def remove_song_from_queue(song_name:str):
        """Removes a song from a Spotify playlist. Dequeue songs as you see fit especially if the mood is not right or the queue is too long.

        Args:
            song_name: The name of the song to remove from the queue.
        """
        spotify = SpotifyInterface()
        return "Song remove from queue" +(str(spotify.remove_song_from_queue(song_name)))