import requests
from ollama import chat
from ollama import ChatResponse


def get_unix_command(english_sentence):
    prompt = 'Please translate the following English sentence to \
      a Unix command to be executed in bash. Please just output the command itself in \
      format {command: "example"}: ' + english_sentence
    response = chat(model='deepseek-r1:latest', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    return response['message']['content']

# Example usage
if __name__ == "__main__":
    sentence = "List all files in the current directory"
    command = get_unix_command(sentence)
    print(f"Command: {command}")
