# Python AI LLM API Lab

This repository is a small Python lab for experimenting with local LLM access via Ollama. It demonstrates common AI integration patterns such as basic chat requests, temperature comparisons, structured JSON extraction, streaming responses, and multi-turn conversations.

## Project purpose

The code in this project was designed as a hands-on learning example for working with a local language model in Python. It is meant to help beginners understand how to:

- call an LLM through a simple API wrapper
- send system and user messages
- compare generation settings
- parse structured JSON output
- stream text responses incrementally
- maintain a short conversation history

## Included examples

The application in `main.py` includes these menu options:

1. Basic AI request
2. Compare temperature settings
3. Structured JSON extraction
4. Streaming response
5. Multi-turn conversation
6. Clear conversation history
0. Exit

## Repository files

- `main.py` - interactive menu-driven demo application
- `ollama_api.py` - wrapper for the Ollama API service
- `settings.py` - model, host, timeout, and prompt configuration
- `requirements.txt` - Python dependencies

## Requirements

Before running the project, make sure you have:

- Python 3.10+
- Ollama installed and running locally
- a model available in Ollama (the default configuration uses `qwen3.5:9b`)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Open `settings.py` and verify these values:

```python
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "qwen3.5:9b"
TIMEOUT_SECONDS = 600
```

If your Ollama setup is running elsewhere or uses a different model, update the settings before launching the app.

## Run the lab

```bash
python main.py
```

The app will show a menu and let you try each example interactively.

## Notes

This project is intentionally simple and educational. It focuses on the fundamentals of calling an LLM from Python rather than building a production-ready application framework.

## License

This project does not currently declare a license file.
