import pyautogui
import pytesseract
from PIL import Image
import cv2
import os
import subprocess
import io

# If tesseract is not in your PATH, uncomment and set this:
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def read_screen():
    """
    Captures the primary desktop screen and returns the text found via OCR.
    """
    try:
        screenshot = pyautogui.screenshot()
        text = pytesseract.image_to_string(screenshot)
        return text.strip()
    except Exception as e:
        return f"Error reading desktop screen: {str(e)}"

def read_mobile_screen():
    """
    Captures the mobile screen via ADB and returns the text found via OCR.
    """
    try:
        # Capture screen via ADB
        process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
        screenshot_data, _ = process.communicate()

        if not screenshot_data:
            return "Error: Failed to capture mobile screen via ADB. Is the device connected?"

        # Load image from bytes
        img = Image.open(io.BytesIO(screenshot_data))
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"Error reading mobile screen: {str(e)}"

def read_camera():
    """
    Captures a frame from the default webcam and returns the text found via OCR.
    """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Error: Camera not available."

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "Error: Failed to capture image from camera."

        # Convert BGR (OpenCV) to RGB (PIL)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        text = pytesseract.image_to_string(pil_img)
        return text.strip()
    except Exception as e:
        return f"Error reading camera: {str(e)}"

if __name__ == "__main__":
    print("Vision module loaded with mobile support.")
