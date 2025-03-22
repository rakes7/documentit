# langgraph_agent.py
from langgraph.graph import START, StateGraph, MessagesState, END
from tools.file_mapper import map_files
from tools.dependency_parser import parse_dependencies
from tools.markdown_generator import generate_markdown

def file_mapping_state(state: MessagesState) -> MessagesState:
    """State function that maps files from the provided directory."""
    directory = state.payload.get("directory")
    files = map_files(directory)
    state.payload["files"] = files
    return state

def dependency_mapping_state(state: MessagesState) -> MessagesState:
    """State function that uses the LLM to extract dependencies from each file."""
    files = state.payload.get("files", {})
    dependencies_map = {}
    for file_name, content in files.items():
        deps = parse_dependencies(file_name, content)
        dependencies_map[file_name] = deps
    state.payload["dependencies_map"] = dependencies_map
    return state

def markdown_generation_state(state: MessagesState) -> MessagesState:
    """State function that generates Markdown documentation based on file content and dependencies."""
    files = state.payload.get("files", {})
    dependencies_map = state.payload.get("dependencies_map", {})
    markdown_docs = {}
    for file_name, deps in dependencies_map.items():
        content = files[file_name]
        markdown = generate_markdown(file_name, content, deps)
        markdown_docs[file_name] = markdown
    state.payload["markdown_docs"] = markdown_docs
    return state

def build_agent_graph(directory: str) -> dict:
    """
    Builds and runs the LangGraph state graph using function-based states.
    
    The graph flows from:
      START -> file_mapping_state -> dependency_mapping_state -> markdown_generation_state -> END
      
    Returns the final markdown_docs dictionary from the state payload.
    """
    initial_state = MessagesState(payload={"directory": directory})
    # Define the sequence of state functions.
    steps = [
        file_mapping_state,
        dependency_mapping_state,
        markdown_generation_state,
    ]
    # Instantiate the state graph.
    graph = StateGraph(steps=steps, start=START, end=END)
    final_state = graph.run(initial_state)
    return final_state.payload.get("markdown_docs", {})


