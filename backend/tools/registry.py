"""
Tool Registry — central manager for tool schema definitions and execution dispatch.
Includes: Web search, Image search, File system, Gmail, Calendar, Browser automation,
Code execution, Screen Vision inspection, Pixel Color Inspector, System Hardware monitor, Autonomous Git agent,
Proactive Task Scheduler, App Launcher, Clipboard Manager, Network Diagnostics,
System Audio controller, PDF Reader, Fast File Search, Webcam Vision, Weather, PowerToys Awake,
Automated File Organizer, Large File Finder, Security Port Scanner,
Spotify Player & Lyrics, YouTube Player & Control, Canva Design Automator, Window Opacity & Fullscreen Controller,
System Power Inspector, Clipboard Snippet Stash, Executive Daily Briefing, Remote Mobile Control,
Mobile File Retrieval, Workspace Layout Snap, Multi-Item Clipboard Vault, Process Manager & Kill Switch,
File Zipper Archive, Smart Playlist Generator, Code Refactoring & Lint Auditor, GitHub Repository Tracker,
Environment Secret Vault, Webcam Security Motion Alarm, Wi-Fi Device Intrusion Scanner,
Voice Settings, Book Summarizer, Financial Quotes, Tech News Digest, Screen Region Crop, Focus Shield,
Junk File Cleaner, Network Speedtest, Markdown Notes Vault, Email Drafts, Cloud Storage Sync,
Discord/Slack Webhooks, and Todo Task Manager.
"""

import json
import logging
from typing import Any, Callable

from tools.search import web_search, image_search
from tools.files import read_file, write_file, list_directory, send_file_to_mobile
from tools.gmail import list_unread_emails, send_email
from tools.calendar import list_calendar_events, create_calendar_event
from tools.browser import browse_url, take_screenshot
from tools.code import execute_python_code
from tools.screen import capture_desktop_screen, analyze_screen_image, get_screen_pixel_color
from tools.system import get_system_health
from tools.git_agent import git_status, git_commit_and_push
from tools.scheduler import schedule_reminder, list_scheduled_tasks
from tools.app_launcher import launch_app, open_url_in_browser
from tools.clipboard import get_clipboard_text, set_clipboard_text
from tools.network import get_network_diagnostics
from tools.audio import set_master_volume, mute_master_volume
from tools.pdf_reader import read_pdf_file
from tools.file_search import search_local_files
from tools.webcam import capture_webcam_snapshot
from tools.weather import get_weather
from tools.powertoys import toggle_awake_mode
from tools.disk_cleaner import organize_directory, find_large_files
from tools.port_scanner import get_open_ports
from tools.media import play_spotify_song, get_song_lyrics
from tools.youtube import play_youtube_video, control_youtube_player
from tools.canva import open_canva_design
from tools.window import set_window_opacity, toggle_fullscreen
from tools.power import get_power_status
from tools.clipboard_history import stash_clipboard_snippet, list_stashed_snippets
from tools.briefing import generate_morning_briefing
from tools.remote_mobile import get_mobile_remote_url, execute_remote_laptop_command
from tools.layout import setup_workspace_preset
from tools.clipboard_vault import push_to_clipboard_vault, get_clipboard_vault_history
from tools.process_manager import list_top_processes, terminate_process_by_name
from tools.archive import zip_directory
from tools.playlist import generate_smart_playlist
from tools.code_auditor import audit_code_file
from tools.github_tracker import track_github_repository
from tools.env_vault import generate_env_vault_template
from tools.webcam_alarm import check_webcam_motion_alarm
from tools.wifi_scanner import scan_wifi_devices
from tools.voice_settings import set_voice_settings
from tools.book_reader import summarize_pdf_book
from tools.finance import get_financial_quote
from tools.news import get_tech_news_digest
from tools.screen_crop import crop_screen_region
from tools.focus_mode import toggle_focus_shield
from tools.junk_cleaner import clean_junk_files
from tools.speedtest import run_network_speedtest
from tools.notes import create_markdown_note, search_markdown_notes
from tools.email_pro import create_email_draft, search_priority_emails
from tools.cloud_storage import sync_cloud_file
from tools.messaging import send_webhook_message
from tools.todo import add_todo_task, list_todo_tasks
from tools import expansion_batch, expansion_batch_2

