# main.py
import cv2
from hand_tracking import HandTracker
from head_tracking import HeadTracker
from game_controller import GameController


def main():
    # Initialize objects
    hand_tracker = HandTracker()
    head_tracker = HeadTracker()
    game_controller = GameController()

    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Hand tracking for WASD commands
        hand_result = hand_tracker.detect_hands(frame)
        if hand_result.multi_hand_landmarks:
            for hand_landmarks in hand_result.multi_hand_landmarks:
                fingers_up = hand_tracker.count_fingers(hand_landmarks)
                command = hand_tracker.get_wasd_command(fingers_up)
                game_controller.send_keyboard_command(command)

        # Head tracking for camera rotation
        face_result = head_tracker.detect_head(frame)
        if face_result.multi_face_landmarks:
            # Draw face mesh
            head_tracker.draw_face_mesh(frame, face_result.multi_face_landmarks)

            for face_landmarks in face_result.multi_face_landmarks:
                rotation_x, rotation_y = head_tracker.get_head_rotation(face_landmarks)
                game_controller.send_mouse_movement(rotation_x, rotation_y)

        # Display the video frame
        cv2.imshow("Game Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
