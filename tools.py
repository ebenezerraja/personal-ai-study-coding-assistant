from web_search import search_web
from datetime import datetime
import ast
import operator
from embedder import create_embedding
from vector_store import search_documents
from memory import search_memories


def calculate(expression: str) -> str:
    """
    Safely calculate a mathematical expression.

    Supports:
    +, -, *, /, //, %, **, and parentheses.
    """

    try:
        # Remove Qwen thinking markers
        expression = expression.replace("/think", "").strip()

        # Limit expression length
        if len(expression) > 100:
            return "Expression is too long."

        # Convert expression into an AST
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            # Numbers
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError("Only numbers are allowed.")

            # Binary operations
            if isinstance(node, ast.BinOp):

                left = evaluate(node.left)
                right = evaluate(node.right)

                operations = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.FloorDiv: operator.floordiv,
                    ast.Mod: operator.mod,
                    ast.Pow: operator.pow
                }

                operation = operations.get(type(node.op))

                if operation is None:
                    raise ValueError("Operation not allowed.")

                # Prevent extremely large exponent calculations
                if isinstance(node.op, ast.Pow):
                    if abs(right) > 100:
                        raise ValueError("Exponent is too large.")

                return operation(left, right)

            # Positive and negative numbers
            if isinstance(node, ast.UnaryOp):

                value = evaluate(node.operand)

                if isinstance(node.op, ast.UAdd):
                    return +value

                if isinstance(node.op, ast.USub):
                    return -value

                raise ValueError("Unary operation not allowed.")

            raise ValueError("Invalid mathematical expression.")

        result = evaluate(tree.body)

        return str(result)

    except ZeroDivisionError:
        return "Cannot divide by zero."

    except Exception:
        return "I couldn't calculate that expression."

def pdf_search(query: str) -> str:
    """
    Search the user's PDF documents for relevant information.

    Args:
        query: The question or topic to search for.

    Returns:
        Relevant document passages.
    """

    try:
        query_embedding = create_embedding(query)

        results = search_documents(
            query_embedding,
            number_of_results=3
        )

        documents = results.get("documents", [[]])[0]

        if not documents:
            return "No relevant information was found in the PDF."

        output = ""

        for i, document in enumerate(documents, start=1):
            output += f"""
Document passage {i}:
{document}
"""

        return output

    except Exception as e:
        return f"PDF search error: {e}"

def memory_search(query: str) -> str:
    """
    Search the user's stored memories for information relevant
    to the user's question.

    Args:
        query: The user's question or search topic.

    Returns:
        Relevant stored memories.
    """

    try:
        memories = search_memories(query)

        if not memories:
            return "No relevant memories were found."

        output = ""

        for i, (key, value) in enumerate(memories, start=1):
            output += f"""
Memory {i}
Key: {key}
Value: {value}
"""

        return output

    except Exception as e:
        return f"Memory search error: {e}"

def web_search(query: str) -> str:
    """
    Search the web for current or recent information.

    Args:
        query: The search query.

    Returns:
        Relevant web search results with titles,
        descriptions, and URLs.
    """

    current_date = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().year

    freshness_words = [
        "latest",
        "current",
        "today",
        "recent",
        "now",
        "newest"
    ]

    search_query = query

    query_lower = query.lower()

    # Make version questions more precise
    if "latest version" in query_lower:
        if "python" in query_lower:
            search_query = (
                f"site:python.org/downloads/ "
                f"{query} latest stable officially released version "
                f"{current_year}"
            )
        else:
            search_query = (
                f"{query} latest stable officially released version "
                f"official {current_year}"
            )

    # Add the current date for other time-sensitive questions
    elif any(word in query_lower for word in freshness_words):
        search_query = f"{query} {current_date} {current_year}"

    results = search_web(
        search_query,
        max_results=5
    )

    if not results:
        return "No web search results were found."

    output = ""

    for i, result in enumerate(results, start=1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        description = result.get("description", "No description")

        output += f"""
    Result {i}
    Title: {title}
    Description: {description}
    URL: {url}
    """

    return output