from langchain.agents import AgentExecutor
from langchain_core.agents import AgentFinish
from langchain.tools import tool
from spotify_interface import SpotifyInterface
from langchain_core.agents import AgentFinish
from langchain.tools import tool
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.memory import ConversationBufferMemory
from openai import OpenAI
import time
import os
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
import time



def string_wrapper(string):
    if string is None:
        return "Output is None. The function returned nothing so this the default string."
    if not isinstance(string, str):
        return "Output is not a string"
    return string  # Or process the string as needed


class CustomAgent():

    @tool
    @staticmethod
    def qeue_songs(song_name,artist):
        """Suggests songs to add to a Spotify playlist.

        Args:
            name of song: The ID of the Spotify playlist.
            optional: the artist

        Returns:
            A list of tuples containing (track_name, artist_name).
        """
        spotify = SpotifyInterface()
        spotify.search_track(song_name,artist)
        spotify.add_song_to_playlist(playlist_id, track_uri)
        return self.get_songs_from_playlist(playlist_id)
    
    @tool
    @staticmethod
    def deqeue_songs(playlist_id,track_uri):
        """Removes a song from a Spotify playlist.

        Args:
            playlist_id: The ID of the Spotify playlist.
            track_uri: The Spotify track URI.
        """
        spotify = SpotifyInterface()
        spotify.remove_song_from_playlist(playlist_id, track_uri)
        return "Song removed from playlist."

class BaseAgentRunner:

    def __init__(self, custom_agent, thread_id=None):
        OPENAI_API_KEY = "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"

        def _handle_error(error) -> str:
            return str(error)[:50]

        self.custom_agent = custom_agent
        self.custom_tools = self.generate_tools()
        self.user_messages = []
        self.messages = []
        os.environ[
            "OPENAI_API_KEY"] = "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"
        memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent = OpenAIAssistantRunnable.create_assistant(
            name="code_editor",
            instructions="Work with the use to write and debugg code.",
            tools=self.custom_tools,
            model="gpt-4-1106-preview",
            as_agent=True,
            verbose=True,
            max_iterations=10,
            memory=memory,
        )
        self.thread_id = thread_id

    def generate_tools(self):
        tools = [
            getattr(self.custom_agent, attr) for attr in dir(self.custom_agent)
            if callable(getattr(self.custom_agent, attr))
            and not attr.startswith('__')
        ]
        return tools

    def execute_agent(self, agent, tools, input):
        time.sleep(1)
        tool_map = {tool.name: tool for tool in tools}
        response = self.agent.invoke(input)
        while not isinstance(response, AgentFinish):
            tool_outputs = []
            for action in response:
                tool_output = tool_map[action.tool].invoke(action.tool_input)
                print(action.tool, action.tool_input, tool_output, end="\n\n")
                tool_outputs.append({
                    "output": tool_output,
                    "tool_call_id": action.tool_call_id
                })
            response = agent.invoke({
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id,
            })
            self.thread_id = action.thread_id

        return response

    def main(self):
        user_input = input("Request here: ")
        self.user_messages.append(user_input)
        data = {"content": user_input, "max_iterations": 5}

        if self.thread_id:
            data["thread_id"] = self.thread_id
        response = self.execute_agent(self.agent, self.generate_tools(), data)
        print(response.return_values)
        self.messages.append(response.return_values)


if __name__ == "__main__":
    custom_agent = CustomAgent()
    agent_runner = BaseAgentRunner(custom_agent)
    while (True):
        agent_runner.main()
