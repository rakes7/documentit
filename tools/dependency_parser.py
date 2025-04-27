# tools/dependency_parser.py

from models.gpt_4o_client import Model

def parse_dependencies(file_name: str, file_content: str) -> list:
    """
    Use gpt4o to parse the file and extract its dependencies.
    The prompt is constructed with the file content.
    """
    model = Model()

    prompt = (
        f"Analyze the following file: {file_name}\n\n"
        f"Content:\n{file_content}\n\n"
        "Extract all external dependencies from this file. External dependencies include:\n"
        "- Python import statements (e.g., 'import numpy', 'from pandas import DataFrame')\n"
        "- Package references in requirements\n"
        "- External libraries or frameworks used\n\n"
        "Return ONLY a valid JSON array of strings with the base package names, without versions or submodules.\n"
        "For example: [\"numpy\", \"pandas\", \"requests\"]\n\n"
        "Do not include:\n"
        "- Standard library modules (like os, sys, datetime)\n"
        "- Internal/relative imports (from .module import X)\n"
        "- Comments or explanations\n\n"
        "Return only the JSON array."
    )
    response = model.call_gpt(prompt)
    
    # Parse the JSON response
    import json
    try:
        dependencies = json.loads(response.strip())
        return dependencies
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return []
