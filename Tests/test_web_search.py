from web_search import search_web


query = "latest Java version"

results = search_web(query)

print("Search results:")
print("=" * 60)

for i, result in enumerate(results, start=1):

    print(f"\nRESULT {i}")
    print("-" * 60)

    print("Title:", result["title"])
    print("URL:", result["url"])
    print("Description:", result["description"])