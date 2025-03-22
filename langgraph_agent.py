# langgraph_agent.py

from langgraph import Graph, Node  # Assuming LangGraph provides these classes.
from tools.file_mapper import map_files
from tools.dependency_parser import parse_dependencies
from tools.markdown_generator import generate_markdown

class FileMappingNode(Node):
    def run(self, input_data: dict) -> dict:
        directory = input_data.get("directory")
        files = map_files(directory)
        return {"files": files}

class DependencyMappingNode(Node):
    def run(self, input_data: dict) -> dict:
        files = input_data.get("files", {})
        dependencies_map = {}
        # Process each file using the LLM node to parse dependencies.
        for file_name, content in files.items():
            deps = parse_dependencies(file_name, content)
            dependencies_map[file_name] = deps
        # Pass both files and dependencies_map to the next node.
        return {"files": files, "dependencies_map": dependencies_map}

class MarkdownGenerationNode(Node):
    def run(self, input_data: dict) -> dict:
        files = input_data.get("files", {})
        dependencies_map = input_data.get("dependencies_map", {})
        markdown_docs = {}
        for file_name, deps in dependencies_map.items():
            content = files[file_name]
            markdown = generate_markdown(file_name, content, deps)
            markdown_docs[file_name] = markdown
        return {"markdown_docs": markdown_docs}

def build_agent_graph(directory: str) -> dict:
    # Instantiate a LangGraph and add nodes in the desired order.
    graph = Graph()
    graph.add_node(FileMappingNode())
    graph.add_node(DependencyMappingNode())
    graph.add_node(MarkdownGenerationNode())

    result = graph.run({"directory": directory})
    return result.get("markdown_docs", {})
