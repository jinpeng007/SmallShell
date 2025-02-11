import requests
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

def parse_json_script(json_script):
    try:
        data = json.loads(json_script)
        return data.get('command', None)
    except json.JSONDecodeError:
        return None

def extract_blocks(message_content):
    lines = message_content.split("\n")
    script_lines = []
    think_lines = []
    note_lines = []
    inside_code_block = False
    inside_think_block = False
    inside_note_block = False

    for line in lines:
        if line.strip() == "<think>":
            inside_think_block = True
            continue
        if line.strip() == "</think>":
            inside_think_block = False
            continue
        if line.strip() == "<note>":
            inside_note_block = True
            continue
        if line.strip() == "</note>": 
            inside_note_block = False
            continue
        if line.strip() == "```bash" and not inside_think_block: 
            inside_code_block = True
            continue
        if line.strip() == "```" and inside_code_block: 
            inside_code_block = False 
            continue
        if inside_think_block:
            think_lines.append(line)
        if inside_code_block:
            script_lines.append(line)
        if inside_note_block:
            note_lines.append(line)

    return "\n".join(script_lines), "\n".join(think_lines), "\n".join(note_lines) 

def get_linux_command(human_question):
    llm = OllamaLLM(model='deepseek-r1:7b')
    prompt = ChatPromptTemplate.from_template(
      """
      You are an expert on Linux CLI. Please translate the human question in plain English 
      sentence to script to be executed in bash in the simpliest way. Make sure the script only
      does what the user asks for. Avoid using echo or any other unnecessary output formatting commands.
      For example, to show the current hostname, the script should only contain the command `hostname`.
      Use the following command cheatsheet to help you:
      File Commands
ls – directory listing
ls -al – formatted listing with hidden files
cd dir - change directory to dir
cd – change to home
pwd – show current directory
mkdir dir – create a directory dir
rm file – delete file
rm -r dir – delete directory dir
rm -f file – force remove file
rm -rf dir – force remove directory dir *
cp file1 file2 – copy file1 to file2
cp -r dir1 dir2 – copy dir1 to dir2; create dir2 if it
doesn't exist
mv file1 file2 – rename or move file1 to file2
if file2 is an existing directory, moves file1 into
directory file2
ln -s file link – create symbolic link link to file
touch file – create or update file
cat > file – places standard input into file
more file – output the contents of file
head file – output the first 10 lines of file
tail file – output the last 10 lines of file
tail -f file – output the contents of file as it
grows, starting with the last 10 lines
Process Management
ps – display your currently active processes
top – display all running processes
kill pid – kill process id pid
killall proc – kill all processes named proc *
bg – lists stopped or background jobs; resume a
stopped job in the background
fg – brings the most recent job to foreground
fg n – brings job n to the foreground
System Info
date – show the current date and time
cal – show this month's calendar
uptime – show current uptime
w – display who is online
whoami – who you are logged in as
finger user – display information about user
uname -a – show kernel information
cat /proc/cpuinfo – cpu information
cat /proc/meminfo – memory information
man command – show the manual for command
df – show disk usage
du – show directory space usage
free – show memory and swap usage
whereis app – show possible locations of app
which app – show which app will be run by default
Network
hostname – show hostname
ping host – ping host and output results
whois domain – get whois information for domain
dig domain – get DNS information for domain
dig -x host – reverse lookup host
wget file – download file
wget -c file – continue a stopped download
Searching
grep pattern files – search for pattern in files
grep -r pattern dir – search recursively for
pattern in dir
command | grep pattern – search for pattern in the
output of command
locate file – find all instances of file
      If there are multiple commands needed, generate the bash script to use them together that print 
      out the desired output. 
      Please first return a brief note of how the script will work in the format of 

      <note>
      [note_content]
      </note>

      then return the bash script in the format 

      ```bash
      [script_content]
      ```
      at the end: {ask}
      """
    ).format(ask=human_question)
    response = llm.invoke(prompt)
    # print(response)
    
    command, reason, note = extract_blocks(response)
    return (command, reason, note) 

# Example usage
if __name__ == "__main__":
    sentence = "show me my host name"
    command, reason, note= get_linux_command(sentence)
    print(f"Command:\n{command}")
    print(f"\n\nNote:\n{note}")
    print(f"\n\nReason:\n{reason}")
