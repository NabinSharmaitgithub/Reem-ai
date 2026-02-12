import pyautogui
import time

# Enable fail-safe: move mouse to top-left corner to abort
pyautogui.FAILSAFE = True

def run_plan(steps):
    """
    Executes a sequence of UI actions based on a list of steps.
    Each step is a dictionary containing 'action' and parameters.
    """
    if not steps:
        print("No actions to execute.")
        return

    for step in steps:
        action = step.get("action")
        print(f"Executing: {step}")

        try:
            if action == "click":
                x, y = step.get("x"), step.get("y")
                if x is not None and y is not None:
                    pyautogui.click(x, y)

            elif action == "type":
                text = step.get("text", "")
                pyautogui.typewrite(text, interval=0.1)

            elif action == "scroll":
                amount = step.get("amount", 0)
                pyautogui.scroll(amount)

            elif action == "wait":
                seconds = step.get("seconds", 1)
                time.sleep(seconds)

            elif action == "press":
                key = step.get("key")
                if key:
                    pyautogui.press(key)

            else:
                print(f"Unknown action: {action}")

        except Exception as e:
            print(f"Failed to execute {action}: {e}")

if __name__ == "__main__":
    print("Executor module ready.")
