from langgraph.graph import START, StateGraph, END # Removed MessagesState import as it's not directly used now
from tools.file_mapper import map_files
from tools.dependency_parser import parse_dependencies
from tools.markdown_generator import generate_markdown
from typing import Annotated, TypedDict, List, Dict, Any # Corrected imports
from langgraph.graph.message import AnyMessage, add_messages

# Define the state structure using TypedDict WITHOUT __init__
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    directory: str
    files: Dict[str, str]  # Use Dict for better type hinting
    dependencies_map: Dict[str, Any] # Add missing state keys used later
    markdown_docs: Dict[str, str]    # Add missing state keys used later

# --- State Functions ---
# Use the specific State type hint
def file_mapping_state(state: State) -> State:
    """State function that maps files from the provided directory."""
    print("--- Running file_mapping_state ---") # Added for debugging
    directory = state["directory"]
    print(f"Mapping files in directory: {directory}") # Added for debugging
    files = map_files(directory)
    state["files"] = files
    print(f"Mapped files: {list(files.keys())}") # Added for debugging
    return state

def dependency_mapping_state(state: State) -> State:
    """State function that uses the LLM to extract dependencies from each file."""
    print("--- Running dependency_mapping_state ---") # Added for debugging
    # Access state directly, not via payload
    files = state["files"]
    dependencies_map = {}
    print(f"Parsing dependencies for {len(files)} files...") # Added for debugging
    for file_name, content in files.items():
        deps = parse_dependencies(file_name, content)
        dependencies_map[file_name] = deps
    # Update state directly
    state["dependencies_map"] = dependencies_map
    print("Finished parsing dependencies.") # Added for debugging
    return state

def markdown_generation_state(state: State) -> State:
    """State function that generates Markdown documentation based on file content and dependencies."""
    print("--- Running markdown_generation_state ---") # Added for debugging
    # Access state directly, not via payload
    files = state.get("files", {}) # Use .get for safety if needed, though should exist
    dependencies_map = state.get("dependencies_map", {}) # Use .get for safety
    markdown_docs = {}
    print(f"Generating markdown for {len(dependencies_map)} files...") # Added for debugging
    for file_name, deps in dependencies_map.items():
        content = files.get(file_name, "") # Use .get for safety
        if content: # Only generate if content exists
            markdown = generate_markdown(file_name, content, deps)
            markdown_docs[file_name] = markdown
        else:
            print(f"Warning: Content not found for file {file_name} during markdown generation.")
    # Update state directly
    state["markdown_docs"] = markdown_docs
    print("Finished generating markdown.") # Added for debugging
    return state

# --- Graph Building ---
def build_agent_graph(directory: str) -> Dict[str, str]:
    """
    Builds and runs the LangGraph state graph using function-based states.

    The graph flows from:
      START -> file_mapping_state -> dependency_mapping_state -> markdown_generation_state -> END

    Returns the final markdown_docs dictionary from the state.
    """
    # Initialize state as a dictionary conforming to the State TypedDict
    initial_state: State = {
        "directory": directory,
        "messages": [],       # Initialize messages list
        "files": {},          # Initialize files dict
        "dependencies_map": {}, # Initialize dependencies_map dict
        "markdown_docs": {}   # Initialize markdown_docs dict
    }

    # Define the sequence of state functions using the State TypedDict.
    builder = StateGraph(State) # Use the State TypedDict here

    # Add nodes
    builder.add_node("file_mapping_state", file_mapping_state)
    builder.add_node("dependency_mapping_state", dependency_mapping_state)
    builder.add_node("markdown_generation_state", markdown_generation_state)

    # Define edges
    builder.add_edge(START, "file_mapping_state")
    builder.add_edge("file_mapping_state", "dependency_mapping_state")
    builder.add_edge("dependency_mapping_state", "markdown_generation_state")
    builder.add_edge("markdown_generation_state", END)

    # Instantiate the state graph.
    graph = builder.compile()
    print("Graph compiled. Invoking...") # Added for debugging

    # Invoke the graph with the dictionary initial_state
    final_state = graph.invoke(initial_state)
    print("Graph invocation complete.") # Added for debugging
    # print(f"Final state: {final_state}") # Optional: Print final state for inspection

    # Access the final result directly from the final_state dictionary
    return final_state.get("markdown_docs", {})