# Reem AI (Mobile & Desktop)

Reem AI is an offline, free, and open-source AI operator that can see your screen and perform actions like a human. This version supports **Mobile Applications** (via ADB) and **Desktop** (via PyAutoGUI).

## 🎯 Features
- **Mobile Vision**: Captures mobile screens via ADB for OCR.
- **Desktop Vision**: Uses PyAutoGUI for desktop OCR.
- **Mobile Gestures**: Supports `tap`, `swipe`, and `keyevent` (home, back, etc.) via ADB.
- **Cross-Platform GUI**: Built with Kivy for mobile and desktop compatibility.
- **Local Brain**: Runs locally using GGUF models via `llama-cpp-python`.

## 🛠 Architecture
```
ReemAI/
 ├── app/
      ├── main.py           # Kivy UI Entry Point
      ├── orchestrator.py   # Core Logic (handles mobile/desktop modes)
      ├── llm.py            # Local Model Interface
      ├── vision.py         # OCR for both Mobile & Desktop
      ├── voice.py          # Speech Recognition
      ├── planner.py        # AI Action Planning
      ├── executor.py       # Action Execution
      ├── prompt.txt        # System Prompt Template
      ├── buildozer.spec    # APK Build Configuration
      ├── DEPLOYMENT.md     # Guide for GitHub/Vercel
      └── model/
           └── model.gguf   # Place your local model here
```

## 📦 Requirements
- Python 3.10+
- **Tesseract OCR engine**: Must be installed on the machine running the app.
- **ADB (Android Debug Bridge)**: Required for mobile control mode.

### Python Libraries:
```bash
pip install kivy plyer pyautogui pytesseract pillow llama-cpp-python speechrecognition pyaudio opencv-python
```

## 🚀 Setup & Running

1. **Desktop Mode**:
   - Run: `REEM_MODE=desktop python3 app/main.py`
   - The AI will see your computer screen and control your mouse/keyboard.

2. **Mobile Mode (Remote Control)**:
   - Connect your Android device via USB.
   - Enable **USB Debugging** in Developer Options.
   - Verify connection: `adb devices`
   - Run: `REEM_MODE=mobile python3 app/main.py`
   - The AI will see the phone screen and send touch events via ADB.

## 🧠 Example Mobile Interaction

**User Command**: "Open Instagram and scroll down"

**AI Action**:
```json
[
  {"action": "tap", "x": 200, "y": 500},
  {"action": "wait", "seconds": 2},
  {"action": "swipe", "x1": 500, "y1": 1500, "x2": 500, "y2": 500, "duration": 500}
]
```

## ⚠ SAFETY WARNING
**This program controls your device.**
- **Desktop**: Move mouse to **top-left** to abort.
- **Mobile**: Disconnect the USB cable to stop.
- The AI may misinterpret screen content. Use only on trusted systems.

## 🆓 License
Apache-2.0. Free, Offline, Open-Source.
