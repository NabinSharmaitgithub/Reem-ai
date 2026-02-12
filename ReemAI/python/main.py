import vision
import llm
import planner
import executor

def process(command):
    """
    The core loop of Reem AI:
    1. Read the screen context.
    2. Think using the local LLM.
    3. Execute the resulting actions.
    """
    if not command:
        print("No command provided.")
        return "No command provided."

    print(f"\n--- Reem AI Processing Command: '{command}' ---")

    # 1. Capture screen context via OCR
    print("[Vision] Reading screen...")
    screen_content = vision.read_screen()

    # 2. Generate AI plan
    print("[LLM] Thinking...")
    plan = planner.generate_plan(screen_content, command, llm.think)

    # 3. Execute the plan
    print(f"[Executor] Running {len(plan)} actions...")
    executor.run_plan(plan)

    print("--- Done ---\n")
    return f"Processed: {command}"

if __name__ == "__main__":
    print("Reem AI Core Logic loaded.")
