# AI Travel Planner Agent

An AI-powered travel planning agent built to explore modern AI engineering patterns, including:

* LLM orchestration
* Planning and execution workflows
* Tool integration
* Retrieval-Augmented Generation (RAG)
* Semantic memory
* Structured outputs

The goal is to build a controllable and extensible AI agent that can generate personalized travel itineraries.

---

## Architecture

The agent uses a planner-controlled workflow:

```
User Request
      |
      v
   Agent
      |
      v
  Planner
      |
      v
Execution Plan
      |
      v
PlanExecutor
      |
      v
   Tools
      |
      v
Tool Results
      |
      v
    LLM
      |
      v
Final Response
```

The planner decides **what actions should happen**, the executor performs those actions, and the LLM generates the final answer using the collected information.

---

## Project Structure

```
travel-agent/
│
├── app.py                  # Application entry point and dependency wiring
├── agent.py                # Agent orchestration workflow
├── llm.py                  # LLM client wrapper
├── prompts.py              # Prompt templates
│
├── planning/
│   ├── planner.py          # Creates execution plans
│   └── models.py           # Planning models
│
├── execution/
│   └── plan_executor.py    # Executes planned actions
│
├── tools/
│   ├── tool_registry.py    # Tool registration
│   ├── tool_executor.py    # Tool execution
│   └── weather_tool.py     # Weather capability
│
├── memory/                 # Semantic memory storage and retrieval
├── rag/                    # Knowledge retrieval components
├── travel/                 # Travel-specific logic
├── models/                 # Shared data models
│
├── tests/
├── requirements.txt
└── README.md
```

---

## Components

| Component    | Responsibility                                         |
| ------------ | ------------------------------------------------------ |
| Agent        | Coordinates planning, execution, memory, and LLM calls |
| Planner      | Creates executable plans from user requests            |
| PlanExecutor | Executes planned steps                                 |
| Tools        | Provide external capabilities                          |
| RAG          | Retrieves travel knowledge                             |
| Memory       | Stores user preferences                                |
| LLM          | Generates plans and final responses                    |

---

## Current Capabilities

### Planning

Creates structured execution plans that determine:

* required actions
* tool usage
* execution order

### Tools

Current tools include:

* Weather lookup
* Knowledge search (RAG)

### Memory

Stores user preferences for personalization.

Example:

```
Interest:
hiking_nature

Preference:
Enjoys hiking and nature-focused activities
```

---

## Future Improvements

* Add explicit plan step types (`tool`, `user_input`, `reasoning`, `final_answer`)
* Add replanning after execution feedback
* Improve vector-based memory retrieval
* Expand tools (maps, flights, hotels, restaurants)
* Improve testing coverage

---

## Goal

This project is a learning platform for designing AI agents with clear separation between:

```
Planning  ->  Execution  ->  Generation
```

making the system easier to debug, test, and extend.

```
```
