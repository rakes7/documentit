import argparse
from langgraph_agent import build_agent_graph
from tools.file_writer import write_markdown_docs

def main():
    parser = argparse.ArgumentParser(description="Generate documentation for a project folder.")
    parser.add_argument("--directory", required=True, help="Path to the main folder to document")
    args = parser.parse_args()

    # Build the documentation using the LangGraph agent
    markdown_docs = build_agent_graph(args.directory)

    # Write markdown docs into a new folder under the input directory
    write_markdown_docs(markdown_docs, args.directory)

    # For demonstration, print the markdown output for each file.
    for file_name, markdown in markdown_docs.items():
        print(f"--- Documentation for {file_name} ---")
        print(markdown)
        print("\n")

if __name__ == "__main__":
    main()