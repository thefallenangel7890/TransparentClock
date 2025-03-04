import sys  # Import system-specific parameters and functions
import time  # Import time module to handle date and time functions
import pyautogui  # Import PyAutoGUI for screen interactions (not used in this script)
from PyQt5.QtWidgets import QApplication, QLabel, QWidget  # Import PyQt5 classes for GUI components
from PyQt5.QtCore import Qt, QTimer  # Import Qt core functionalities for window behavior and timers
from PyQt5.QtGui import QFont  # Import QFont to set custom fonts
from PIL import ImageGrab  # Import ImageGrab from PIL to capture screen pixels

class TransparentClock(QWidget):  # Define a class for the transparent clock widget
    def __init__(self):  # Initialize the widget
        super().__init__()  # Call the constructor of the parent QWidget class

        # Set window properties: frameless, always on top, and treated as a tool window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the background transparent
        self.setGeometry(1200, 2, 250, 50)  # Set initial position and size of the clock window

        # Create a label for the date display
        self.date_label = QLabel(self)
        self.date_label.setFont(QFont("Bahnschrift SemiBold", 12))  # Set font type and size
        self.date_label.setAlignment(Qt.AlignCenter)  # Center-align the text

        # Create a label for the clock display
        self.clock_label = QLabel(self)
        self.clock_label.setFont(QFont("Bahnschrift SemiBold", 15))  # Set font type and size
        self.clock_label.setAlignment(Qt.AlignCenter)  # Center-align the text

        # Set positions for labels within the widget
        self.date_label.setGeometry(0, 0, 250, 20)  # Position date label at the top
        self.clock_label.setGeometry(0, 20, 250, 30)  # Position clock label below the date

        # Create a timer that updates the clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)  # Connect the timer signal to the update function
        self.timer.start(1000)  # Set timer interval to 1000ms (1 second)

        self.update_time()  # Initial update of time and date

    def get_background_brightness(self):  # Function to determine background brightness
        """Capture the brightness of the background behind the clock."""
        x, y = self.x() + (self.width() // 2), self.y() + (self.height() // 2)  # Get center coordinates of the widget
        screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))  # Capture a 1x1 pixel area at the center
        pixel = screenshot.getpixel((0, 0))  # Extract RGB values of the pixel
        brightness = (0.299 * pixel[0]) + (0.587 * pixel[1]) + (0.114 * pixel[2])  # Calculate brightness using standard formula
        return "white" if brightness < 128 else "black"  # Return text color based on brightness level

    def update_time(self):  # Function to update date and time display
        """Update the date and time labels dynamically."""
        current_date = time.strftime("%A, %d %B %Y")  # Get current date in format: Monday, 04 March 2025
        current_time = time.strftime("%I:%M:%S %p")  # Get current time in 12-hour format with AM/PM

        text_color = self.get_background_brightness()  # Get adaptive text color based on background brightness

        # Update labels with formatted date and time, applying the chosen text color
        self.date_label.setText(f"<font color='{text_color}'>{current_date}</font>")
        self.clock_label.setText(f"<font color='{text_color}'>{current_time}</font>")

if __name__ == "__main__":  # Check if the script is being run directly
    app = QApplication(sys.argv)  # Create the application instance
    clock = TransparentClock()  # Create an instance of the TransparentClock widget
    clock.show()  # Display the clock window
    sys.exit(app.exec_())  # Start the event loop and exit cleanly when closed
