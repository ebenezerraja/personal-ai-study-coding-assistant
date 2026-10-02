from tools import calculate, web_search, pdf_search, memory_search


TOOLS = {
    "calculate": calculate,
    "web_search": web_search,
    "pdf_search": pdf_search,
    "memory_search": memory_search
}


def execute_tool(tool_name, arguments):
    if tool_name not in TOOLS:
        return f"Unknown tool: {tool_name}"

    tool = TOOLS[tool_name]

    try:
        result = tool(**arguments)
        return str(result)

    except Exception as e:
        return f"Tool error: {e}"