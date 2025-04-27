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
        "Extract ONLY internal project module/script dependencies from this file. These include:\n"
        "- Relative imports (e.g., 'from .module import X', 'from ..utils import Y')\n"
        "- Absolute imports that reference project-specific modules (e.g., 'from project_name.module import Z')\n"
        "- Any other references to files or modules that appear to be part of the same project\n\n"
        "Return ONLY a valid JSON array of strings with the full import paths.\n"
        "For example: [\".module\", \"..utils\", \"project_name.module\"]\n\n"
        "Do not include:\n"
        "- Standard library modules (like os, sys, datetime)\n"
        "- External/third-party library imports (like numpy, pandas, requests)\n"
        "- Comments or explanations\n\n"
        "Return only the JSON array."
    )
    response = model.call_gpt(prompt)
    
    # Parse the JSON response
    import json
    try:
        print(f"Raw response: {response}")  # Debugging output

        dependencies = json.loads(response.strip())
        print(f"Dependencies for {file_name}: {dependencies}")  # Debugging output

        return dependencies
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return []
