from typing import Dict, List
import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))
import os
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

system_instructions = """
You are a conversational AI designed to summarize chat histories. You will be provided with chat messages from various channels, each organized by the channel name. Your task is to summarize the content of each channel separately. The summary should capture the main topics discussed, any important events, and the general tone of the conversation. 

The output should be structured as a JSON object where the keys are the channel names and the values are the summaries of the conversations within those channels. Be concise but ensure that all significant details are included in each summary.
"""
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=system_instructions
)

async def send_to_gemini_api(messages: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Example function to send messages to the Google Gemini model API.
        example output:
        {
            "general": "The conversation in the 'general' channel started with casual greetings, with users discussing their busy schedules. The conversation then shifted towards a shared interest in a new series, with user4 expressing their enthusiasm for the latest episode and user1 confirming they watched it and enjoyed the plot twists.",
            "random": "The 'random' channel focused on a recent sports game, with users discussing the outcome and their reactions. User5 and user6 shared their excitement about the game's intensity and the close final score. User7 expressed regret for missing the game and user5 provided details about the home team's overtime win."
        }
    """
    try:
        response = model.generate_content(create_prompt(messages))
        # Check if the response has valid content before processing
        if not response or not response.text:
            raise ValueError("Received empty or invalid response from Google Gemini API")
        cleaned_response = response.text.strip().strip('```').strip('json').strip('\n')
        expected_channels = list(messages.keys())
        summary_dict = clean_response(cleaned_response, expected_channels)
        # summary_dict: Dict[str, str] = json.loads(cleaned_response)
        return summary_dict
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON. Response: {response.text}, Error: {str(e)}")
        raise ValueError("Failed to parse the JSON response from the API.")


def create_prompt(messages_dict: Dict[str, List[str]]) -> str:
    prompt = "Here are chat histories for each channel. Please summarize the conversations and provide the output as a JSON object with only the following channel names:\n\n"
    prompt += "{\n"
    for channel in messages_dict.keys():
        prompt += f'    "{channel}": "Summary of the {channel} channel...",\n'
    prompt += "}\n\n"
    prompt += "Here are the chat histories for each channel:\n\n"
    for channel, messages in messages_dict.items():
        prompt += f"# {channel}\n"
        prompt += "\n".join(messages)
        prompt += "\n\n"
    return prompt

def clean_response(response: str, expected_channels: List[str]) -> Dict[str, str]:
    """
    Cleans up the response to ensure it only contains the expected channels as keys.
    """
    try:
        summary_dict = json.loads(response)
        cleaned_summary = {channel: summary_dict.get(channel, "") for channel in expected_channels}
        return cleaned_summary
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON. Response: {response}, Error: {str(e)}")
        raise ValueError("Failed to parse the JSON response from the API.")