import vision
import llm
import planner
import executor
import os

# Mode can be 'desktop' or 'mobile'
MODE = os.getenv("REEM_MODE", "mobile")

def process(command):
    """
    The core loop of Reem AI:
    1. Read the screen context (Mobile or Desktop).
    2. Think using the local LLM.
    3. Execute the resulting actions.
    """
    if not command:
        print("No command provided.")
        return "No command provided."

    print(f"\n--- Reem AI Processing Command ({MODE}): '{command}' ---")

    # 1. Capture screen context via OCR
    if MODE == "mobile":
        print("[Vision] Reading mobile screen...")
        screen_content = vision.read_mobile_screen()
    else:
        print("[Vision] Reading desktop screen...")
        screen_content = vision.read_screen()

    # 2. Generate AI plan
    print("[LLM] Thinking...")
    plan = planner.generate_plan(screen_content, command, llm.think)

    # 3. Execute the plan
    print(f"[Executor] Running {len(plan)} actions...")
    if MODE == "mobile":
        executor.run_mobile_plan(plan)
    else:
        executor.run_plan(plan)

    print("--- Done ---\n")
    return f"Processed: {command}"

if __name__ == "__main__":
    print(f"Reem AI Core Logic loaded in {MODE} mode.")
