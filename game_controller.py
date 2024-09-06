# game_controller.py
import pyautogui

class GameController:
    def __init__(self):
        pass

    def send_keyboard_command(self, command):
        if command:
            pyautogui.press(command)

    def send_mouse_movement(self, x, y):
        pyautogui.moveRel(x, y)
