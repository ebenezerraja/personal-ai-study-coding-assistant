from agent import run_agent


question = """
Search the web for the latest Java version,
then explain whether it is an LTS release.
"""

print("User:", question)

answer = run_agent(question)

print("\nAI:", answer)