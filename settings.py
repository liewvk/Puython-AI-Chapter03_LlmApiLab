# settings.py

OLLAMA_HOST = "http://localhost:11434"

MODEL_NAME = "qwen3.5:9b"

TIMEOUT_SECONDS = 600

DEFAULT_TEMPERATURE = 0.3

DEFAULT_MAX_TOKENS = 250

SYSTEM_PROMPT = """
You are a helpful Python programming assistant.

Explain concepts clearly and accurately.
Use beginner-friendly language.
Give concise responses unless more detail is requested.
Do not invent information when uncertain.
"""
