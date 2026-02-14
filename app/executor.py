import time
import subprocess

def run_plan(steps):
    """
    Executes a sequence of UI actions for Desktop.
    """
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
    except ImportError:
        print("Desktop execution (pyautogui) not available.")
        return

    if not steps:
        print("No actions to execute.")
        return

    for step in steps:
        action = step.get("action")
        print(f"Executing Desktop: {step}")

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
                if action in ["tap", "swipe"]:
                    run_mobile_plan([step])
                else:
                    print(f"Unknown desktop action: {action}")

        except Exception as e:
            print(f"Failed to execute {action}: {e}")

def run_mobile_plan(steps):
    """
    Executes a sequence of UI actions for Mobile via ADB.
    """
    if not steps:
        return

    for step in steps:
        action = step.get("action")
        print(f"Executing Mobile: {step}")

        try:
            if action == "tap" or action == "click":
                x, y = step.get("x"), step.get("y")
                if x is not None and y is not None:
                    subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])

            elif action == "type":
                text = step.get("text", "")
                escaped_text = text.replace(" ", "%s")
                subprocess.run(['adb', 'shell', 'input', 'text', escaped_text])

            elif action == "swipe":
                x1, y1 = step.get("x1"), step.get("y1")
                x2, y2 = step.get("x2"), step.get("y2")
                duration = step.get("duration", 300)
                if all(v is not None for v in [x1, y1, x2, y2]):
                    subprocess.run(['adb', 'shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)])

            elif action == "press":
                key = step.get("key")
                if key:
                    key_map = {"enter": "66", "home": "3", "back": "4"}
                    keycode = key_map.get(str(key).lower(), key)
                    subprocess.run(['adb', 'shell', 'input', 'keyevent', str(keycode)])

            elif action == "wait":
                seconds = step.get("seconds", 1)
                time.sleep(seconds)

            else:
                print(f"Unknown mobile action: {action}")

        except Exception as e:
            print(f"Failed to execute mobile {action}: {e}")

if __name__ == "__main__":
    print("Executor module ready.")
