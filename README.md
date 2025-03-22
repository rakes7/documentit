# documentit

This repository contains an agent built using LangGraph that generates software documentation. It:

- Explores a given root folder for files (Python, Java, Terraform, etc.).
- Uses an LLM (gpt4o) to parse each file and extract its dependencies.
- Generates a Markdown file for each file documenting its content and dependencies.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. run agent:
    python main.py --directory path/to/your/project
