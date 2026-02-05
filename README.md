
<img width="1785" height="945" alt="Screenshot 2026-02-05 155305" src="https://github.com/user-attachments/assets/fc014018-ef8c-4c17-8011-7bc8f5ed6025" />
# Gesture-Controlled Mouse with MediaPipe

A high-performance Python application that allows you to control your computer's mouse using hand gestures via a webcam (or Iriun USB/Wi-Fi camera).

This project uses **MediaPipe** for hand landmark detection and **PyAutoGUI** for system-level mouse and keyboard control.

## Features

* **Smooth Cursor Movement:** Uses a weighted smoothing algorithm to eliminate hand tremors.
* **Intelligent Clicking:** * **Single Click:** Pinch your thumb and index finger.
* **Double Click:** Double-pinch within 0.4 seconds.


* **Scroll Mode:** Show an open palm (4 fingers up) and move your hand to the top or bottom of the screen to scroll.
* **Hand Gestures for Utilities:** * **Screenshot:** Make a fist (0 fingers up) to capture and save your screen automatically.
* **Stability:** Optimized for 640x480 resolution to ensure low latency and prevent application crashes.



## Hand Landmark Reference

The system tracks 21 specific points on your hand to calculate gestures:



## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/gesture-controlled-mouse.git
cd gesture-controlled-mouse

```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv gesture_env
# Activate on Windows:
.\gesture_env\Scripts\activate
# Activate on Mac/Linux:
source gesture_env/bin/activate

```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui

```

---

## Usage

1. Connect your webcam or start the **Iriun Webcam** app on your phone and PC.
2. Run the script:
```bash
python main.py

```


3. **Controls:**
* **Move:** Point your index finger.
* **Click:** Pinch thumb and index finger together.
* **Scroll:** Open your palm; move hand UP to scroll up, DOWN to scroll down.
* **Screenshot:** Close your hand into a fist.
* **Quit:** Press **'q'** while the camera window is active.



---

## Configuration

You can adjust the following variables in `main.py` to suit your needs:

* `smoothness`: Increase this value (e.g., 7-10) for even smoother movement, or decrease it (e.g., 2-3) for faster response.
* `min_detection_confidence`: Set to a higher value (e.g., 0.8) if you are in a busy background to reduce false detections.
* `screenshot_cooldown`: Changes how many seconds must pass between screenshots.

## Troubleshooting

* **AttributeError: module 'mediapipe' has no attribute 'solutions'**: Ensure your script is not named `mediapipe.py`. If the error persists, run `pip install mediapipe==0.10.9`.
* **Mouse hits corner and script stops**: The `pyautogui.FAILSAFE` is set to `False` in this script, but ensure you move your hand back into view to regain control.
* **Iriun Camera not found**: Change `cv2.VideoCapture(0)` to `1` or `2` depending on how many cameras are connected to your PC.

<img width="1785" height="945" alt="Screenshot 2026-02-05 155305" src="https://github.com/user-attachments/assets/fc014018-ef8c-4c17-8011-7bc8f5ed6025" />



