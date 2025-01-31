import tkinter as tk
from tkinter import Canvas
import random
import threading
import pystray
from PIL import Image, ImageTk, ImageDraw
import math

# Configuration variables
snow_speed = 3          # Speed of snowflakes (1 = slow, 10 = fast)
snow_size = 10          # Base size of snowflakes (in pixels)
sway_intensity = 0.5      # How much snowflakes sway left and right (higher = more sway)
sway_speed = 0.01       # How fast snowflakes sway (higher = faster sway)

# Snowflake class
class Snowflake:
    def __init__(self, canvas, x, y, size, speed, image):
        self.canvas = canvas
        self.image = image
        self.size = size
        self.speed = speed
        self.id = canvas.create_image(x, y, image=self.image, anchor=tk.NW)
        self.falling = True
        self.angle = random.uniform(0, 2 * math.pi)  # Random starting angle for swaying

    def fall(self):
        if self.falling:
            # Calculate swaying motion using sine wave
            sway_offset = math.sin(self.angle) * sway_intensity
            self.canvas.move(self.id, sway_offset, self.speed)
            self.angle += sway_speed  # Increment angle for smooth swaying

            # Reset snowflake to the top when it reaches the bottom
            x, y = self.canvas.coords(self.id)
            if y > self.canvas.winfo_height():
                self.canvas.coords(self.id, x, -self.size)
            self.canvas.after(30, self.fall)

# Main application
class SnowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Let It Snow!")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)  # Stay on top of the desktop
        self.root.attributes("-transparentcolor", "black")  # Make the background transparent
        self.root.config(bg="black")

        self.canvas = Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.snowflakes = []
        self.create_snowflakes()
        self.start_system_tray()

    def create_snowflake_image(self, base_size):
        """Create a snowball image with very small differences."""
        # Randomize size slightly (within 95% to 105% of base size)
        size = random.randint(int(base_size * 0.95), int(base_size * 1.05))

        # Create a transparent image
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw a perfect white circle
        draw.ellipse((0, 0, size, size), fill=(255, 255, 255, 255))  # Fully opaque white

        return ImageTk.PhotoImage(image)

    def create_snowflakes(self):
        for _ in range(100):  # Number of snowflakes
            x = random.randint(0, self.root.winfo_screenwidth())
            y = random.randint(-self.root.winfo_screenheight(), 0)
            speed = snow_speed
            snowflake_image = self.create_snowflake_image(snow_size)  # Unique snowball
            snowflake = Snowflake(self.canvas, x, y, snow_size, speed, snowflake_image)
            self.snowflakes.append(snowflake)
            snowflake.fall()

    def start_system_tray(self):
        def stop_snow(icon, item):
            self.root.destroy()
            icon.stop()

        # Create a system tray icon
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill="white")  # Simple white circle for the tray icon
        menu = pystray.Menu(pystray.MenuItem("Stop Snow", stop_snow))
        icon = pystray.Icon("snow_icon", image, "Let It Snow!", menu)

        threading.Thread(target=icon.run, daemon=True).start()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SnowApp(root)
    root.mainloop()