# main.py

import json

from ollama import ResponseError

from httpx import (
    ConnectError,
    TimeoutException
)

from settings import (
    MODEL_NAME,
    SYSTEM_PROMPT
)

from ollama_api import OllamaApiService


def create_messages(question, system_prompt=SYSTEM_PROMPT):

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]


def display_statistics(response):
    """Display selected Ollama response metadata."""

    print("\n--- RESPONSE STATISTICS ---")

    print("Model:", response.model)

    prompt_tokens = getattr(
        response, "prompt_eval_count", None
    )

    output_tokens = getattr(
        response, "eval_count", None
    )

    duration = getattr(
        response, "total_duration", None
    )

    if prompt_tokens is not None:
        print("Input tokens:", prompt_tokens)

    if output_tokens is not None:
        print("Output tokens:", output_tokens)

    if duration is not None:
        seconds = duration / 1_000_000_000

        print(
            f"Total duration: {seconds:.2f} seconds"
        )

    print("---------------------------")


def basic_request(service):
    """Demonstrate a simple AI API request."""

    question = input(
        "\nEnter your question: "
    ).strip()

    if not question:
        print("A question is required.")
        return

    messages = create_messages(question)

    response = service.chat(messages)

    print("\nAssistant:")
    print(response.message.content or "")

    display_statistics(response)


def compare_temperature(service):
    """Compare two generation settings."""

    question = (
        "Suggest three creative names for "
        "a Python AI programming club."
    )

    messages = create_messages(question)

    print("\nQUESTION:")
    print(question)

    print("\nTemperature = 0.0")

    response1 = service.chat(
        messages,
        temperature=0.0,
        max_tokens=180
    )

    print(response1.message.content or "")

    print("\nTemperature = 0.8")

    response2 = service.chat(
        messages,
        temperature=0.8,
        max_tokens=180
    )

    print(response2.message.content or "")

    print("\nThe responses may vary.")
    print(
        "Temperature changes sampling behavior, "
        "but does not guarantee different output."
    )


def structured_json(service):
    """Extract information into structured JSON."""

    student_text = (
        "Alice is 20 years old and is studying "
        "Python and Mathematics."
    )

    # Define the expected JSON structure.
    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "age": {
                "type": "integer"
            },
            "courses": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [
            "name",
            "age",
            "courses"
        ],
        "additionalProperties": False
    }

    messages = [
        {
            "role": "system",
            "content": (
                "Extract only the explicitly stated "
                "student information. "
                "Do not invent missing values. "
                "Return the required JSON object."
            )
        },
        {
            "role": "user",
            "content": student_text
        }
    ]

    response = service.chat(
        messages,
        temperature=0.0,
        max_tokens=180,
        response_format=schema
    )

    raw_text = response.message.content or ""

    student = json.loads(raw_text)

    # Validate the fields before using them.
    if not isinstance(student, dict):
        raise ValueError(
            "Expected a JSON object."
        )

    if (
        not isinstance(student.get("name"), str)
        or type(student.get("age")) is not int
        or not isinstance(
            student.get("courses"), list
        )
        or not all(
            isinstance(course, str)
            for course in student["courses"]
        )
    ):
        raise ValueError(
            "Unexpected student JSON structure."
        )

    print("\nOriginal Text:")
    print(student_text)

    print("\nStructured JSON:")
    print(
        json.dumps(
            student,
            indent=4
        )
    )

    print("\nExtracted Values:")
    print("Name:", student["name"])
    print("Age:", student["age"])
    print(
        "Courses:",
        ", ".join(student["courses"])
    )


def streaming_request(service):
    """Display generated text progressively."""

    question = input(
        "\nEnter a question for streaming: "
    ).strip()

    if not question:
        print("A question is required.")
        return

    messages = create_messages(question)

    print("\nAssistant:")

    stream = service.stream_chat(messages)

    parts = []
    last_chunk = None

    for chunk in stream:

        last_chunk = chunk

        text = chunk.message.content or ""

        if text:
            print(text, end="", flush=True)
            parts.append(text)

    print()

    if not parts:
        print("No response text was generated.")

    if last_chunk is not None:
        display_statistics(last_chunk)


def conversation_demo(service, history):
    """Demonstrate multi-turn conversation context."""

    question = input(
        "\nConversation question: "
    ).strip()

    if not question:
        print("A question is required.")
        return

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": question
    })

    response = service.chat(messages)

    answer = response.message.content or ""

    if not answer.strip():
        raise ValueError(
            "Ollama returned an empty answer."
        )

    print("\nAssistant:")
    print(answer)

    # Save only successful exchanges.
    history.append({
        "role": "user",
        "content": question
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    # Keep the four most recent exchanges.
    history[:] = history[-8:]


def display_menu():

    print("\n===================================")
    print("       PYTHON LLM API LAB")
    print("===================================")

    print("1. Basic AI request")
    print("2. Compare temperature settings")
    print("3. Structured JSON extraction")
    print("4. Streaming response")
    print("5. Multi-turn conversation")
    print("6. Clear conversation history")
    print("0. Exit")


def main():

    print("Python LLM and API Laboratory")
    print("Visual Studio 2026")
    print("Model:", MODEL_NAME)

    service = OllamaApiService()

    conversation_history = []

    while True:

        display_menu()

        choice = input(
            "\nSelect an option: "
        ).strip()

        if choice == "0":
            print("Goodbye!")
            break

        try:

            if choice == "1":
                basic_request(service)

            elif choice == "2":
                compare_temperature(service)

            elif choice == "3":
                structured_json(service)

            elif choice == "4":
                streaming_request(service)

            elif choice == "5":
                conversation_demo(
                    service,
                    conversation_history
                )

            elif choice == "6":
                conversation_history.clear()

                print(
                    "Conversation history cleared."
                )

            else:
                print("Invalid menu option.")

        except ResponseError as ex:

            print("\nOllama API error:")
            print(ex)

            print(
                "Check the model name and "
                "Ollama server."
            )

        except ConnectError:

            print("\nCannot connect to Ollama.")

            print(
                "Verify that the local server "
                "is running at localhost:11434."
            )

        except TimeoutException:

            print("\nThe AI request timed out.")

            print(
                "Try a smaller model or "
                "reduce the response length."
            )

        except (ValueError, KeyError) as ex:

            print("\nResponse processing error:")
            print(ex)

        except Exception as ex:

            print("\nUnexpected error:")
            print(ex)


if __name__ == "__main__": main()
