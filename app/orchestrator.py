import vision
import llm
import planner
import executor
import os
import subprocess
import re

# Mode can be 'desktop' or 'mobile'
MODE = os.getenv("REEM_MODE", "mobile")

def get_resolution():
    """
    Attempts to get screen resolution for the current mode.
    """
    if MODE == "mobile":
        try:
            result = subprocess.run(['adb', 'shell', 'wm', 'size'], capture_output=True, text=True)
            match = re.search(r'Override size: (\d+)x(\d+)', result.stdout)
            if not match:
                match = re.search(r'Physical size: (\d+)x(\d+)', result.stdout)
            if match:
                return f"{match.group(1)}x{match.group(2)}"
        except:
            pass
        return "Unknown Mobile Res"
    else:
        try:
            import pyautogui
            w, h = pyautogui.size()
            return f"{w}x{h}"
        except:
            return "Unknown Desktop Res"

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

    res = get_resolution()
    print(f"\n--- Reem AI Processing Command ({MODE} - {res}): '{command}' ---")

    # 1. Capture screen context via OCR
    if MODE == "mobile":
        print("[Vision] Reading mobile screen...")
        screen_content = vision.read_mobile_screen()
    else:
        print("[Vision] Reading desktop screen...")
        screen_content = vision.read_screen()

    # Prepend resolution to screen content for AI context
    full_context = f"Screen Resolution: {res}\n\nElements detected:\n{screen_content}"

    # 2. Generate AI plan
    print("[LLM] Thinking...")
    plan = planner.generate_plan(full_context, command, llm.think)

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
