from dotenv import load_dotenv

from anthropic import Anthropic
load_dotenv()

client = Anthropic(max_retries=3)
model = "claude-sonnet-4-6"

# Helpers functions 
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return "Chat:" + message.content[0].text

# Start with an empty message list
messages = []


add_user_message(messages, "what's the weather in new york?")

# Streaming response from Claude
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,    
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
