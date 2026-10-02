from tools import calculate


expressions = [
    "25 * 16",
    "100 / 4",
    "(10 + 5) * 4",
    "2 ** 5",
    "100 / 0",
    "25 * 16 /think",
    "hello"
]


for expression in expressions:

    result = calculate(expression)

    print(f"Expression: {expression}")
    print(f"Result: {result}")
    print("-" * 50)