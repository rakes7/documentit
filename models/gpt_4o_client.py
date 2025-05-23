import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Model:
    """
    Represents a wrapper around an OpenAI client that can call a GPT-4–style model.
    """

    def __init__(self):
        # In a real scenario, you might pass an API key or other credentials.
        API_KEY = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=API_KEY)

    def call_gpt(self, prompt: str) -> str:
        """
        Call the GPT-4–style model with the provided prompt and return a text response.
        Uses the chat completion endpoint which is correct for gpt-4o models.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        # Extract the text from the message content
        return response.choices[0].message.content

    def call_gpt_for_json(self, prompt: str) -> dict:
        """
        Call gpt4o and expect a JSON response.
        We first call 'call_gpt' to get a text response, then try to parse it as JSON.
        If parsing fails, we return an empty dict. In a production system, you would
        want more robust error handling or retry logic.
        """
        response_text = self.call_gpt(prompt)
        try:
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            # Optionally, handle the error or retry in a real implementation.
            return {}