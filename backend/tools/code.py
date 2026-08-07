"""
Code Execution Tool — Isolated Python code evaluation engine.
Allows Luna to test, execute, and verify code logic dynamically.
"""

import sys
import time
import subprocess
import tempfile
import logging
from typing import Any

log = logging.getLogger(__name__)


def execute_python_code(code: str, timeout_seconds: int = 10) -> dict[str, Any]:
    """
    Executes a snippet of Python code in an isolated subprocess and returns execution results.

    Args:
        code: Python source code string to execute.
        timeout_seconds: Execution timeout limit in seconds (default 10).

    Returns:
        Dict containing status, returncode, stdout, stderr, and execution_time_ms.
    """
    log.info(f"[Tool: execute_python_code] Running code snippet ({len(code)} chars)...")

    # Create temporary python script file
    temp_script = tempfile.NamedTemporaryFile(suffix=".py", mode="w", encoding="utf-8", delete=False)
    temp_path = temp_script.name
    try:
        temp_script.write(code)
        temp_script.close()

        start_time = time.time()
        res = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "status": "success" if res.returncode == 0 else "error",
            "returncode": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "execution_time_ms": elapsed_ms,
        }

    except subprocess.TimeoutExpired:
        log.error(f"[Tool: execute_python_code] Code execution timed out after {timeout_seconds}s")
        return {
            "status": "error",
            "message": f"Code execution timed out after {timeout_seconds} seconds.",
            "stdout": "",
            "stderr": "TimeoutExpired",
        }
    except Exception as e:
        log.error(f"[Tool: execute_python_code] Execution error: {e}")
        return {
            "status": "error",
            "message": f"Failed to execute code: {str(e)}",
            "stdout": "",
            "stderr": str(e),
        }
    finally:
        import os
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
