"use client";

import React, { useState, useEffect } from "react";
import { Header, ThemeOption } from "@/components/Header";
import { ChatArea, Message } from "@/components/ChatArea";
import { InputBar } from "@/components/InputBar";
import { MobileQuickBar } from "@/components/MobileQuickBar";
import { LockScreen } from "@/components/LockScreen";

const BACKEND_URL = "http://localhost:8000";

export default function Home() {
  const [theme, setTheme] = useState<ThemeOption>("dark");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if PIN was previously saved in localStorage
  useEffect(() => {
    const savedAuth = localStorage.getItem("luna_authenticated");
    if (savedAuth === "true") {
      setIsAuthenticated(true);
    }
  }, []);

  // Apply theme data attribute to document root
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  // Initialise session & health check
  useEffect(() => {
    if (!isAuthenticated) return;

    const initSession = async () => {
      try {
        const healthRes = await fetch(`${BACKEND_URL}/health`);
        if (healthRes.ok) {
          setIsBackendConnected(true);
        }

        const sessionRes = await fetch(`${BACKEND_URL}/session/start`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (sessionRes.ok) {
          const data = await sessionRes.json();
          setSessionId(data.session_id);

          // Add initial greeting message
          setMessages([
            {
              id: "init",
              role: "assistant",
              text: "Luna online, Sir. How may I assist you today?",
              timestamp: new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              }),
            },
          ]);
        }
      } catch (err) {
        console.warn("Backend not reachable yet:", err);
        setIsBackendConnected(false);
        setMessages([
          {
            id: "offline",
            role: "assistant",
            text: "Backend server offline. Please start backend: uvicorn main:app --port 8000",
            timestamp: new Date().toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            }),
          },
        ]);
      }
    };

    initSession();
  }, [isAuthenticated]);

  // Handle PIN authentication unlock
  const handleUnlock = (pin: string) => {
    localStorage.setItem("luna_authenticated", "true");
    setIsAuthenticated(true);
  };

  // Handle sending user message to backend
  const handleSendMessage = async (text: string) => {
    if (!sessionId) return;

    const timeStr = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    const userMsg: Message = {
      id: String(Date.now()),
      role: "user",
      text,
      timestamp: timeStr,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, text }),
      });

      if (res.ok) {
        const payload = await res.json();
        const assistantMsg: Message = {
          id: String(Date.now() + 1),
          role: "assistant",
          text: payload.text || "",
          type: payload.type || "text",
          images: payload.images || undefined,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } else {
        throw new Error(`Server returned ${res.status}`);
      }
    } catch (err) {
      console.error("Failed to send message:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 2),
          role: "assistant",
          text: "Sir, I encountered an issue communicating with the backend API.",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceToggle = () => {
    setIsListening((prev) => !prev);
  };

  if (!isAuthenticated) {
    return <LockScreen onUnlock={handleUnlock} />;
  }

  return (
    <main className="flex flex-col h-screen w-full max-w-[440px] mx-auto border-x border-[var(--border)] bg-[var(--bg)] shadow-2xl overflow-hidden">
      <Header
        currentTheme={theme}
        onThemeChange={setTheme}
        isBackendConnected={isBackendConnected}
      />

      <ChatArea messages={messages} isLoading={isLoading} />

      <MobileQuickBar onQuickAction={handleSendMessage} />

      <InputBar
        onSendMessage={handleSendMessage}
        onVoiceToggle={handleVoiceToggle}
        isListening={isListening}
        disabled={isLoading || !sessionId}
      />
    </main>
  );
}
