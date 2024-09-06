import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller as KeyboardController


class HandTracker:
    def __init__(self):
        # Initialize the HandDetector with specific parameters
        self.detector = HandDetector(maxHands=1, detectionCon=0.8)
        self.keyboard = KeyboardController()

    def detect_hands(self, frame):
        # Detect hands and landmarks in the frame
        hands, img = self.detector.findHands(frame)
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
            if thumb_tip_y < thumb_ip_y:
                fingers_up += 1

            # Fingers: Index, Middle, Ring, Pinky
            for i in [8, 12, 16, 20]:
                tip_y = landmarks[i][1]
                mcp_y = landmarks[i - 2][1]
                if tip_y < mcp_y:
                    fingers_up += 1

            print(f"Counted fingers up: {fingers_up}")
            return fingers_up
        return 0

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
