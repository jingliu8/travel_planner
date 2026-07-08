# AI Travel Planner Agent

A personalized AI-powered travel planning application built to demonstrate modern AI engineering practices. The application generates customized travel itineraries based on user preferences and will gradually incorporate memory, tool calling, retrieval, planning, and agent capabilities.

## Project Structure

```text
travel-agent/
│
├── app.py          # Application entry point
├── config.py       # Loads environment variables and application configuration
├── llm.py          # Wrapper around the OpenAI client for LLM interactions
├── planner.py      # Core business logic for generating travel plans
├── prompts.py      # Centralized prompt templates used by the application
├── models.py       # Pydantic models and data structures
│
├── tools/          # External tools (weather, maps, flights, etc.)
├── memory/         # User preferences and conversation memory
├── data/           # Local knowledge base and RAG resources
├── tests/          # Unit and integration tests
│
├── requirements.txt
├── .env
└── README.md
```

## Responsibilities

| File         | Responsibility                                                                        |
| ------------ | ------------------------------------------------------------------------------------- |
| `app.py`     | Initializes the application, wires components together, and handles user interaction. |
| `config.py`  | Loads API keys, model configuration, and other application settings.                  |
| `llm.py`     | Provides a reusable interface for communicating with the language model.              |
| `planner.py` | Contains the application's business logic for generating travel itineraries.          |
| `prompts.py` | Stores reusable system prompts and prompt templates.                                  |
| `models.py`  | Defines request/response models and validates structured data.                        |
| `tools/`     | Contains integrations with external services and APIs.                                |
| `memory/`    | Stores and retrieves long-term user preferences and conversation context.             |
| `data/`      | Holds local documents and resources used for retrieval.                               |
| `tests/`     | Contains automated tests for application components.                                  |
