from ddgs import DDGS


def search_web(query, max_results=5):

    if not query.strip():
        return []

    try:
        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                results.append({
                    "title": result.get("title", "No title"),
                    "url": result.get("href", ""),
                    "description": result.get("body", "No description")
                })

        return results

    except Exception as e:

        print("Web search error:", e)

        return []