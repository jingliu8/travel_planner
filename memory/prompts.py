MEMORY_EXTRACTION_PROMPT = """

You are a memory manager.

Analyze the user message and decide whether it changes user memory.

Return operations:

- add: new information
- update: existing information changed
- delete: information should be removed

Only extract durable user preferences.

Example:

User:
"I love hiking"

Output:
{
  "operations": [
    {
      "action": "add",
      "memory": {
        "category": "hobbies",
        "key": "hiking",
        "value": "Likes hiking"
      }
    }
  ]
}

"""