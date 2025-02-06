# SmallShell

## 1. Introduction
**Purpose**  
SmallShell is a Linux shell integrated with an LLM to enable users to perform system tasks via natural language. It eliminates the need to memorize Linux commands by translating queries into commands, executing them securely, and presenting results in human-readable formats.

**Scope**  
- Natural language processing (NLP) for command generation.  
- Secure command execution with user consent.  
- Translation of command outputs into user-friendly summaries.  
- Configurable settings and history tracking.  

---

## 2. Architecture
### 2.1 Overview
SmallShell comprises five modules:  
1. **User Interface (UI)**  
2. **Natural Language Processing (NLP) Engine**  
3. **Command Execution Manager**  
4. **Result Translation Module**  
5. **Configuration & History Module**  

### 2.2 Component Details
#### **User Interface**  
- **CLI Prompt**: `SmallShell> ` for input.  
- **Commands**:  
  - `exit`: Terminate the shell.  
  - `history`: View past commands/results.  
  - `config`: Modify settings.  

#### **NLP Engine**  
- **LLM Integration**: Use OpenAI API or a local model (e.g., Llama 2) to convert queries to commands.  
- **Caching**: Store frequent queries to reduce API calls.  
- **Security**: Mask sensitive data (e.g., passwords) before sending to external APIs.  

#### **Command Execution Manager**  
- **Permission Workflow**:  
  ```python
  user_query = "how big is my hard drive?"
  generated_command = "df -h /"
  print(f"Generated command: {generated_command}\nExecute? [y/N]")
  ```  
- **Execution**: Use `subprocess.run()` with timeouts and error handling.  

#### **Result Translation Module**  
- Convert technical outputs (e.g., `df -h`) into summaries (e.g., "Your hard drive is 75% full").  
- Leverage LLM for output interpretation.  

#### **Configuration & History Module**  
- **Config File**: YAML-based settings (e.g., default LLM, auto-execute).  
- **History**: SQLite database storing queries, commands, and results.  

---

## 3. Technical Specifications
### 3.1 Tools & Libraries  
- **Python 3.8+** with libraries:  
  - `argparse` (CLI parsing), `requests` (API calls), `pyyaml` (config).  
  - `sqlite3` (history), `subprocess` (command execution).  
- **LLM**: OpenAI API or DeepSeek with Ollama for local models.  

### 3.2 Security  
- **Input Sanitization**: Prevent command injection via regex checks.  
- **Local Model Option**: Avoid external API dependencies for sensitive environments.  
- **Allow List Commands**: Only commands in the allow list can be executed by the shell.
---

## 4. Challenges & Mitigations
- **Accuracy**: Test LLM-generated commands against common queries (e.g., `df` for disk usage).  
- **Latency**: Cache frequent queries and use lightweight local models.  
- **Safety**: Always prompt before executing commands like `rm` or `chmod`.  

---

## 5. Future Enhancements
1. **Multi-Step Queries**: Support chained commands (e.g., "Compress logs older than 7 days").  
2. **Plugin System**: Allow custom command templates.  
3. **User Feedback**: Improve LLM accuracy by letting users correct commands.  

---

## 6. Testing Plan
- **Unit Tests**: Validate command generation, execution, and result translation.  
- **Integration Tests**: End-to-end workflow (e.g., "What’s my CPU usage?" → `mpstat` → summary).  
- **User Testing**: Gather feedback on usability and edge cases.  

---

## 7. Timeline
- **Phase 1 (Research)**: 2 weeks (LLM selection, architecture).  
- **Phase 2 (Core Development)**: 3 weeks (UI, execution manager).  
- **Phase 3 (NLP Integration)**: 3 weeks (LLM API/local model).  
- **Phase 4 (Testing)**: 2 weeks.  
- **Phase 5 (Deployment)**: 1 week (Packaging, docs).  

---

## 8. Conclusion
SmallShell bridges the gap between natural language and Linux commands, prioritizing security and usability. Future iterations will expand functionality while maintaining robust error handling and user control.  

**Documentation**: Include setup guides, examples, and security best practices.  
**License**: Open-source (MIT License).
