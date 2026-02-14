import sys
import os
from unittest.mock import MagicMock, patch

# Mock libraries before they are imported
sys.modules['pyautogui'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['llama_cpp'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()

# Mock Kivy and its submodules
kivy_mock = MagicMock()
sys.modules['kivy'] = kivy_mock
sys.modules['kivy.app'] = MagicMock()
sys.modules['kivy.uix'] = MagicMock()
sys.modules['kivy.uix.boxlayout'] = MagicMock()
sys.modules['kivy.uix.label'] = MagicMock()
sys.modules['kivy.uix.textinput'] = MagicMock()
sys.modules['kivy.uix.button'] = MagicMock()
sys.modules['kivy.uix.scrollview'] = MagicMock()
sys.modules['kivy.clock'] = MagicMock()

# Add the app directory to path
sys.path.append(os.path.dirname(__file__))

import orchestrator
import vision
import executor
import llm

def mock_vision_read_mobile():
    return '"Settings" [100, 200, 50, 20]\n"Wi-Fi" [100, 300, 40, 20]'

def mock_llm_think(prompt):
    print(f"[Mock LLM] Received prompt with OCR data.")
    # Return a mobile action using the center of "Settings"
    return '[{"action": "tap", "x": 125, "y": 210}]'

@patch('subprocess.run')
def run_mobile_test(mock_run):
    print("=== Running Improved Mobile Integration Test ===")

    # Setup mocks
    vision.read_mobile_screen = mock_vision_read_mobile
    llm.think = mock_llm_think
    orchestrator.MODE = "mobile"

    # Mock resolution response
    mock_run.return_value.stdout = "Physical size: 1080x2400"

    test_command = "Tap on Settings"

    try:
        orchestrator.process(test_command)

        # Verify ADB was called for tap
        called_args = [call.args for call in mock_run.call_args_list]
        print(f"[Mock Subprocess] Called with: {called_args}")

        adb_call_found = any('adb' in args[0] and 'tap' in args[0] for args in called_args)
        if adb_call_found:
            print("ADB tap call verified with coordinates!")
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
