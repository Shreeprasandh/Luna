"""
Window Opacity & Fullscreen Controller Tool — Adjusts Luna window transparency and fullscreen state.
"""

import subprocess
import logging
from typing import Any

log = logging.getLogger(__name__)


def set_window_opacity(opacity_percent: int = 100) -> dict[str, Any]:
    """
    Adjusts the opacity/transparency percentage of Luna's desktop window (e.g. 10%, 50%, 100%).

    Args:
        opacity_percent: Opacity level percentage from 10 (90% transparent) to 100 (opaque).
    """
    level = max(10, min(100, opacity_percent))
    alpha = int((level / 100.0) * 255)
    log.info(f"[Tool: set_window_opacity] Setting window opacity to {level}% (alpha={alpha})...")

    try:
        # PowerShell script using Win32 SetLayeredWindowAttributes to adjust active window opacity
        ps_cmd = f"""
        $code = '[DllImport("user32.dll")] public static extern bool SetLayeredWindowAttributes(IntPtr hwnd, uint crKey, byte bAlpha, uint dwFlags); [DllImport("user32.dll")] public static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong); [DllImport("user32.dll")] public static extern int GetWindowLong(IntPtr hWnd, int nIndex);'
        $type = Add-Type -MemberDefinition $code -Name 'Win32Opacity' -Namespace 'Win32' -PassThru
        $hwnd = (Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {{ $_.MainWindowTitle -like "*Luna*" }}).MainWindowHandle
        if ($hwnd) {{
            $style = $type::GetWindowLong($hwnd, -20)
            $type::SetWindowLong($hwnd, -20, $style -bor 0x80000)
            $type::SetLayeredWindowAttributes($hwnd, 0, [byte]{alpha}, 2)
        }}
        """
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)

        return {
            "status": "success",
            "opacity_percent": level,
            "message": f"Adjusted window opacity to {level}%.",
        }
    except Exception as e:
        log.error(f"[Tool: set_window_opacity] Error: {e}")
        return {"status": "error", "message": f"Failed to set opacity: {str(e)}"}


def toggle_fullscreen(enable: bool = True) -> dict[str, Any]:
    """
    Toggles fullscreen mode for Luna's window.

    Args:
        enable: True for fullscreen, False for standard sidepanel window mode.
    """
    log.info(f"[Tool: toggle_fullscreen] Setting fullscreen mode to {enable}...")
    try:
        key_code = "{F11}" if enable else "%{ENTER}"
        ps_cmd = f"$wshShell = New-Object -ComObject WScript.Shell; $wshShell.SendKeys('{key_code}')"
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)

        return {
            "status": "success",
            "fullscreen": enable,
            "message": f"Toggled window fullscreen mode (fullscreen={enable}).",
        }
    except Exception as e:
        log.error(f"[Tool: toggle_fullscreen] Error: {e}")
        return {"status": "error", "message": f"Fullscreen toggle failed: {str(e)}"}
