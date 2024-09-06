import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller as KeyboardController
from time import time, sleep


class HandTracker:
    def __init__(self, key_hold_duration=0.5):
        self.hand_detector = HandDetector()
        self.keyboard = KeyboardController()
        self.key_hold_duration = key_hold_duration
        self.key_press_times = {}  # Track when keys were last pressed

    def detect_hands(self, frame):
        hands, img = self.hand_detector.findHands(frame, draw=True)
        return hands, img

    def send_commands(self, hands):
        if hands:
            hand = hands[0]  # Use the first detected hand
            fingers_up = self.count_fingers(hand)
            command = self.get_wasd_command(fingers_up)
            self.manage_keyboard(command)
        else:
            # Release all keys if no hands are detected
            self.release_all_keys()

    def count_fingers(self, hand_landmarks):
        fingers_up = 0
        # Implement the logic to count fingers based on landmarks
        return fingers_up

    def get_wasd_command(self, fingers_up):
        commands = {
            1: "w",  # Forward
            2: "a",  # Left
            3: "s",  # Backward
            4: "d"  # Right
        }
        return commands.get(fingers_up, None)

    def manage_keyboard(self, command):
        current_time = time()
        if command:
            # Press the key if it's not already being pressed or if the hold duration has passed
            if command not in self.key_press_times or (
                    current_time - self.key_press_times[command] > self.key_hold_duration):
                self.keyboard.press(command)
                self.key_press_times[command] = current_time
                print(f"Holding key: {command}")
        else:
            # Release all keys if no valid command
            self.release_all_keys()

    def release_all_keys(self):
        # Release all currently pressed keys
        for key in self.key_press_times.keys():
            self.keyboard.release(key)
        self.key_press_times.clear()
        print("Released all keys")

