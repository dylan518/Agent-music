from langchain_core.agents import AgentFinish
from spotify_interface import SpotifyInterface
from langchain_core.agents import AgentFinish
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.memory import ConversationBufferMemory
from openai import OpenAI
import time
import os
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
import time
from agent_tools import CustomAgent




class SpotifyAgentRunner:

    def __init__(self, thread_id=None):
        OPENAI_API_KEY = "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"

        def _handle_error(error) -> str:
            return str(error)[:50]

        self.custom_agent = CustomAgent()
        self.custom_tools = self.generate_tools()
        os.environ[
            "OPENAI_API_KEY"] = "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"
        memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent = OpenAIAssistantRunnable.create_assistant(
            name="code_editor",
            instructions="DJ for the user. Try to queue songs that might match what they want. Queue 3 to 4 songs at a time unless under other specific instructions.",
            tools=self.custom_tools,
            model="gpt-3.5-turbo-0125",
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

    def main(self, queue, messages):
        # Concatenate messages and the queue into a single string
        full_message_str = ". ".join(messages) + ". Queue: " + ", ".join(queue)
        data = {
            "content": full_message_str,
            "max_iterations": 10
        }

        if self.thread_id:
            data["thread_id"] = self.thread_id

        # Now, pass this data to execute_agent, which should expect 'content' to be a string
        response = self.execute_agent(self.agent, self.generate_tools(), data)

        # Assuming response processing is correct, but ensure you're extracting the string correctly
        # The response handling here depends on the structure of the response object
        print(response)
        print(full_message_str)  # Debugging: print the full input message

        # Example of handling the response, adjust based on actual response structure
        if hasattr(response, 'return_values'):
            messages.append(response.return_values["output"])  # Assuming response.return_values is the expected format

        # Return the updated queue and messages
        return SpotifyInterface().get_queue(), messages


