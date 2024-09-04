from typing import Dict, List
import google.generativeai as genai
import json
from dotenv import load_dotenv
load_dotenv('../../.env')
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



def send_to_gemini_api(messages: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Example function to send messages to the Google Gemini model API.
        example output:
        {
            "general": "The conversation in the 'general' channel started with casual greetings, with users discussing their busy schedules. The conversation then shifted towards a shared interest in a new series, with user4 expressing their enthusiasm for the latest episode and user1 confirming they watched it and enjoyed the plot twists.",
            "random": "The 'random' channel focused on a recent sports game, with users discussing the outcome and their reactions. User5 and user6 shared their excitement about the game's intensity and the close final score. User7 expressed regret for missing the game and user5 provided details about the home team's overtime win."
        }
    """
    response = model.generate_content(create_prompt(messages))
    cleaned_response = response.text.strip().strip('```').strip('json').strip('\n')
    summary_dict:Dict[str, str] = json.loads(cleaned_response)
    return summary_dict


def create_prompt(messages_dict: Dict[str, List[str]]) -> str:
    prompt = "Here are chat histories from various channels. Please summarize the conversations in each channel and provide the output as a JSON object.\n\n"
    for channel, messages in messages_dict.items():
        prompt += f"# {channel}\n"
        prompt += "\n".join(messages)
        prompt += "\n\n"
    prompt += "Please provide the summary in the following JSON format:\n"
    prompt += "{\n"
    for channel in messages_dict.keys():
        prompt += f'    "{channel}": "Summary of the {channel} channel...",\n'
    prompt += "}\n"
    
    return prompt