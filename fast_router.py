import re

from tools import calculate


def try_fast_path(question):
    """
    Handle obvious requests without calling the full agent.

    Returns:
        (tool_name, data) if a fast route is detected
        None if the normal agent should handle the question.
    """

    question = question.strip()

    # -------------------------------------------------
    # 1. Explicit calculation requests
    # -------------------------------------------------

    pattern = r"^(calculate|compute|solve)\s+(.+)$"

    match = re.match(pattern, question, re.IGNORECASE)

    if match:
        expression = match.group(2).strip()

        result = calculate(expression)

        return "calculate", result

    # -------------------------------------------------
    # 2. Plain mathematical expressions
    # -------------------------------------------------

    expression_pattern = r"^[0-9\s\+\-\*\/\%\(\)\.\^]+$"

    if re.fullmatch(expression_pattern, question):
        expression = question.replace("^", "**")

        result = calculate(expression)

        return "calculate", result

    # -------------------------------------------------
    # 3. Explicit PDF / document requests
    # -------------------------------------------------

    pdf_patterns = [
        r"\bmy pdf\b",
        r"\bthe pdf\b",
        r"\bfrom my pdf\b",
        r"\bin my pdf\b",
        r"\baccording to my pdf\b",
        r"\bmy document\b",
        r"\bthe document\b",
        r"\bfrom my document\b",
        r"\bin my document\b",
    ]

    if any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in pdf_patterns
    ):
        return "pdf", question

        # -------------------------------------------------
    # 4. Obvious personal-memory requests
    # -------------------------------------------------

    memory_patterns = [
        r"\bwhat is my goal\b",
        r"\bwhat's my goal\b",
        r"\bwhat am i learning\b",
        r"\bwhat am i studying\b",
        r"\bwhat programming language am i learning\b",
        r"\bwhat language am i learning\b",
        r"\bwhat tool do i use\b",
        r"\bwhat editor do i use\b",
        r"\bwhat is my preference\b",
        r"\bwhat do i prefer\b",
    ]

    if any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in memory_patterns
    ):
        return "memory", question

    # -------------------------------------------------
    # 5. Obvious current-information requests
    # -------------------------------------------------

    web_patterns = [
        r"\blatest\b",
        r"\bcurrent\b",
        r"\btoday\b",
        r"\brecent\b",
        r"\bnow\b",
        r"\bcurrently\b",
    ]

    if any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in web_patterns
    ):
        return "web", question

    # -------------------------------------------------
    # 6. Let the normal AI agent handle it
    # -------------------------------------------------

    return None