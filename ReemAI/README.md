# Reem AI

Reem AI is an offline, free, and open-source AI operator that can see your screen and perform actions like a human (mouse, keyboard, scroll). Inspired by AI phone operators like blurr, Reem AI runs 100% locally on your machine.

## 🎯 Features
- **Screen Vision**: Uses OCR to read what's on your screen.
- **Voice Control**: Accepts voice commands (with offline support options).
- **Local Brain**: Powered by local GGUF models via `llama-cpp-python`.
- **Action Execution**: Controls mouse and keyboard using `pyautogui`.
- **Privacy First**: No cloud APIs, no data leaves your computer.

## 🛠 Architecture
```
ReemAI/
 ├── README.md
 └── python/
      ├── gui.py        # Tkinter User Interface
      ├── main.py       # Core Orchestration Logic
      ├── llm.py        # Local Model Interface
      ├── vision.py     # Screen Capture & OCR
      ├── voice.py      # Speech Recognition
      ├── planner.py    # AI Action Planning
      ├── executor.py   # UI Action Execution
      ├── prompt.txt    # System Prompt Template
      └── model/
           └── model.gguf # Place your local model here
```

## 📦 Requirements
- Python 3.10+
- **Tesseract OCR engine**: Must be installed on your system.
- **PortAudio**: Required for the `pyaudio` library.

### Python Libraries:
```bash
pip install pyautogui pytesseract pillow llama-cpp-python speechrecognition pyaudio opencv-python
```

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ReemAI
   ```

2. **Install System Dependencies**:
   - **Tesseract OCR**:
     - Ubuntu: `sudo apt install tesseract-ocr`
     - Mac: `brew install tesseract`
     - Windows: Download the installer from UB Mannheim's Tesseract page.
   - **PortAudio** (for Voice):
     - Ubuntu: `sudo apt install portaudio19-dev`
     - Mac: `brew install portaudio`

3. **Download a Local LLM**:
   - Download a GGUF model (Recommended: Phi-2, Gemma 2B, or Mistral 7B Q4_K_M).
   - Place the file in `ReemAI/python/model/` and rename it to `model.gguf`.

4. **Run the Application**:
   ```bash
   python3 python/gui.py
   ```

## 🧠 Example AI Interaction

**User Command**: "Search for cats on Google"

**System Prompt (Generated)**:
```text
You are Reem AI, an offline AI operator...
Screen Content: [Text from your browser window...]
User Command: Search for cats on Google
...
```

**Example AI JSON Response**:
```json
[
  {"action": "click", "x": 400, "y": 300},
  {"action": "type", "text": "cats"},
  {"action": "press", "key": "enter"},
  {"action": "wait", "seconds": 2}
]
```

## ⚠ SAFETY WARNING
**This program controls your mouse and keyboard.** It can perform any action a human can.
- Use only on systems you trust.
- Be aware that the AI might misinterpret screen content or commands.
- **Fail-safe**: If the AI goes out of control, move your mouse cursor quickly to the **top-left corner** of the screen to abort all actions.

## 🆓 License
Reem AI is released under the Apache-2.0 license. It is 100% free, offline, and open-source.
