"""
Luna Native Windows OS Floating Desktop Glassmorphic Orb Widget.
Uses Windows Win32 API (ctypes / user32.dll) to force HWND_TOPMOST always-on-top positioning.
Renders Sir's EXACT official vector brand logo mark (Central Charcoal Square, Bracket Nodes & Directional Arrow).
"""

import sys
import os
import ctypes
import subprocess
import tkinter as tk
from typing import Any
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


class NativeWindowsOrb:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Luna OS Orb")

        # 1. Window Sizing & Position (bottom right corner)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.orb_w, self.orb_h = 74, 74
        x_pos = max(50, screen_w - self.orb_w - 60)
        y_pos = max(50, screen_h - self.orb_h - 120)

        self.root.geometry(f"{self.orb_w}x{self.orb_h}+{x_pos}+{y_pos}")

        # 2. Tkinter Frameless Configuration
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.90)

        # Set transparent color key for Windows
        TRANS_COLOR = "#000001"
        self.root.configure(bg=TRANS_COLOR)
        try:
            self.root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        except Exception:
            pass

        # 3. Canvas Drawing (Vibrant Neon Glass Orb)
        self.canvas = tk.Canvas(
            self.root,
            width=self.orb_w,
            height=self.orb_h,
            bg=TRANS_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Outer Neon Cyan Glow Ring & Dark Surface Inner Circle
        self.canvas.create_oval(3, 3, self.orb_w - 3, self.orb_h - 3, outline="#38BDF8", width=3, fill="#0F172A")
        self.canvas.create_oval(9, 9, self.orb_w - 9, self.orb_h - 9, outline="#334155", width=1.5, fill="#1E293B")

        # Render Sir's EXACT Official Vector Logo Mark inside the Orb
        self.draw_official_vector_logo(x_offset=17, y_offset=17, scale=0.40)

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

    def draw_official_vector_logo(self, x_offset: float, y_offset: float, scale: float):
        """
        Draws Sir's exact official vector brand logo mark onto Tkinter canvas:
        - Central Charcoal Square (32..68)
        - Left Path Bracket with Amber Nodes at top & bottom
        - Right Path Bracket with Left-pointing Directional Triangle
        """
        def S(val: float) -> float:
            return x_offset + (val * scale)

        # Central Solid Charcoal Square
        self.canvas.create_rectangle(
            S(32), S(32), S(68), S(68),
            fill="#0F172A", outline="#38BDF8", width=2
        )

        # Left Path Bracket: (45,18) -> (18,18) -> (18,82) -> (45,82)
        left_pts = [S(45), S(18), S(18), S(18), S(18), S(82), S(45), S(82)]
        self.canvas.create_line(left_pts, fill="#94A3B8", width=3, capstyle="square")

        # Top Left Circular Node (45, 18)
        r = 3.5
        self.canvas.create_oval(S(45) - r, S(18) - r, S(45) + r, S(18) + r, fill="#F59E0B", outline="#0F172A", width=1.5)
        # Bottom Left Circular Node (45, 82)
        self.canvas.create_oval(S(45) - r, S(82) - r, S(45) + r, S(82) + r, fill="#F59E0B", outline="#0F172A", width=1.5)

        # Right Path Bracket: (58,82) -> (82,82) -> (82,18) -> (68,18)
        right_pts = [S(58), S(82), S(82), S(82), S(82), S(18), S(68), S(18)]
        self.canvas.create_line(right_pts, fill="#94A3B8", width=3, capstyle="square")

        # Directional Triangle pointing Left: (68,10), (52,18), (68,26)
        tri_pts = [S(68), S(10), S(52), S(18), S(68), S(26)]
        self.canvas.create_polygon(tri_pts, fill="#F8FAFC", outline="")

    def enforce_win32_topmost(self):
        """Uses ctypes user32.dll to pin window to HWND_TOPMOST OS layer."""
        if os.name != "nt":
            return
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            if not hwnd:
                hwnd = self.root.winfo_id()

            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_TOOLWINDOW | WS_EX_TOPMOST)

            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
            )
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
        def keep_topmost():
            self.enforce_win32_topmost()
            self.root.after(3000, keep_topmost)

        self.root.after(1000, keep_topmost)
        self.root.mainloop()


if __name__ == "__main__":
    orb = NativeWindowsOrb()
    orb.run()
