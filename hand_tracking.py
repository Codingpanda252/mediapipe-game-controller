import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller as KeyboardController
import numpy as np


class HandTracker:
    def __init__(self, smoothing_factor=0.8):
        # Initialize the HandDetector with specific parameters
        self.detector = HandDetector(maxHands=1, detectionCon=0.8)
        self.keyboard = KeyboardController()
        self.smoothing_factor = smoothing_factor
        self.previous_fingers_up = 0

    def detect_hands(self, frame):
        # Detect hands and landmarks in the frame
        hands, img = self.detector.findHands(frame)
        if hands:
            for hand in hands:
                landmarks = hand['lmList']
                # Draw landmarks for debugging
                for lm in landmarks:
                    x, y = lm[0], lm[1]
                    cv2.circle(img, (x, y), 5, (0, 255, 0), cv2.FILLED)
                print("Landmarks:", landmarks)
        return hands, img

    def count_fingers(self, hands):
        if hands:
            hand = hands[0]
            landmarks = hand['lmList']

            # Initialize the number of fingers up
            fingers_up = 0

            # Thumb (special case)
            thumb_tip_y = landmarks[4][1]
            thumb_ip_y = landmarks[3][1]
            thumb_mcp_y = landmarks[2][1]
            if thumb_tip_y < thumb_ip_y and thumb_ip_y < thumb_mcp_y:
                fingers_up += 1

            # Fingers: Index, Middle, Ring, Pinky
            for i, base in zip([8, 12, 16, 20], [6, 10, 14, 18]):
                tip_y = landmarks[i][1]
                base_y = landmarks[base][1]
                if tip_y < base_y:
                    fingers_up += 1

            # Ensure not to count more than 5 fingers
            fingers_up = min(fingers_up, 5)

            return fingers_up
        return 0

    def smooth_fingers_count(self, current_fingers_up):
        # Smooth the transition between finger counts
        smoothed_fingers_up = int(
            self.smoothing_factor * current_fingers_up + (1 - self.smoothing_factor) * self.previous_fingers_up)
        self.previous_fingers_up = smoothed_fingers_up
        return smoothed_fingers_up

    def get_wasd_command(self, fingers_up):
        # Map the number of fingers to WASD keys
        commands = {
            1: "w",  # Forward
            2: "a",  # Left
            3: "s",  # Backward
            4: "d"  # Right
        }
        return commands.get(fingers_up, None)

    def send_keyboard_command(self, fingers_up):
        command = self.get_wasd_command(fingers_up)
        if command:
            # Send the keyboard command
            self.keyboard.press(command)
            self.keyboard.release(command)
            print(f"Sent keyboard command: {command}")
        else:
            print("No command mapped for this number of fingers.")

