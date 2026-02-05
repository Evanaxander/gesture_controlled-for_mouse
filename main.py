import cv2
import mediapipe as mp
import pyautogui
import time
import math

# 1. Initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Screen and Control Settings
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False 

# State Variables
click_times = []
last_screenshot_time = 0
screenshot_cooldown = 2
prev_screen_x, prev_screen_y = 0, 0
smoothness = 5 

# Camera Setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("\nHand mouse control active. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
          
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            
           
            fingers = [1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0 
                       for tip in [8, 12, 16, 20]]

          
            distance = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y) 
            freeze_cursor = False
            
            if distance < 0.05:
                freeze_cursor = True
                current_time = time.time()
                click_times.append(current_time)

                # Double Click Detection
                if len(click_times) >= 2 and (click_times[-1] - click_times[-2] < 0.4):
                    pyautogui.doubleClick()
                    cv2.putText(frame, "Double Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    click_times = [] 
                else:
                    # Single Click Cooldown
                    if len(click_times) == 1 or (click_times[-1] - click_times[-2] > 0.5):
                        pyautogui.click()
                        cv2.putText(frame, "Single Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            else:
                # Cleanup list
                if len(click_times) > 5: click_times = click_times[-2:]

         
            if sum(fingers) == 4:
                if index_tip.y < 0.4:
                    pyautogui.scroll(80)
                    cv2.putText(frame, "Scrolling Up", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif index_tip.y > 0.6:
                    pyautogui.scroll(-80)
                    cv2.putText(frame, "Scrolling Down", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                freeze_cursor = True 

         # SCREENSHOT LOGIC
            if sum(fingers) == 0:
                current_time = time.time()
                if current_time - last_screenshot_time > screenshot_cooldown:
                    pyautogui.screenshot(f"screenshot_{int(current_time)}.png")
                    last_screenshot_time = current_time
                    cv2.putText(frame, "Screenshot Saved", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                freeze_cursor = True

            # (Interpolated/Smoothed) 
            if not freeze_cursor:
               
                target_x = int(index_tip.x * screen_width)
                target_y = int(index_tip.y * screen_height)
                
                curr_screen_x = prev_screen_x + (target_x - prev_screen_x) // smoothness
                curr_screen_y = prev_screen_y + (target_y - prev_screen_y) // smoothness
                
                pyautogui.moveTo(curr_screen_x, curr_screen_y, _pause=False)
                prev_screen_x, prev_screen_y = curr_screen_x, curr_screen_y

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Optimized Hand Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()