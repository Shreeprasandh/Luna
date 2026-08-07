"""
Luna Native Windows OS Floating Desktop Glassmorphic Orb Widget.
Uses Windows Win32 API (ctypes / user32.dll) to force HWND_TOPMOST always-on-top positioning
over ALL Windows applications, desktop wallpapers, and taskbars.
"""

import sys
import os
import ctypes
import subprocess
import tkinter as tk
from tkinter import font
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("NativeWinOrb")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Win32 Constants
HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_TOPMOST = 0x00000008
WS_EX_LAYERED = 0x00080000


class NativeWindowsOrb:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Luna OS Orb")

        # 1. Window Sizing & Position (bottom right corner)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        orb_w, orb_h = 70, 70
        x_pos = max(50, screen_w - orb_w - 60)
        y_pos = max(50, screen_h - orb_h - 120)

        self.root.geometry(f"{orb_w}x{orb_h}+{x_pos}+{y_pos}")

        # 2. Tkinter Frameless Configuration
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.90)  # High visibility

        # Set transparent color key for Windows
        TRANS_COLOR = "#0F0F0F"
        self.root.configure(bg=TRANS_COLOR)
        try:
            self.root.wm_attributes("-transparentcolor", TRANS_COLOR)
        except Exception:
            pass

        # 3. Canvas Drawing (Vibrant Neon Glass Orb)
        self.canvas = tk.Canvas(
            self.root,
            width=orb_w,
            height=orb_h,
            bg=TRANS_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Outer Neon Cyan Glow Ring
        self.canvas.create_oval(4, 4, orb_w - 4, orb_h - 4, outline="#38BDF8", width=3, fill="#0F172A")
        # Inner Amber Ring
        self.canvas.create_oval(12, 12, orb_w - 12, orb_h - 12, outline="#F59E0B", width=2, fill="#1E293B")
        
        # Center Moon Emoji / Text Mark
        try:
            custom_font = font.Font(family="Segoe UI Emoji", size=22, weight="bold")
            self.canvas.create_text(orb_w // 2, orb_h // 2, text="🌙", font=custom_font, fill="#F8FAFC")
        except Exception:
            self.canvas.create_text(orb_w // 2, orb_h // 2, text="L", fill="#F8FAFC", font=("Arial", 20, "bold"))

        # 4. Enforce Native Windows OS HWND_TOPMOST via user32.dll
        self.enforce_win32_topmost()

        # 5. Interaction Bindings
        self.root.bind("<Enter>", self.on_hover)
        self.root.bind("<Leave>", self.on_leave)
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.start_x = 0
        self.start_y = 0
        self.is_dragging = False

        log.info(f"Native Windows OS Orb Initialized at ({x_pos}, {y_pos})")

    def enforce_win32_topmost(self):
        """Uses ctypes user32.dll to pin window to HWND_TOPMOST OS layer."""
        if os.name != "nt":
            return
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if not hwnd:
                hwnd = self.root.winfo_id()

            # Set WS_EX_TOOLWINDOW so it doesn't clutter taskbar
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_TOOLWINDOW | WS_EX_TOPMOST)

            # Pin to HWND_TOPMOST (-1)
            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
            )
            log.info("Successfully pinned Native Orb to Windows HWND_TOPMOST layer.")
        except Exception as e:
            log.warning(f"Win32 Topmost Pin Notice: {e}")

    def on_hover(self, event):
        self.root.attributes("-alpha", 1.0)
        self.enforce_win32_topmost()

    def on_leave(self, event):
        self.root.attributes("-alpha", 0.90)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.is_dragging = False

    def on_drag(self, event):
        self.is_dragging = True
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        nx = self.root.winfo_x() + dx
        ny = self.root.winfo_y() + dy
        self.root.geometry(f"+{nx}+{ny}")

    def on_release(self, event):
        if not self.is_dragging:
            log.info("Native OS Orb clicked! Launching Luna Desktop Panel...")
            hud_script = os.path.join(ROOT_DIR, "launch_hud.py")
            subprocess.Popen([sys.executable, hud_script])

    def run(self):
        # Periodically re-enforce topmost status every 3 seconds
        def keep_topmost():
            self.enforce_win32_topmost()
            self.root.after(3000, keep_topmost)

        self.root.after(1000, keep_topmost)
        self.root.mainloop()


if __name__ == "__main__":
    orb = NativeWindowsOrb()
    orb.run()
