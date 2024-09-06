# game_controller.py
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController


class GameController:
    def __init__(self):
        # Initialize Keyboard and Mouse Controllers
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

    def send_keyboard_command(self, command):
        """Simulate sending keyboard command (W, A, S, D)."""
        if command in ['w', 'a', 's', 'd']:
            self.keyboard.press(command)
            self.keyboard.release(command)
            print(f"Simulated sending command: {command}")
        else:
            print("Invalid command. Only 'W', 'A', 'S', 'D' are supported.")

    def send_mouse_movement(self, x, y):
        """Simulate mouse movement by setting the mouse position."""
        self.mouse.position = (x, y)
        print(f"Simulated moving mouse to: ({x}, {y})")

    def move_mouse_relative(self, dx, dy):
        """Move the mouse relative to its current position."""
        current_x, current_y = self.mouse.position
        self.mouse.position = (current_x + dx, current_y + dy)
        print(f"Simulated moving mouse by: ({dx}, {dy})")

    def get_last_command(self):
        """Placeholder for debug - returns the last simulated command (not implemented)."""
        return "None"  # No state is kept for simplicity.

    def get_last_mouse_move(self):
        """Placeholder for debug - returns the last simulated mouse movement (not implemented)."""
        return (0, 0)  # No state is kept for simplicity.
