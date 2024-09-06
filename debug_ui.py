# debug_ui.py
import tkinter as tk


class DebugUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debug UI")

        # WASD Command Display
        self.wasd_label = tk.Label(self.root, text="WASD Command: None", font=("Arial", 16))
        self.wasd_label.pack(pady=10)

        # Head Rotation Display
        self.head_rotation_label = tk.Label(self.root, text="Head Rotation: X=0, Y=0", font=("Arial", 16))
        self.head_rotation_label.pack(pady=10)

        # Update loop for UI
        self.root.after(100, self.update_ui)

    def update_wasd_command(self, command):
        self.wasd_label.config(text=f"WASD Command: {command}")

    def update_head_rotation(self, rotation_x, rotation_y):
        self.head_rotation_label.config(text=f"Head Rotation: X={rotation_x:.2f}, Y={rotation_y:.2f}")

    def update_ui(self):
        self.root.update()

    def run(self):
        self.root.mainloop()


# Usage Example (if run standalone):
if __name__ == "__main__":
    ui = DebugUI()
    ui.run()