from dotenv import load_dotenv

from anthropic import Anthropic
load_dotenv()

client = Anthropic()
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

# Add the initial user question
# add_user_message(messages, "Define quantum computing in one sentence")
user_input = input(">: ")   

add_user_message(messages, user_input)

# Get Claude's response
final_answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, final_answer)

print(final_answer)