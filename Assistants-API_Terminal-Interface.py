from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import logging


#configure logging to display http request-response at DEBUG level
#be casutions with logs, they expose a lot of info
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("openai")
logger.setLevel(logging.DEBUG)

# Load environment variables from the .env file
load_dotenv()  # Load environment variables from .env file

assistant_id = os.getenv("ASSISTANT_ID")
OPENAI_API_KEY = os.getenv("THE_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Verify that the environment variables have been loaded properly
if not OPENAI_API_KEY or not assistant_id:
    raise ValueError("API key or Assistant ID environment variables not set.")


def start_conversation():
    # Start the conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation.")
            break

        # Create a Thread with the initial user message
        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": user_input}]
        )

        # Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Check the Run status and wait for the completion
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(f"Run status: {run.status}")
            time.sleep(1)

        # List Messages to get the Assistant's Response
        thread_messages = client.beta.threads.messages.list(thread.id)

        # Display the Assistant's Response
        for msg in thread_messages.data:
            if msg.role == "assistant":
                # Assuming the response has a 'text' attribute for simplicity
                if isinstance(msg.content, dict) and 'text' in msg.content:
                    print(f"Assistant: {msg.content['text']}")
                else:
                    print(f"Assistant: {msg.content}")

# Let's start the conversation!
if __name__ == "__main__":
    start_conversation()
