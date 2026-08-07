"""
Luna Native Windows Desktop Floating Glassmorphic Orb Widget.
Runs directly on the Windows desktop as a frameless, 35% translucent, always-on-top floating orb.
Clicking the orb or speaking 'Hey Luna' pops open Luna's right-side desktop panel window.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import font
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("DesktopOrb")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class NativeDesktopOrb:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Luna Desktop Orb")
        
        # Frameless, always-on-top, translucent window
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.45)  # 45% translucent opacity
        
        # Window size and positioning (bottom right desktop corner)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        orb_size = 64
        x = screen_width - orb_size - 40
        y = screen_height - orb_size - 80
        self.root.geometry(f"{orb_size}x{orb_size}+{x}+{y}")

        # Dark Glassmorphic canvas styling
        self.root.configure(bg="#0F172A")
        
        self.canvas = tk.Canvas(
            self.root,
            width=orb_size,
            height=orb_size,
            bg="#0F172A",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Draw glowing ring & outer circle
        self.canvas.create_oval(4, 4, orb_size-4, orb_size-4, outline="#38BDF8", width=2, fill="#1E293B")
        self.canvas.create_oval(14, 14, orb_size-14, orb_size-14, outline="#F59E0B", width=2, fill="#0F172A")

        # Draw "L" Mark text in center
        try:
            custom_font = font.Font(family="Segoe UI", size=16, weight="bold")
            self.canvas.create_text(orb_size//2, orb_size//2, text="🌙", font=custom_font, fill="#F8FAFC")
        except Exception:
            self.canvas.create_text(orb_size//2, orb_size//2, text="L", fill="#F8FAFC", font=("Arial", 16, "bold"))

        # Mouse hover effects & click binding
        self.root.bind("<Enter>", self.on_hover)
        self.root.bind("<Leave>", self.on_leave)
        self.root.bind("<Button-1>", self.on_click)
        
        # Draggable window behavior
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.x = 0
        self.y = 0

        log.info(f"Native Desktop Orb Active at position ({x}, {y})")

    def on_hover(self, event):
        self.root.attributes("-alpha", 0.95)  # Become fully visible on hover

    def on_leave(self, event):
        self.root.attributes("-alpha", 0.45)  # Return to translucent opacity

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.root.winfo_x() + deltax
        new_y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{new_x}+{new_y}")

    def on_click(self, event=None):
        log.info("Native Desktop Orb clicked! Popping open Luna Panel...")
        hud_script = os.path.join(ROOT_DIR, "launch_hud.py")
        subprocess.Popen([sys.executable, hud_script])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    orb = NativeDesktopOrb()
    orb.run()
