"""
Luna Native Windows Desktop Floating Glassmorphic Orb Widget.
Runs directly on the Windows desktop as a transparent, glowing, always-on-top circular orb.
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

        # Transparent canvas background color key
        TRANSPARENT_COLOR = "#000001"
        
        # Frameless, always-on-top, transparent window
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)  # 85% high visibility
        
        try:
            self.root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        except Exception as e:
            log.warning(f"Transparent color key not supported: {e}")

        # Window size and positioning (bottom right desktop corner, elevated above taskbar)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        orb_size = 72
        x = max(100, screen_width - orb_size - 100)
        y = max(100, screen_height - orb_size - 180)
        self.root.geometry(f"{orb_size}x{orb_size}+{x}+{y}")

        self.root.configure(bg=TRANSPARENT_COLOR)
        
        self.canvas = tk.Canvas(
            self.root,
            width=orb_size,
            height=orb_size,
            bg=TRANSPARENT_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Draw glowing neon outer ring & inner circle
        self.canvas.create_oval(4, 4, orb_size-4, orb_size-4, outline="#38BDF8", width=3, fill="#0F172A")
        self.canvas.create_oval(12, 12, orb_size-12, orb_size-12, outline="#F59E0B", width=2, fill="#1E293B")

        # Draw "🌙" icon mark in center
        try:
            custom_font = font.Font(family="Segoe UI Emoji", size=20, weight="bold")
            self.canvas.create_text(orb_size//2, orb_size//2, text="🌙", font=custom_font, fill="#F8FAFC")
        except Exception:
            self.canvas.create_text(orb_size//2, orb_size//2, text="L", fill="#F8FAFC", font=("Arial", 18, "bold"))

        # Mouse hover effects & click binding
        self.root.bind("<Enter>", self.on_hover)
        self.root.bind("<Leave>", self.on_leave)
        
        # Click & drag behavior
        self.canvas.bind("<ButtonPress-1>", self.on_click_down)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_click_up)

        self.x = 0
        self.y = 0
        self.dragged = False

        log.info(f"Native Desktop Orb Active at position ({x}, {y})")

    def on_hover(self, event):
        self.root.attributes("-alpha", 1.0)  # 100% full opacity on hover

    def on_leave(self, event):
        self.root.attributes("-alpha", 0.85)

    def on_click_down(self, event):
        self.x = event.x
        self.y = event.y
        self.dragged = False

    def do_move(self, event):
        self.dragged = True
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.root.winfo_x() + deltax
        new_y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{new_x}+{new_y}")

    def on_click_up(self, event):
        if not self.dragged:
            log.info("Native Desktop Orb clicked! Popping open Luna Panel...")
            hud_script = os.path.join(ROOT_DIR, "launch_hud.py")
            subprocess.Popen([sys.executable, hud_script])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    orb = NativeDesktopOrb()
    orb.run()
