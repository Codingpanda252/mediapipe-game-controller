import cv2
from hand_tracking import HandTracker
from head_tracking import HeadTracker


def main():
    # Initialize trackers
    hand_tracker = HandTracker()
    head_tracker = HeadTracker()

    # Start video capture (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Process hand tracking
        hands, frame_with_hands = hand_tracker.detect_hands(frame)
        hand_tracker.send_commands(hands)

        # Process head tracking
        frame_with_head_tracking = head_tracker.process_frame(frame_with_hands)

        # Display the frame with both hand and head tracking
        cv2.imshow('Hand and Head Tracking', frame_with_head_tracking)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
