import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

#confirm .env is setup correctly, and that we can view the assistant ID object properties we will interact with. If this works, our .env is setup and we can start sending requests

client = OpenAI(
    api_key=os.getenv("THE_API_KEY")
)
assistant_id = os.getenv("ASSISTANT_ID")

something = client.beta.assistants.retrieve(assistant_id)
print(something)
