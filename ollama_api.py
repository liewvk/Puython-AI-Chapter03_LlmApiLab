# ollama_api.py

from ollama import Client

from settings import (
    OLLAMA_HOST,
    MODEL_NAME,
    TIMEOUT_SECONDS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS
)


class OllamaApiService:

    def __init__(self):

        self.client = Client(
            host=OLLAMA_HOST,
            timeout=TIMEOUT_SECONDS
        )

    def chat(
        self,
        messages,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
        response_format=None
    ):
        """Send a complete chat request to Ollama."""

        response = self.client.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=False,
            think=False,
            format=response_format,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        return response

    def stream_chat(self, messages):
        """Return a stream of response chunks."""

        return self.client.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            think=False,
            options={
                "temperature": DEFAULT_TEMPERATURE,
                "num_predict": 350
            }
        )
