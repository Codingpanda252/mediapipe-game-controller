import cv2
from cvzone.FaceDetectionModule import FaceDetector
from pynput.mouse import Controller as MouseController
import numpy as np


class HeadTracker:
    def __init__(self, smoothing_factor=0.8):
        self.face_detector = FaceDetector()
        self.mouse = MouseController()
        self.smoothing_factor = smoothing_factor
        self.prev_x, self.prev_y = self.mouse.position

    def detect_head(self, frame):
        faces, img = self.face_detector.findFaces(frame, draw=True)
        return faces, img

    def get_head_rotation(self, faces, frame):
        if faces.size == 0:
            return 0, 0

        # Assume faces is an ndarray with bounding boxes in [x, y, w, h] format
        # We use the first detected face
        face = faces[0]

        # Extract bounding box coordinates
        x, y, w, h = face

        center_x = x + w // 2
        center_y = y + h // 2

        screen_width, screen_height = self.mouse.screen_size
        norm_x = (center_x / frame.shape[1]) * screen_width
        norm_y = (center_y / frame.shape[0]) * screen_height

        rotation_x = norm_x - self.prev_x
        rotation_y = norm_y - self.prev_y

        print(f"Face bbox: {face}")
        print(f"Face center: ({center_x}, {center_y})")
        print(f"Normalized position: ({norm_x}, {norm_y})")
        print(f"Rotation deltas: ({rotation_x}, {rotation_y})")

        return rotation_x, rotation_y

    def move_mouse_based_on_head_rotation(self, rotation_x, rotation_y):
        screen_width, screen_height = self.mouse.screen_size
        norm_x = np.clip(rotation_x, -screen_width / 2, screen_width / 2)
        norm_y = np.clip(rotation_y, -screen_height / 2, screen_height / 2)

        smoothed_x = self.prev_x + self.smoothing_factor * (norm_x - self.prev_x)
        smoothed_y = self.prev_y + self.smoothing_factor * (norm_y - self.prev_y)

        self.mouse.position = (smoothed_x, smoothed_y)
        self.prev_x, self.prev_y = smoothed_x, smoothed_y

        print(f"Smoothed mouse position: ({smoothed_x}, {smoothed_y})")

    def process_frame(self, frame):
        faces, img = self.detect_head(frame)

        if faces.size > 0:  # Check if faces array is non-empty
            rotation_x, rotation_y = self.get_head_rotation(faces, frame)
            self.move_mouse_based_on_head_rotation(rotation_x, rotation_y)

        return img
