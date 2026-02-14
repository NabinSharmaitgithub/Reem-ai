import json
import os
import re

PROMPT_FILE = os.path.join(os.path.dirname(__file__), "prompt.txt")

def generate_plan(screen_text, user_command, think_func):
    """
    Combines inputs into a prompt, sends it to the LLM, and parses the JSON response.
    """
    if not os.path.exists(PROMPT_FILE):
        return [{"action": "wait", "seconds": 1, "error": "System prompt.txt is missing."}]

    try:
        with open(PROMPT_FILE, "r") as f:
            template = f.read()

        # Inject context into the prompt
        full_prompt = template.format(screen=screen_text, command=user_command)

        # Get response from AI
        raw_response = think_func(full_prompt)

        # Clean up and parse JSON
        actions = parse_json_actions(raw_response)
        return actions
    except Exception as e:
        return [{"action": "wait", "seconds": 1, "error": f"Planner Error: {str(e)}"}]

def parse_json_actions(text):
    """
    Extracts and parses JSON from the raw LLM string.
    """
    try:
        # Look for JSON array or object using regex
        match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            if isinstance(data, list):
                return data
            else:
                return [data]
        else:
            # Fallback if no JSON-like structure is found
            print(f"No JSON found in response: {text}")
            return []
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from: {text}")
        return []

if __name__ == "__main__":
    print("Planner module ready.")
