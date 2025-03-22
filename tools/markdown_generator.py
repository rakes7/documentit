# tools/markdown_generator.py

from models.gpt4o_client import call_gpt4o

def generate_markdown(file_name: str, file_content: str, dependencies: list) -> str:
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
    markdown = call_gpt4o(prompt)
    return markdown