log = logging.getLogger(__name__)

# Map of tool_name -> execution function
_TOOL_MAP: dict[str, Callable[..., dict[str, Any]]] = {
    "web_search": web_search,
    "image_search": image_search,
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
    "list_unread_emails": list_unread_emails,
    "send_email": send_email,
    "list_calendar_events": list_calendar_events,
    "create_calendar_event": create_calendar_event,
    "browse_url": browse_url,
    "take_screenshot": take_screenshot,
    "execute_python_code": execute_python_code,
    "capture_desktop_screen": capture_desktop_screen,
    "analyze_screen_image": analyze_screen_image,
    "get_screen_pixel_color": get_screen_pixel_color,
    "get_system_health": get_system_health,
    "git_status": git_status,
    "git_commit_and_push": git_commit_and_push,
    "schedule_reminder": schedule_reminder,
    "list_scheduled_tasks": list_scheduled_tasks,
    "launch_app": launch_app,
    "open_url_in_browser": open_url_in_browser,
    "get_clipboard_text": get_clipboard_text,
    "set_clipboard_text": set_clipboard_text,
    "get_network_diagnostics": get_network_diagnostics,
    "set_master_volume": set_master_volume,
    "mute_master_volume": mute_master_volume,
    "read_pdf_file": read_pdf_file,
    "search_local_files": search_local_files,
    "capture_webcam_snapshot": capture_webcam_snapshot,
    "get_weather": get_weather,
    "toggle_awake_mode": toggle_awake_mode,
    "organize_directory": organize_directory,
    "find_large_files": find_large_files,
    "get_open_ports": get_open_ports,
    "play_spotify_song": play_spotify_song,
    "get_song_lyrics": get_song_lyrics,
    "play_youtube_video": play_youtube_video,
    "control_youtube_player": control_youtube_player,
    "open_canva_design": open_canva_design,
    "set_window_opacity": set_window_opacity,
    "toggle_fullscreen": toggle_fullscreen,
    "get_power_status": get_power_status,
    "stash_clipboard_snippet": stash_clipboard_snippet,
    "list_stashed_snippets": list_stashed_snippets,
    "generate_morning_briefing": generate_morning_briefing,
    "get_mobile_remote_url": get_mobile_remote_url,
    "execute_remote_laptop_command": execute_remote_laptop_command,
    "send_file_to_mobile": send_file_to_mobile,
    "setup_workspace_preset": setup_workspace_preset,
    "push_to_clipboard_vault": push_to_clipboard_vault,
    "get_clipboard_vault_history": get_clipboard_vault_history,
    "list_top_processes": list_top_processes,
    "terminate_process_by_name": terminate_process_by_name,
    "zip_directory": zip_directory,
    "generate_smart_playlist": generate_smart_playlist,
    "audit_code_file": audit_code_file,
    "track_github_repository": track_github_repository,
    "generate_env_vault_template": generate_env_vault_template,
    "check_webcam_motion_alarm": check_webcam_motion_alarm,
    "scan_wifi_devices": scan_wifi_devices,
    "set_voice_settings": set_voice_settings,
    "summarize_pdf_book": summarize_pdf_book,
    "get_financial_quote": get_financial_quote,
    "get_tech_news_digest": get_tech_news_digest,
    "crop_screen_region": crop_screen_region,
    "toggle_focus_shield": toggle_focus_shield,
    "clean_junk_files": clean_junk_files,
    "run_network_speedtest": run_network_speedtest,
    "create_markdown_note": create_markdown_note,
    "search_markdown_notes": search_markdown_notes,
    "create_email_draft": create_email_draft,
    "search_priority_emails": search_priority_emails,
    "sync_cloud_file": sync_cloud_file,
    "send_webhook_message": send_webhook_message,
    "add_todo_task": add_todo_task,
    "list_todo_tasks": list_todo_tasks,
    # Category 1-5 Expansion Suite Tools
    "get_virtual_desktop_status": expansion_batch.get_virtual_desktop_status,
    "set_process_priority": expansion_batch.set_process_priority,
    "query_windows_registry": expansion_batch.query_windows_registry,
    "list_startup_applications": expansion_batch.list_startup_applications,
    "get_disk_smart_metrics": expansion_batch.get_disk_smart_metrics,
    "flush_ram_cache": expansion_batch.flush_ram_cache,
    "get_bluetooth_devices": expansion_batch.get_bluetooth_devices,
    "set_display_brightness": expansion_batch.set_display_brightness,
    "get_system_uptime": expansion_batch.get_system_uptime,
    "trigger_keyboard_shortcut": expansion_batch.trigger_keyboard_shortcut,
    "extract_ocr_text": expansion_batch.extract_ocr_text,
    "scan_qr_code": expansion_batch.scan_qr_code,
    "remove_image_background": expansion_batch.remove_image_background,
    "extract_color_palette": expansion_batch.extract_color_palette,
    "upscale_image_resolution": expansion_batch.upscale_image_resolution,
    "detect_faces_in_image": expansion_batch.detect_faces_in_image,
    "extract_video_frames": expansion_batch.extract_video_frames,
    "convert_text_to_audio_speech": expansion_batch.convert_text_to_audio_speech,
    "get_docker_containers": expansion_batch.get_docker_containers,
    "run_sql_query": expansion_batch.run_sql_query,
    "test_rest_api_endpoint": expansion_batch.test_rest_api_endpoint,
    "format_code_snippet": expansion_batch.format_code_snippet,
    "audit_dependencies_vulnerabilities": expansion_batch.audit_dependencies_vulnerabilities,
    "run_automated_unit_tests": expansion_batch.run_automated_unit_tests,
    "validate_json_schema": expansion_batch.validate_json_schema,
    "test_regex_pattern": expansion_batch.test_regex_pattern,
    "push_mobile_notification": expansion_batch.push_mobile_notification,
    "sync_mobile_clipboard": expansion_batch.sync_mobile_clipboard,
    "get_mobile_telemetry_status": expansion_batch.get_mobile_telemetry_status,
    "trigger_remote_camera_preview": expansion_batch.trigger_remote_camera_preview,
    "send_mobile_location_ping": expansion_batch.send_mobile_location_ping,
    "shred_file_securely": expansion_batch.shred_file_securely,
    "encrypt_file_aes256": expansion_batch.encrypt_file_aes256,
    "decrypt_file_aes256": expansion_batch.decrypt_file_aes256,
    "generate_secure_password": expansion_batch.generate_secure_password,
    "validate_ssl_certificate": expansion_batch.validate_ssl_certificate,
    "check_windows_defender_status": expansion_batch.check_windows_defender_status,
    "generate_ssh_keypair": expansion_batch.generate_ssh_keypair,
    # Category 6-10 Expansion Suite Tools
    "convert_video_format": expansion_batch_2.convert_video_format,
    "trim_audio_file": expansion_batch_2.trim_audio_file,
    "generate_presentation_outline": expansion_batch_2.generate_presentation_outline,
    "generate_meme_image": expansion_batch_2.generate_meme_image,
    "add_watermark_to_image": expansion_batch_2.add_watermark_to_image,
    "query_wikipedia_summary": expansion_batch_2.query_wikipedia_summary,
    "check_web_bookmarks": expansion_batch_2.check_web_bookmarks,
    "generate_citation_reference": expansion_batch_2.generate_citation_reference,
    "generate_mindmap_nodes": expansion_batch_2.generate_mindmap_nodes,
    "analyze_text_sentiment": expansion_batch_2.analyze_text_sentiment,
    "log_habit_streak": expansion_batch_2.log_habit_streak,
    "generate_daily_standup_report": expansion_batch_2.generate_daily_standup_report,
    "convert_timezone_time": expansion_batch_2.convert_timezone_time,
    "log_expense_item": expansion_batch_2.log_expense_item,
    "detect_calendar_conflicts": expansion_batch_2.detect_calendar_conflicts,
    "get_public_ip_info": expansion_batch_2.get_public_ip_info,
    "query_dns_whois_info": expansion_batch_2.query_dns_whois_info,
    "upload_file_to_s3": expansion_batch_2.upload_file_to_s3,
    "probe_web_server_health": expansion_batch_2.probe_web_server_health,
    "get_bandwidth_usage_metrics": expansion_batch_2.get_bandwidth_usage_metrics,
    "get_cpu_temperature_metrics": expansion_batch_2.get_cpu_temperature_metrics,
    "get_gpu_vram_metrics": expansion_batch_2.get_gpu_vram_metrics,
    "switch_power_performance_plan": expansion_batch_2.switch_power_performance_plan,
    "get_battery_health_cycles": expansion_batch_2.get_battery_health_cycles,
    "benchmark_storage_drive_speed": expansion_batch_2.benchmark_storage_drive_speed,
}

