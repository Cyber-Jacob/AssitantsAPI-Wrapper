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
    thread = client.beta.threads.create(messages=[])
    console.print("Conversation thread created. Thread ID is " + thread.id + ".", style="bold green")

    last_message_ids = set()  # Set to track processed assistant message IDs
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            console.print("Ending the conversation.", style="bold red")
            break
        
        # Send user message
        user_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        console.print(f"[DEBUG] User Message ID: {user_message.id}", style="yellow")
        
        # Generate the assistant's response
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Wait for the run to complete
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            time.sleep(0.09)
        
        # Retrieve the latest messages
        thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
        console.print(f"[DEBUG] Total messages in thread: {len(thread_messages.data)}", style="yellow")
        
        # Filter out the assistant messages that are new
        new_assistant_messages = [msg for msg in thread_messages.data if msg.role == "assistant" and msg.id not in last_message_ids]

        if new_assistant_messages:
            for msg in new_assistant_messages:
                last_message_ids.add(msg.id)  # Add each message ID to processed set
                latest_message_id = msg.id
            
            # Retrieve the latest assistant message to ensure correctness
            latest_message = client.beta.threads.messages.retrieve(message_id=latest_message_id, thread_id=thread.id)
            console.print(f"[DEBUG] Latest message ID: {latest_message.id}", style="yellow")
            
            formatted_response = ""
            if isinstance(latest_message.content, list):
                for content_part in latest_message.content:
                    if hasattr(content_part, 'text') and hasattr(content_part.text, 'value'):
                        formatted_response += content_part.text.value
                    else:
                        console.print("Received response in unexpected format.", style="bold yellow")
                        continue
            
            formatted_response = formatted_response.replace("\\n", "\n").replace("```", "###")
            console.print(formatted_response, style="green")
        else:
            console.print("[DEBUG] No new assistant messages found.", style="bold red")

if __name__ == "__main__":
    start_conversation()