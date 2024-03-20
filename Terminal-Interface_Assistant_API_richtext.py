from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from rich.console import Console

# Create a rich console object
console = Console()

# Load environment variables from the .env file
load_dotenv()

# Assign script variables from .env file
assistant_id = os.getenv("ASSISTANT_ID")
OPENAI_API_KEY = os.getenv("THE_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def start_conversation():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            console.print("Ending the conversation.", style="bold red")
            break

        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": user_input}]
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            time.sleep(0.3)

        thread_messages = client.beta.threads.messages.list(thread.id)

        for msg in thread_messages.data:
            if msg.role == "assistant":
                formatted_response = ""
                if isinstance(msg.content, list):
                    for content_part in msg.content:
                        if hasattr(content_part, 'text') and hasattr(content_part.text, 'value'):
                            formatted_response = content_part.text.value
                            formatted_response = formatted_response.replace("\\n", "\n").replace("```", "")
                            console.print(formatted_response, style="green")
                else:
                    console.print("Received response in unexpected format.", style="bold yellow")


if __name__ == "__main__":
    start_conversation()