# OpenAI-compatible function tool definitions
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Searches the web for up-to-date information, news, current facts, or articles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search term or query to look up on the web."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "image_search",
            "description": "Searches for images on the web when the user asks to see an image or visual of a concept, object, or person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The visual search term or image query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a local file on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The file path to read."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Creates or overwrites a file on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The target file path to create/overwrite."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists files and folders inside a local directory on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "The directory path to list (defaults to '.')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_unread_emails",
            "description": "Lists recent unread emails from the user's Gmail inbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of unread emails to fetch (default 5)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Sends an email to a recipient address via Gmail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address."
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line."
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content."
                    }
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_calendar_events",
            "description": "Lists upcoming events from the user's primary Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of upcoming events to list (default 5)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Schedules a new appointment or event on the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Title or summary of the event."
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO 8601 format e.g. 2026-08-08T10:00:00+05:30"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO 8601 format e.g. 2026-08-08T11:00:00+05:30"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional notes or event description."
                    }
                },
                "required": ["summary", "start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browse_url",
            "description": "Navigates to a webpage using Playwright headless browser and extracts its text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The webpage URL to visit and scrape."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Captures a visual screenshot of a webpage and saves it locally.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The webpage URL to capture."
                    },
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path (default 'design/page_preview.png')."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": "Executes a Python code snippet in an isolated sandbox and returns stdout/stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code snippet to execute."
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "capture_desktop_screen",
            "description": "Captures a full screenshot of the user's primary monitor screen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path for screenshot (default 'design/screen_capture.png')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_screen_image",
            "description": "Uses Gemini Multimodal Vision to inspect and analyze an image file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "File path to the image to analyze."
                    },
                    "prompt": {
                        "type": "string",
                        "description": "What to look for or question about the visual screen content."
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_screen_pixel_color",
            "description": "Captures screen and returns the exact Hex color code and RGB values of the pixel at coordinates (x, y).",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "Horizontal X coordinate on screen."
                    },
                    "y": {
                        "type": "integer",
                        "description": "Vertical Y coordinate on screen."
                    }
                },
                "required": ["x", "y"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_health",
            "description": "Inspects real-time PC hardware metrics including CPU, RAM, Disk usage %, and top processes.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_status",
            "description": "Inspects current Git repository branch and modified/untracked files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to local Git repo (default '.')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_commit_and_push",
            "description": "Stages all changes, creates a commit with the provided message, and pushes to remote.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commit_message": {
                        "type": "string",
                        "description": "Git commit message."
                    },
                    "repo_path": {
                        "type": "string",
                        "description": "Path to local Git repo (default '.')."
                    }
                },
                "required": ["commit_message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_reminder",
            "description": "Schedules a timed proactive reminder or notification to trigger after a delay in seconds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "The reminder text or task description."
                    },
                    "delay_seconds": {
                        "type": "integer",
                        "description": "Time delay in seconds from now before triggering reminder."
                    }
                },
                "required": ["task_description", "delay_seconds"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_scheduled_tasks",
            "description": "Lists all active background reminders and scheduled tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "launch_app",
            "description": "Launches a desktop application by name (e.g. 'code', 'chrome', 'notepad', 'calculator', 'spotify').",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The application name to launch."
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_url_in_browser",
            "description": "Opens a website URL in the user's default desktop browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The website URL to open."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_clipboard_text",
            "description": "Reads text content currently stored on the user's OS clipboard.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_clipboard_text",
            "description": "Copies text content to the user's OS clipboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to copy to clipboard."
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_network_diagnostics",
            "description": "Inspects local IP address, hostname, and tests internet ping latency.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_master_volume",
            "description": "Sets the system master audio volume percentage (0 to 100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "level_percent": {
                        "type": "integer",
                        "description": "Volume percentage level (0-100)."
                    }
                },
                "required": ["level_percent"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mute_master_volume",
            "description": "Mutes or unmutes system master audio output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mute": {
                        "type": "boolean",
                        "description": "True to mute, False to unmute."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_pdf_file",
            "description": "Reads and extracts text from a local PDF document.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to local PDF file."
                    },
                    "max_pages": {
                        "type": "integer",
                        "description": "Maximum pages to read (default 10)."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_local_files",
            "description": "Recursively searches local directory for files matching a wildcard pattern (e.g. '*.py', '*.pdf').",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_pattern": {
                        "type": "string",
                        "description": "Wildcard pattern to search for (e.g. '*.pdf')."
                    },
                    "search_dir": {
                        "type": "string",
                        "description": "Starting directory (default '.')."
                    }
                },
                "required": ["query_pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "capture_webcam_snapshot",
            "description": "Captures a frame snapshot from the primary laptop webcam camera.",
            "parameters": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path (default 'design/webcam_snapshot.png')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Fetches real-time weather conditions, temperature, humidity, and wind speed for a specified city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. 'London', 'New York', 'Tokyo')."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_awake_mode",
            "description": "Prevents PC from going to sleep or turning off screen (PowerToys Awake utility).",
            "parameters": {
                "type": "object",
                "properties": {
                    "enable": {
                        "type": "boolean",
                        "description": "True to keep PC awake, False to restore normal sleep timer."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "organize_directory",
            "description": "Sorts unorganized files into categorized subfolders (Documents, Images, Code, Archives, Executables).",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "Target folder path to organize (defaults to '.')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_large_files",
            "description": "Finds large files taking up disk space.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "Search directory (default '.')."
                    },
                    "min_size_mb": {
                        "type": "integer",
                        "description": "Minimum file size in MB to flag (default 100)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_open_ports",
            "description": "Scans active listening network ports and connections on the machine.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_spotify_song",
            "description": "Searches and plays a song or playlist on Spotify.",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "Song title or artist name to play."
                    }
                },
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_song_lyrics",
            "description": "Fetches the lyrics for a song by title and artist name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_title": {
                        "type": "string",
                        "description": "Song title to look up."
                    }
                },
                "required": ["song_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_youtube_video",
            "description": "Searches YouTube for a video query and opens the video or search results directly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Video title or topic to search on YouTube."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_youtube_player",
            "description": "Controls desktop video playback (play, pause, toggle captions, fullscreen).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action type: 'play_pause', 'mute', 'fullscreen', 'toggle_captions'."
                    }
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_canva_design",
            "description": "Opens Canva design canvas pre-configured for a specified template (e.g. invitation, poster, presentation, thumbnail).",
            "parameters": {
                "type": "object",
                "properties": {
                    "design_type": {
                        "type": "string",
                        "description": "Type of design ('invitation', 'poster', 'presentation', 'logo', 'thumbnail')."
                    },
                    "topic": {
                        "type": "string",
                        "description": "Theme or topic (e.g. 'birthday party', 'hackathon')."
                    }
                },
                "required": ["design_type", "topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_window_opacity",
            "description": "Adjusts the opacity/transparency percentage of Luna's desktop window (e.g. 10%, 50%, 100%).",
            "parameters": {
                "type": "object",
                "properties": {
                    "opacity_percent": {
                        "type": "integer",
                        "description": "Opacity percentage level (10-100)."
                    }
                },
                "required": ["opacity_percent"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_fullscreen",
            "description": "Toggles fullscreen mode for Luna's window.",
            "parameters": {
                "type": "object",
                "properties": {
                    "enable": {
                        "type": "boolean",
                        "description": "True for fullscreen, False for standard sidepanel window mode."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_power_status",
            "description": "Inspects laptop battery status, power source, and estimated time remaining.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stash_clipboard_snippet",
            "description": "Saves current OS clipboard text under a custom label for future recall.",
            "parameters": {
                "type": "object",
                "properties": {
                    "label": {
                        "type": "string",
                        "description": "Name or label for the snippet."
                    }
                },
                "required": ["label"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_stashed_snippets",
            "description": "Lists all saved clipboard snippets and labels.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_morning_briefing",
            "description": "Generates a 3-point executive briefing combining Weather, System Health, Battery Power, and Git Status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City for weather report (default 'London')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_mobile_remote_url",
            "description": "Returns the local network IP address and URL to access Luna's panel from your mobile phone on Wi-Fi.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_remote_laptop_command",
            "description": "Executes a remote laptop command triggered from mobile (e.g. launch VS Code, create project folder, open terminal, play song).",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_type": {
                        "type": "string",
                        "description": "Action type ('create_project_folder', 'launch_vscode', 'open_terminal', 'play_music')."
                    },
                    "target_name": {
                        "type": "string",
                        "description": "Project folder name or song title."
                    }
                },
                "required": ["action_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_file_to_mobile",
            "description": "Locates a file on the laptop's disk and generates a 1-tap download link for mobile phone retrieval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to local file on laptop (e.g. 'design/logo_mark.png' or 'notes.pdf')."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "setup_workspace_preset",
            "description": "Launches applications and arranges workspace layout (e.g. 'coding', 'research', 'media').",
            "parameters": {
                "type": "object",
                "properties": {
                    "preset_name": {
                        "type": "string",
                        "description": "Preset type ('coding', 'research', 'media')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "push_to_clipboard_vault",
            "description": "Pushes text into the multi-item clipboard vault history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Snippet text to store."
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_clipboard_vault_history",
            "description": "Retrieves stored clipboard vault items.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_top_processes",
            "description": "Lists top background processes consuming CPU and memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max processes to list (default 10)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate_process_by_name",
            "description": "Terminates background process by executable name (e.g. 'notepad.exe', 'calculator.exe').",
            "parameters": {
                "type": "object",
                "properties": {
                    "process_name": {
                        "type": "string",
                        "description": "Process executable name to terminate."
                    }
                },
                "required": ["process_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "zip_directory",
            "description": "Compresses a directory into a .zip archive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_dir": {
                        "type": "string",
                        "description": "Directory path to compress (default '.')."
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Output archive file name (default 'archive.zip')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_smart_playlist",
            "description": "Generates and plays a music playlist tailored to your mood ('focus', 'coding', 'chill', 'workout').",
            "parameters": {
                "type": "object",
                "properties": {
                    "mood": {
                        "type": "string",
                        "description": "Mood type ('focus', 'coding', 'chill', 'workout')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_code_file",
            "description": "Audits a Python or text code file for syntax errors, line count, and structural health.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to code file to inspect."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "track_github_repository",
            "description": "Inspects GitHub repository status, active branch, and modified files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "GitHub repository owner/name (default 'Shreeprasandh/Luna')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_env_vault_template",
            "description": "Generates a secure .env.example environment secret vault template file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path (default '.env.example')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_webcam_motion_alarm",
            "description": "Captures a webcam frame snapshot to monitor room security while away.",
            "parameters": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Destination file path (default 'design/motion_alarm.png')."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scan_wifi_devices",
            "description": "Scans local Wi-Fi network ARP table to inspect connected IP addresses and MAC addresses.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_voice_settings",
            "description": "Adjusts Luna's speech synthesis parameters (rate, pitch, gender).",
            "parameters": {
                "type": "object",
                "properties": {
                    "rate": { "type": "integer" },
                    "pitch": { "type": "integer" },
                    "voice_gender": { "type": "string" }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_pdf_book",
            "description": "Reads and summarizes long PDF documents or books up to max_pages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": { "type": "string" },
                    "max_pages": { "type": "integer" }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_financial_quote",
            "description": "Fetches real-time stock or cryptocurrency market quote data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": { "type": "string" }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tech_news_digest",
            "description": "Fetches top tech news headlines from Hacker News API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": { "type": "string" }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crop_screen_region",
            "description": "Crops a specific monitor region (x, y, width, height) and saves it for visual analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": { "type": "integer" },
                    "y": { "type": "integer" },
                    "width": { "type": "integer" },
                    "height": { "type": "integer" }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "toggle_focus_shield",
            "description": "Enables or disables Pomodoro Daily Focus Shield to block online distractions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "enable": { "type": "boolean" },
                    "duration_minutes": { "type": "integer" }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clean_junk_files",
            "description": "Scans and removes temporary cache files and .tmp files to free up disk storage space.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": { "type": "string" }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_network_speedtest",
            "description": "Measures network ping latency, packet stability, and internet connection health.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_markdown_note",
            "description": "Creates or appends to a local Markdown note file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": { "type": "string" },
                    "content": { "type": "string" },
                    "folder": { "type": "string" }
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_markdown_notes",
            "description": "Searches local Markdown notes folder for a keyword query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": { "type": "string" },
                    "folder": { "type": "string" }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_email_draft",
            "description": "Creates and stores an email draft for review before sending.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": { "type": "string" },
                    "subject": { "type": "string" },
                    "body": { "type": "string" }
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_priority_emails",
            "description": "Searches recent unread inbox emails matching sender or keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sender_or_keyword": { "type": "string" }
                },
                "required": ["sender_or_keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sync_cloud_file",
            "description": "Syncs a local file to the local Cloud Drive sync folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": { "type": "string" },
                    "destination_folder": { "type": "string" }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_webhook_message",
            "description": "Sends an automated notification message to a Discord or Slack webhook URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "webhook_url": { "type": "string" },
                    "message": { "type": "string" }
                },
                "required": ["webhook_url", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_todo_task",
            "description": "Adds a checkable task item to your daily to-do list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": { "type": "string" },
                    "due_date": { "type": "string" }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_todo_tasks",
            "description": "Retrieves active to-do list tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def execute_tool(name: str, arguments: dict[str, Any] | str) -> dict[str, Any]:
    """
    Dispatches execution of a registered tool by name with arguments.
    Enforces Security & Path Traversal Validation before execution.
    """
    if name not in _TOOL_MAP:
        log.error(f"Unknown tool requested: '{name}'")
        return {"status": "error", "message": f"Unknown tool: '{name}'"}

    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except Exception as e:
            log.error(f"Failed to parse tool arguments for '{name}': {e}")
            return {"status": "error", "message": f"Invalid arguments format: {e}"}

    # Security & Path Traversal Validation Guard
    from tools.safety import validate_tool_execution
    safety_check = validate_tool_execution(name, arguments)
    if not safety_check["allowed"]:
        log.warning(f"Tool execution blocked by Safety Guard: {safety_check['reason']}")
        return {"status": "error", "message": safety_check["reason"]}

    log.info(f"Executing tool '{name}' with args: {arguments}")
    try:
        handler = _TOOL_MAP[name]
        return handler(**arguments)
    except Exception as e:
        log.error(f"Execution error in tool '{name}': {e}")
        return {"status": "error", "message": f"Tool execution failed: {str(e)}"}
