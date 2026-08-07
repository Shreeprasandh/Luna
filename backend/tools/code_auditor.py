"""
Automated Code Refactoring & Lint Auditor Tool — Audits local code files for syntax errors and formatting.
"""

import os
import ast
import logging
from typing import Any

log = logging.getLogger(__name__)


def audit_code_file(filepath: str) -> dict[str, Any]:
    """
    Audits a Python or text code file for syntax errors, line count, and structural health.

    Args:
        filepath: Path to code file to inspect.
    """
    abs_path = os.path.abspath(filepath)
    log.info(f"[Tool: audit_code_file] Auditing code file '{abs_path}'...")

    if not os.path.exists(abs_path):
        return {"status": "error", "message": f"File not found: '{filepath}'"}

    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            code_text = f.read()

        line_count = len(code_text.splitlines())
        syntax_valid = True
        syntax_error = None

        if abs_path.endswith(".py"):
            try:
                ast.parse(code_text)
            except SyntaxError as se:
                syntax_valid = False
                syntax_error = f"Line {se.lineno}: {se.msg}"

        return {
            "status": "success",
            "filepath": abs_path,
            "line_count": line_count,
            "syntax_valid": syntax_valid,
            "syntax_error": syntax_error,
            "message": f"Audited '{os.path.basename(abs_path)}' ({line_count} lines, syntax_valid={syntax_valid}).",
        }
    except Exception as e:
        log.error(f"[Tool: audit_code_file] Error: {e}")
        return {"status": "error", "message": f"Code audit failed: {str(e)}"}
