from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool

# Set up Wikipedia API wrapper
api_wrapper = WikipediaAPIWrapper(
    top_k_results=2 ,                # number of results to fetch
    doc_content_chars_max=1000      # max characters from each article
)

wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def calculate_division(x: float, y: float) -> float:
    """Calculate division of x by y."""
    return x/y

@tool
def get_user_info(name: str, age: int, occupation: str) -> str:
    """Stores user information."""
    return f"Stored user name: {name}, age: {age}, occupation: {occupation}"

@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b
