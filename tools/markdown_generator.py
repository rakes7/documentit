# tools/markdown_generator.py

from models.gpt4o_client import call_gpt

def generate_markdown_v1(file_name: str, file_content: str, dependencies: list) -> str:
    """
    Use gpt4o to generate Markdown documentation for the file.
    The prompt includes the file's content and its dependencies.
    """
    prompt = (
        f"Generate documentation for the file '{file_name}'.\n\n"
        f"File Content:\n{file_content}\n\n"
        f"Dependencies:\n{dependencies}\n\n"
        "Write detailed documentation in Markdown format explaining the purpose of the file, its functionality, "
        "and how it interacts with its dependencies."
    )
    markdown = call_gpt(prompt)
    return markdown

def generate_markdown(file_name: str, file_content: str, dependencies: list) -> str:
    """
    Use gpt4o to generate Markdown documentation for the file.
    The prompt includes the file's content and its dependencies.
    """
    prompt = (
        f"Generate comprehensive Markdown documentation for the Python file '{file_name}'.\n\n"
        f"## File Content:\n```python\n{file_content}\n```\n\n"
        f"## Dependencies:\n{dependencies}\n\n"
        f"## Documentation Requirements:\n"
        f"Your goal is to produce clear, accurate, and well-structured Markdown documentation suitable for other developers.\n"
        f"Please include the following sections:\n"
        f"1.  **Overview:** Briefly explain the purpose of this file within the larger project context.\n"
        f"2.  **Key Components / Functionality:** \n"
        f"    * Describe the main classes, functions, or significant code blocks.\n"
        f"    * For each key function/method, explain its purpose, parameters (including types if not obvious), and return value.\n"
        f"    * Explain any complex logic or algorithms used.\n"
        f"3.  **Dependencies Interaction:** \n"
        f"    * Explain *how* this file uses the listed dependencies.\n"
        f"    * Mention specific functions or classes imported from dependencies and their role in this file's operation.\n"
        f"4.  **Usage / Examples (Optional but Recommended):** \n"
        f"    * If applicable, provide a brief code snippet showing how to use the primary functions or classes defined in this file.\n"
        f"5.  **Assumptions / Notes:** \n"
        f"    * Mention any important assumptions the code makes or any potential caveats.\n\n"
        f"Ensure the documentation is written in clear English and uses standard Markdown formatting (e.g., code blocks for code, bolding for emphasis)."
    )
    markdown = call_gpt(prompt)
    return markdown