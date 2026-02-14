# Reem AI (Mobile & Desktop)

Reem AI is an offline, free, and open-source AI operator that can see your screen and perform actions like a human. This version has been converted to support **Mobile Applications** via ADB and **Desktop** via PyAutoGUI.

## 🎯 Features
- **Mobile Vision**: Captures mobile screens via ADB for OCR.
- **Desktop Vision**: Uses PyAutoGUI for desktop OCR.
- **Mobile Gestures**: Supports `tap`, `swipe`, and `keyevent` (home, back, etc.) via ADB.
- **Cross-Platform GUI**: Built with Kivy for mobile and desktop compatibility.
- **Local Brain**: Runs locally using GGUF models via `llama-cpp-python`.

## 🛠 Architecture
```
ReemAI/
 ├── README.md
 └── python/
      ├── gui.py        # Kivy User Interface (Mobile Ready)
      ├── main.py       # Core Orchestration (handles mobile/desktop modes)
      ├── llm.py        # Local Model Interface
      ├── vision.py     # OCR for both Mobile & Desktop
      ├── voice.py      # Speech Recognition
      ├── planner.py    # AI Action Planning
      ├── executor.py   # Action Execution (ADB for Mobile, PyAutoGUI for Desktop)
      ├── prompt.txt    # System Prompt Template with mobile actions
      └── model/
           └── model.gguf # Place your local model here
```

## 📦 Requirements
- Python 3.10+
- **Tesseract OCR engine**: Must be installed.
- **ADB (Android Debug Bridge)**: Required for mobile control.

### Python Libraries:
```bash
pip install kivy plyer pyautogui pytesseract pillow llama-cpp-python speechrecognition pyaudio opencv-python
```

## 🚀 Mobile Setup

1. **Connect your Android Device**:
   - Enable **Developer Options** and **USB Debugging**.
   - Connect via USB or ADB over WiFi.
   - Verify connection: `adb devices`

2. **Run the Application**:
   ```bash
   # Defaults to mobile mode
   python3 python/gui.py
   ```

3. **Desktop Mode**:
   - To use desktop mode, set the environment variable:
   ```bash
   REEM_MODE=desktop python3 python/gui.py
   ```

## 🧠 Example Mobile Interaction

**User Command**: "Open Instagram and scroll down"

**Example AI JSON Response**:
```json
[
  {"action": "tap", "x": 200, "y": 500},
  {"action": "wait", "seconds": 2},
  {"action": "swipe", "x1": 500, "y1": 1500, "x2": 500, "y2": 500, "duration": 500}
]
```

## ⚠ SAFETY WARNING
**This program controls your device.**
- Move your mouse to the **top-left** (Desktop) or disconnect the device (Mobile) to stop.
- The AI may misinterpret screen content. Use with caution.

## 🆓 License
Apache-2.0. Free, Offline, Open-Source.
