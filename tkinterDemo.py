# Development of base example Week Beginning Feb 2nd 2024

'''
See tkinterBaseFromAI.py for origins of this code.




'''

import tkinter as tk
from tkinter import ttk

class ValueDisplay(tk.Tk):
    
    """A simple GUI to display and adjust values using Tkinter.
    
    This class creates a GUI with descriptions and adjustable values
    for temperatures or times, including increase/decrease buttons for
    each value and forward/backward navigation buttons.
    """
    def __init__(self):
        super().__init__()
        self.geometry("480x320")  # Adjust as per your screen resolution
        self.title("Value Display")

        # Define initial values
        self.value1 = tk.StringVar(value="00:00")
        self.value2 = tk.StringVar(value="0°C")

        self.create_widgets()

    def create_widgets(self):
        # Descriptions
        tk.Label(self, text="Time (Hours:Minutes)").place(x=60, y=20)
        tk.Label(self, text="Temperature (°C)").place(x=300, y=20)

        # Value display
        tk.Label(self, textvariable=self.value1, font=("Arial", 20)).place(x=60, y=50)
        tk.Label(self, textvariable=self.value2, font=("Arial", 20)).place(x=300, y=50)

        # Increase/Decrease buttons for Value1
        tk.Button(self, text="+", command=lambda: self.adjust_value(self.value1, 1)).place(x=60, y=100)
        tk.Button(self, text="-", command=lambda: self.adjust_value(self.value1, -1)).place(x=100, y=100)

        # Increase/Decrease buttons for Value2
        tk.Button(self, text="+", command=lambda: self.adjust_value(self.value2, 1, True)).place(x=300, y=100)
        tk.Button(self, text="-", command=lambda: self.adjust_value(self.value2, -1, True)).place(x=340, y=100)

        # Forward/Backward buttons
        tk.Button(self, text="<<<", command=self.move_backward).place(x=10, y=150)
        tk.Button(self, text=">>>", command=self.move_forward).place(x=400, y=150)

    def adjust_value(self, value_var, delta, is_temperature=False):
        """Adjusts the value based on delta. Can handle time and temperature."""
        if is_temperature:
            current_value = int(value_var.get().replace("°C", ""))
            new_value = current_value + delta
            value_var.set(f"{new_value}°C")
        else:
            # Simplified time adjustment, assumes format "HH:MM"
            current_value = value_var.get()
            hours, minutes = map(int, current_value.split(":"))
            minutes += delta
            if minutes >= 60:
                hours += 1
                minutes = 0
            elif minutes < 0:
                hours -= 1
                minutes = 59
            # Adjust for hours overflow in a simple manner
            hours = hours % 24
            value_var.set(f"{hours:02d}:{minutes:02d}")

    def move_forward(self):
        """Placeholder for forward navigation functionality."""
        print("Move Forward")

    def move_backward(self):
        """Placeholder for backward navigation functionality."""
        print("Move Backward")

if __name__ == '__main__':
    app = ValueDisplay()
    app.mainloop()
