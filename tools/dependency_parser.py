# tools/dependency_parser.py

from models.gpt4o_client import Model

def parse_dependencies(file_name: str, file_content: str) -> list:
    """
    Use gpt4o to parse the file and extract its dependencies.
    The prompt is constructed with the file content.
    """
    model = Model()

    prompt = (
        f"Analyze the following file: {file_name}\n\n"
        f"Content:\n{file_content}\n\n"
        "List all external dependencies (e.g., imported modules, packages, libraries, or references) "
        "in JSON format as a list. For example: [\"dependency1\", \"dependency2\"]"
    )
    response = model.call_gpt4o(prompt)
    
    print(response)
    #  parse the JSON response.

    return []
