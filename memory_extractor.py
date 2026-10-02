def extract_memory(text):

    text = text.strip()
    lower_text = text.lower()

    # --------------------------------
    # Programming language
    # --------------------------------

    if lower_text.startswith("i am learning "):

        value = text[len("I am learning "):].strip()

        if value:
            return "language", value


    # --------------------------------
    # Goal
    # --------------------------------

    if lower_text.startswith("my goal is "):

        value = text[len("My goal is "):].strip()

        if value:
            return "goal", value


    # --------------------------------
    # Preference
    # --------------------------------

    if lower_text.startswith("i prefer "):

        value = text[len("I prefer "):].strip()

        if value:
            return "preference", value


    # --------------------------------
    # Editor / Tool
    # --------------------------------

    if lower_text.startswith("i use "):

        value = text[len("I use "):].strip()

        if value:
            return "tool", value


    return None