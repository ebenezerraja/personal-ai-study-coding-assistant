def route_question(question):
    question_lower = question.lower().strip()

    # --------------------------------
    # 1. Web questions
    # --------------------------------

    web_keywords = [
        "latest",
        "current",
        "today",
        "recent",
        "news",
        "online",
        "this year",
        "this month"
    ]

    for keyword in web_keywords:
        if keyword in question_lower:
            return "web"

    # --------------------------------
    # 2. PDF / document questions
    # --------------------------------

    pdf_keywords = [
        "according to the pdf",
        "according to the document",
        "in the pdf",
        "in the document",
        "from the pdf",
        "from the document"
    ]

    for keyword in pdf_keywords:
        if keyword in question_lower:
            return "pdf"

    # --------------------------------
    # 3. Normal question
    # --------------------------------

    return "normal"