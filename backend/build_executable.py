"""
Luna PyInstaller Build Script — Bundles FastAPI Backend & Tools into a single desktop executable.

Usage:
  python build_executable.py
"""

import os
import sys
import subprocess

def build():
    print("==========================================")
    print("   BUILDING LUNA DESKTOP EXECUTABLE       ")
    print("==========================================")

    backend_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(backend_dir, "main.py")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=LunaBackend",
        "--onefile",
        "--clean",
        f"--add-data={os.path.join(backend_dir, 'agent')};agent",
        f"--add-data={os.path.join(backend_dir, 'db')};db",
        f"--add-data={os.path.join(backend_dir, 'tools')};tools",
        main_script,
    ]

    print("Running command:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=backend_dir)
    if res.returncode == 0:
        print("Build Successful! Executable saved in backend/dist/LunaBackend.exe")
    else:
        print("Build failed with code:", res.returncode)

if __name__ == "__main__":
    build()
