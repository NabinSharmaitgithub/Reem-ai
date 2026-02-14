import os
import subprocess
import io

def get_ocr_with_coords(img):
    """
    Performs OCR on an image and returns a string with text and their bounding boxes.
    """
    try:
        import pytesseract
        from PIL import Image
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        n_boxes = len(data['text'])
        lines = []
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if text:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                lines.append(f'"{text}" [{x}, {y}, {w}, {h}]')

        return "\n".join(lines)
    except ImportError:
        return "Error: pytesseract not installed."
    except Exception as e:
        return f"OCR Error: {str(e)}"

def read_screen():
    """
    Captures the primary desktop screen.
    """
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        return get_ocr_with_coords(screenshot)
    except ImportError:
        return "Error: pyautogui not installed."
    except Exception as e:
        return f"Error reading desktop screen: {str(e)}"

def read_mobile_screen():
    """
    Captures the mobile screen via ADB.
    """
    try:
        from PIL import Image
        # Capture screen via ADB
        process = subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
        screenshot_data, _ = process.communicate()

        if not screenshot_data:
            return "Error: Failed to capture mobile screen via ADB. Is the device connected?"

        # Load image from bytes
        img = Image.open(io.BytesIO(screenshot_data))
        return get_ocr_with_coords(img)
    except ImportError:
        return "Error: PIL not installed."
    except Exception as e:
        return f"Error reading mobile screen: {str(e)}"

def read_camera():
    """
    Captures a frame from the default webcam.
    """
    try:
        import cv2
        from PIL import Image
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
        return get_ocr_with_coords(pil_img)
    except ImportError:
        return "Error: opencv-python not installed."
    except Exception as e:
        return f"Error reading camera: {str(e)}"

if __name__ == "__main__":
    print("Vision module loaded.")
