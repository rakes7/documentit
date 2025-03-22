import os

def write_markdown_docs(markdown_docs: dict, base_path: str, output_folder_name="docs"):
    """
    Writes markdown documentation files to a new folder under the given base path.
    
    Each Markdown file is created based on the key (original file path) from markdown_docs.
    The output folder is created if it does not exist.
    
    Args:
        markdown_docs (dict): A dictionary mapping file paths to markdown content.
        base_path (str): The base directory where the output folder will be created.
        output_folder_name (str): The name of the folder to create (default is "docs").
    """
    output_path = os.path.join(base_path, output_folder_name)
    os.makedirs(output_path, exist_ok=True)
    
    for file_path, markdown_content in markdown_docs.items():
        # Create a unique file name for the markdown file.
        filename = os.path.basename(file_path)
        markdown_filename = f"{filename}.md"
        file_output_path = os.path.join(output_path, markdown_filename)
        
        try:
            with open(file_output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"Written: {file_output_path}")
        except Exception as e:
            print(f"Error writing {file_output_path}: {e}")
