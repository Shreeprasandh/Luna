"""
Epsilon Test Sentinel — Automated API test suite covering FastAPI routes.
"""

import sys
import os

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "zero_token_waste" in data
    assert "system" in data
    assert "safety_switches" in data


def test_session_lifecycle():
    # Start session
    start_res = client.post("/session/start")
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]
    assert session_id is not None

    # End session
    end_res = client.post("/session/end", json={"session_id": session_id})
    assert end_res.status_code == 200
    assert end_res.json()["status"] == "ended"


def test_chat_invalid_session():
    res = client.post("/chat", json={"session_id": "invalid-session-id", "text": "Hello"})
    assert res.status_code == 404


def test_system_health_tool():
    from tools.system import get_system_health
    res = get_system_health()
    assert res["status"] == "success"
    assert "cpu" in res
    assert "ram" in res


def test_git_status_tool():
    from tools.git_agent import git_status
    res = git_status()
    assert res["status"] == "success"
    assert res["branch"] == "main"


def test_safety_guard_path_traversal():
    from tools.safety import validate_tool_execution
    # Path traversal attempt outside workspace
    res = validate_tool_execution("read_file", {"filepath": "C:\\Windows\\System32\\drivers\\etc\\hosts"})
    assert res["allowed"] is False
    assert "outside safe workspace" in res["reason"]


def test_high_risk_tool_classification():
    from tools.safety import validate_tool_execution
    res = validate_tool_execution("send_email", {"to": "test@example.com"})
    assert res["is_high_risk"] is True


def test_scheduler_tool():
    from tools.scheduler import schedule_reminder, list_scheduled_tasks
    res = schedule_reminder("Test reminder", 100)
    assert res["status"] == "success"
    assert "task_id" in res

    tasks_res = list_scheduled_tasks()
    assert tasks_res["status"] == "success"
    assert tasks_res["count"] >= 1


def test_clipboard_tools():
    from tools.clipboard import set_clipboard_text, get_clipboard_text
    set_res = set_clipboard_text("Luna Test Clipboard")
    assert set_res["status"] == "success"

    get_res = get_clipboard_text()
    assert get_res["status"] == "success"
    assert get_res["content"] == "Luna Test Clipboard"


def test_network_tool():
    from tools.network import get_network_diagnostics
    res = get_network_diagnostics()
    assert res["status"] == "success"
    assert "local_ip" in res


def test_file_search_tool():
    from tools.file_search import search_local_files
    res = search_local_files("*.py", search_dir="tools")
    assert res["status"] == "success"
    assert res["match_count"] > 0


def test_audio_tools():
    from tools.audio import set_master_volume
    res = set_master_volume(50)
    assert res["status"] == "success"


def test_weather_tool():
    from tools.weather import get_weather
    res = get_weather("London")
    assert res["status"] == "success"
    assert "temperature_celsius" in res


def test_powertoys_awake_tool():
    from tools.powertoys import toggle_awake_mode
    res = toggle_awake_mode(True)
    assert res["status"] == "success"
    assert res["awake_enabled"] is True


def test_port_scanner_tool():
    from tools.port_scanner import get_open_ports
    res = get_open_ports()
    assert res["status"] == "success"
    assert "open_port_count" in res


def test_disk_cleaner_tool():
    from tools.disk_cleaner import find_large_files
    res = find_large_files("tools", min_size_mb=1)
    assert res["status"] == "success"
    assert "found_count" in res


def test_spotify_youtube_canva_tools():
    from tools.media import get_song_lyrics
    from tools.youtube import play_youtube_video
    from tools.canva import open_canva_design

    lyrics_res = get_song_lyrics("Bohemian Rhapsody")
    assert lyrics_res["status"] == "success"

    yt_res = play_youtube_video("SpaceX launch")
    assert yt_res["status"] == "success"

    canva_res = open_canva_design("invitation", "birthday")
    assert canva_res["status"] == "success"


def test_window_opacity_tool():
    from tools.window import set_window_opacity
    res = set_window_opacity(80)
    assert res["status"] == "success"
    assert res["opacity_percent"] == 80


def test_power_and_briefing_tools():
    from tools.power import get_power_status
    from tools.briefing import generate_morning_briefing

    p_res = get_power_status()
    assert p_res["status"] == "success"

    b_res = generate_morning_briefing("London")
    assert b_res["status"] == "success"
    assert len(b_res["executive_summary_points"]) == 3


def test_remote_mobile_tool():
    from tools.remote_mobile import get_mobile_remote_url
    res = get_mobile_remote_url()
    assert res["status"] == "success"
    assert "mobile_panel_url" in res


def test_extreme_risk_password_guard():
    from tools.safety import validate_tool_execution

    # Test without password -> BLOCKED
    res1 = validate_tool_execution("write_file", {"filepath": "test.txt", "content": "delete_drive format_c"})
    assert res1["allowed"] is False
    assert "ONE PIECE" in res1["reason"]

    # Test with correct password -> ALLOWED
    res2 = validate_tool_execution("write_file", {"filepath": "test.txt", "content": "delete_drive format_c", "password": "ONE PIECE"})
    assert res2["allowed"] is True


def test_magic_identity_word():
    from auth import verify_magic_word
    assert verify_magic_word("lusu") is True
    assert verify_magic_word("wrong_word") is False














