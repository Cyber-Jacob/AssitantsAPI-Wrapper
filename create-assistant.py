from dotenv import load_dotenv
from openai import OpenAI
import openai
import os

load_dotenv() 

openai.api_key = os.getenv("THE_API_KEY")

client = OpenAI()

###
##
#


assistant = client.beta.assistants.create(
        name="Interpreter Assistant 1",
        instructions="You are a clever assistant that parses input for instructions and translates them  into code whenever possible. If there are not code instructions, respond with insightful and clever responses in the form of comments or devising a way to otherwise break out of regular programming format. Be direct, be insightful, and be helpful",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],    
        model="gpt-4-1106-preview"
)
