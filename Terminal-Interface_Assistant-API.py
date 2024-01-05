from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables from the .env file
load_dotenv()

#assign script variables from Env variables placed by our .env file. In this example, the
#"THE_API_KEY" variable is our api key. We also call our Preferred Assistant by its' ID, also stored in .env for security
assistant_id = os.getenv("ASSISTANT_ID")
OPENAI_API_KEY = os.getenv("THE_API_KEY")
 
#the api_key= script is important, because otherwise the OpenAI lib looks for an environmental variable using this call:
#(OPENAI default behavior is to search for an environmental var with: os.getenv("OPENAI_API_KEY")
#In our case, our env variable has a separate name of "THE_API_KEY"

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def start_conversation():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation.")
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
            time.sleep(1)

        thread_messages = client.beta.threads.messages.list(thread.id)

        for msg in thread_messages.data:
            if msg.role == "assistant":
                formatted_response = ""
                if isinstance(msg.content, list):
                    for content_part in msg.content:
                        if hasattr(content_part, 'text') and hasattr(content_part.text, 'value'):
                            formatted_response = content_part.text.value
                            formatted_response = formatted_response.replace("\\n", "\n").replace("```", "")
                            print(formatted_response)
                else:
                    # If the response content is not in the expected list format,
                    # print a fallback message
                    print("Received response in unexpected format.")


if __name__ == "__main__":
    start_conversation()
