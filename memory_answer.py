from memory import get_memory


def answer_from_memory(question):
    question = question.lower().strip()

    # -----------------------------------------
    # Language
    # -----------------------------------------

    if (
        "programming language" in question
        or "what language am i learning" in question
        or "what am i learning" in question
    ):
        value = get_memory("language")

        if value:
            return f"You're learning {value}."

    # -----------------------------------------
    # Goal
    # -----------------------------------------

    if (
        "what is my goal" in question
        or "what's my goal" in question
    ):
        value = get_memory("goal")

        if value:
            return f"Your goal is {value}."

    # -----------------------------------------
    # Tool / Editor
    # -----------------------------------------

    if (
        "what tool do i use" in question
        or "what editor do i use" in question
    ):
        value = get_memory("tool")

        if value:
            return f"You use {value}."

    # -----------------------------------------
    # Preference
    # -----------------------------------------

    if (
        "what is my preference" in question
        or "what do i prefer" in question
    ):
        value = get_memory("preference")

        if value:
            return f"Your preference is {value}."

    return None