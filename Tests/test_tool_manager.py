from tool_manager import execute_tool


result = execute_tool(
    "calculate",
    {
        "expression": "25 * 16"
    }
)

print("Result:", result)