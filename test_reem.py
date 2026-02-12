import sys
import os
from unittest.mock import MagicMock, patch

# Mock libraries before they are imported
sys.modules['pyautogui'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['llama_cpp'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()
sys.modules['kivy'] = MagicMock()
sys.modules['kivy.app'] = MagicMock()
sys.modules['kivy.uix'] = MagicMock()
sys.modules['kivy.clock'] = MagicMock()

# Ensure the python directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ReemAI', 'python')))

import main
import vision
import executor
import llm

def mock_vision_read_mobile():
    return "Mobile Screen: Settings, Wi-Fi, Battery."

def mock_llm_think(prompt):
    print(f"[Mock LLM] Received prompt of length {len(prompt)}")
    # Return a mobile action
    return '[{"action": "tap", "x": 100, "y": 200}]'

@patch('subprocess.run')
def run_mobile_test(mock_run):
    print("=== Running Mobile Integration Test ===")

    # Setup mocks
    vision.read_mobile_screen = mock_vision_read_mobile
    llm.think = mock_llm_think
    main.MODE = "mobile"

    test_command = "Tap on Settings"

    try:
        main.process(test_command)

        # Verify ADB was called for tap
        # The call should look like: subprocess.run(['adb', 'shell', 'input', 'tap', '100', '200'])
        called_args = [call.args for call in mock_run.call_args_list]
        print(f"[Mock Subprocess] Called with: {called_args}")

        adb_call_found = any('adb' in args[0] and 'tap' in args[0] for args in called_args)
        if adb_call_found:
            print("ADB tap call verified!")
        else:
            print("ADB tap call NOT found!")
            sys.exit(1)

        print("Mobile integration test successful!")
    except Exception as e:
        print(f"Mobile integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_mobile_test()
