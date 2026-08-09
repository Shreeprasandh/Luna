"""
Luna Native Windows OS Floating Desktop Glassmorphic Orb Widget — 4K High-Res Sharp Rendering.
Uses PIL supersampling (4x anti-aliasing LANCZOS) to render Sir's exact official vector brand logo mark with zero pixelation.
Uses Windows Win32 API (ctypes / user32.dll) to force HWND_TOPMOST always-on-top positioning.
"""

import sys
import os
import ctypes
import subprocess
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
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
        self.orb_size = 76
        x_pos = max(50, screen_w - self.orb_size - 60)
        y_pos = max(50, screen_h - self.orb_size - 120)

        self.root.geometry(f"{self.orb_size}x{self.orb_size}+{x_pos}+{y_pos}")

        # 2. Tkinter Frameless Configuration
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.90)

        # Transparent color key
        TRANS_COLOR = "#000001"
        self.root.configure(bg=TRANS_COLOR)
        try:
            self.root.wm_attributes("-transparentcolor", TRANS_COLOR)
        except Exception:
            pass

        # 3. Canvas & 4K High-Res Sharp Render Image
        self.canvas = tk.Canvas(
            self.root,
            width=self.orb_size,
            height=self.orb_size,
            bg=TRANS_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Generate 4x Supersampled Anti-Aliased High-Res Logo Image
        self.logo_img = self.render_crisp_logo_image(size=self.orb_size)
        self.canvas.create_image(0, 0, anchor="nw", image=self.logo_img)

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

        log.info(f"4K High-Res Crisp Native Desktop Orb Active at ({x_pos}, {y_pos})")

    def render_crisp_logo_image(self, size: int) -> ImageTk.PhotoImage:
        """
        Renders Sir's official logo mark at 4x supersampled resolution (4 * size) using PIL,
        then resizes down with LANCZOS filter for smooth anti-aliased 4K vector sharpness!
        """
        scale = 4
        S_size = size * scale
        img = Image.new("RGBA", (S_size, S_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Outer Neon Cyan Glow Ring (radius = S_size/2 - 8)
        cx, cy = S_size / 2, S_size / 2
        r_outer = (S_size / 2) - 8
        draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=(56, 189, 248, 255), width=int(10 * scale / 4), fill=(15, 23, 42, 240))

        # Inner Surface Circle
        r_inner = r_outer - 14
        draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], outline=(51, 65, 85, 255), width=int(5 * scale / 4), fill=(30, 41, 59, 255))

        # Official Logo Vector Coordinates (Viewbox 0..100) inside center
        box_offset = (S_size - (60 * scale / 4)) / 2
        logo_scale = 0.60 * scale

        def V(x_val: float) -> float:
            return box_offset + (x_val * logo_scale / 4)

        # Central Solid Charcoal Square (32..68)
        draw.rectangle([V(32), V(32), V(68), V(68)], fill=(15, 23, 42, 255), outline=(56, 189, 248, 255), width=int(6 * scale / 4))

        # Left Path Bracket: (45,18) -> (18,18) -> (18,82) -> (45,82)
        left_pts = [(V(45), V(18)), (V(18), V(18)), (V(18), V(82)), (V(45), V(82))]
        draw.line(left_pts, fill=(148, 163, 184, 255), width=int(10 * scale / 4), joint="miter")

        # Top & Bottom Left Circular Amber Nodes (r=6.5)
        node_r = 6.5 * logo_scale / 4
        draw.ellipse([V(45) - node_r, V(18) - node_r, V(45) + node_r, V(18) + node_r], fill=(245, 158, 11, 255), outline=(15, 23, 42, 255), width=int(4 * scale / 4))
        draw.ellipse([V(45) - node_r, V(82) - node_r, V(45) + node_r, V(82) + node_r], fill=(245, 158, 11, 255), outline=(15, 23, 42, 255), width=int(4 * scale / 4))

        # Right Path Bracket: (58,82) -> (82,82) -> (82,18) -> (68,18)
        right_pts = [(V(58), V(82)), (V(82), V(82)), (V(82), V(18)), (V(68), V(18))]
        draw.line(right_pts, fill=(148, 163, 184, 255), width=int(10 * scale / 4), joint="miter")

        # Directional Triangle pointing Left: (68,10), (52,18), (68,26)
        tri_pts = [(V(68), V(10)), (V(52), V(18)), (V(68), V(26))]
        draw.polygon(tri_pts, fill=(248, 250, 252, 255))

        # Downsample using LANCZOS for super-crisp 4K anti-aliasing
        img_resized = img.resize((size, size), Image.Resampling.LANCZOS)

        # Convert transparent pixels to keying color #000001
        bg_key = Image.new("RGBA", (size, size), (0, 0, 1, 255))
        composite = Image.alpha_composite(bg_key, img_resized)

        return ImageTk.PhotoImage(composite)

    def enforce_win32_topmost(self):
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
