# Personal AI Study & Coding Assistant

A local AI-powered study and coding assistant built with Python, Ollama, Qwen3, SQLite, ChromaDB, embeddings, RAG, web search, and an agent-based tool system.

The assistant can answer normal questions, remember user information, search personal documents, perform calculations, search the web for current information, and automatically choose the appropriate tool.

---

## Features

- Local AI chat using Ollama and Qwen3
- Conversation history
- Persistent user memory using SQLite
- Automatic memory extraction
- Memory search
- PDF document search
- Retrieval-Augmented Generation (RAG)
- Vector database using ChromaDB
- Local embeddings using `nomic-embed-text`
- Web search for current information
- Safe calculator tool
- Agent-based tool selection
- Multi-step tool execution
- Tool error handling and recovery
- Fast-path routing for common requests
- Response timing and tool usage tracking
- Explicit commands for memory, PDF, and web search
- Configurable model and storage paths
- Git-ready project structure

---

## Architecture

```text
                    User
                      |
                      v
                  main.py
                      |
                      v
                Fast Router
                      |
             +--------+--------+
             |                 |
        Fast Path          AI Agent
             |                 |
             |          Tool Selection
             |                 |
             |       +---------+---------+
             |       |         |         |
             v       v         v         v
        Calculator Memory     PDF       Web
                    |          |         |
                    v          v         v
                  SQLite   ChromaDB   DDGS
                               |
                               v
                          Embeddings
                               |
                               v
                         Ollama/Qwen3