import requests
import json
from ollama import chat
from ollama import ChatResponse

def parse_json_script(json_script):
    try:
        data = json.loads(json_script)
        return data.get('command', None)
    except json.JSONDecodeError:
        return None

def extract_bash_script(message_content):
    lines = message_content.split("\n")
    script_lines = []
    inside_code_block = False

    for line in lines:
        if line.strip() == "```bash":
            inside_code_block = True
            continue
        if line.strip() == "```" and inside_code_block:
            break
        if inside_code_block:
            script_lines.append(line)

    return "\n".join(script_lines)

def get_unix_command(english_sentence):
    prompt = 'Please translate the following English sentence to \
      a Unix command to be executed in bash. Please just output the command itself \
      at the end in the format ```bash command ```: ' + english_sentence
    response = chat(model='deepseek-r1:latest', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    command = extract_bash_script(response.message.content)
    return (command, response.message.content) 

# Example usage
if __name__ == "__main__":
    sentence = "List all files in the current directory"
    command, reason = get_unix_command(sentence)
    print(f"Command: {command}, Reason: {reason}")
