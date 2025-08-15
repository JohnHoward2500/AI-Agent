**IMPORTANT: This project was created to learn about AI and apply the material I have been studying in a practical project.  NOT DESIGNED FOR REAL WORLD USE**

**Title:** Gemini Coding AI Agent

**Description:**  This is an coding AI agent that is accessed through the terminal.  Its software development tool powered by google gemini that can debug, write, and run code in a provided working directory.
This coding AI Agent can be used to automatically fix bugs, write tests, create documentation, etc as well as can be asked questions like AI chat agents. 

**Requirements:**<br/>
google-genai==1.12.1 <br/>
  python-dotenv=1.1.0

**Quick Start:** <br/>
  Open the AI_Agent directory by typing "cd AI_Agent" in the terminal <br/>
  Initialize the vertual environment by typing "source .venv/bin/activate" in the terminal <br/>
  To use the agent type "uv run main.py 'your_prompt'" in the terminal <br/>
  Optional: to access additional information type --verbose after your prompt  Example: uv run main.py "your_prompt" --verbose
