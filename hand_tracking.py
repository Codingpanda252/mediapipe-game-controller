# hand_tracking.py
import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return result

    def count_fingers(self, hand_landmarks):
        # Custom logic to count raised fingers and map to WASD commands
        fingers_up = 0
        # Example: Implement logic for thumb, index, middle, ring, pinky
        return fingers_up

    def get_wasd_command(self, fingers_up):
        # Map the number of fingers to WASD keys
        commands = {
            1: "W",  # Forward
            2: "A",  # Left
            3: "S",  # Backward
            4: "D"   # Right
        }
        return commands.get(fingers_up, None)