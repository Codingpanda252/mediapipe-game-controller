import cv2
from hand_tracking import HandTracker


def main():
    # Initialize HandTracker
    hand_tracker = HandTracker()

    # Start video capture (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Detect hands and landmarks
        hands, img = hand_tracker.detect_hands(frame)

        # Count raised fingers and send corresponding keyboard command
        fingers_up = hand_tracker.count_fingers(hands)
        hand_tracker.send_keyboard_command(fingers_up)

        # Display the frame with hand landmarks
        cv2.imshow('Hand Tracking', img)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
