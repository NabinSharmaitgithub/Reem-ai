import sys
import os
from unittest.mock import MagicMock

# Mock pyautogui before it's imported by anything
sys.modules['pyautogui'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['llama_cpp'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()

# Ensure the python directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ReemAI', 'python')))

import main
import vision
import executor
import llm

def mock_vision_read():
    return "Desktop icons: Chrome, Notepad, Terminal."

def mock_llm_think(prompt):
    print(f"[Mock LLM] Received prompt of length {len(prompt)}")
    # Return a valid JSON string
    return '[{"action": "type", "text": "Testing Reem AI integration"}]'

def mock_executor_run(steps):
    print(f"[Mock Executor] Executing {len(steps)} steps.")
    for step in steps:
        print(f" - {step}")
        assert "action" in step

def run_mock_test():
    print("=== Running Mock Integration Test ===")

    # Monkeypatch modules to avoid real UI/LLM calls in test environment
    vision.read_screen = mock_vision_read
    llm.think = mock_llm_think
    executor.run_plan = mock_executor_run

    test_command = "Type a test message"

    try:
        main.process(test_command)
        print("Integration test successful!")
    except Exception as e:
        print(f"Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_mock_test()
