/**
 * Luna Voice Synthesis Engine
 * Native Web Speech API integration with Apple Silicon voice heuristics
 * and live audio intensity simulation for 3D Neural Core reactivity.
 */

class LunaSpeechEngine {
  private activeUtterance: SpeechSynthesisUtterance | null = null;
  private animFrameId: number | null = null;
  private isMuted: boolean = false;
  private selectedVoice: SpeechSynthesisVoice | null = null;

  constructor() {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      // Warm up voices
      window.speechSynthesis.onvoiceschanged = () => {
        this.selectBestVoice();
      };
      this.selectBestVoice();
    }
  }

  private selectBestVoice(): SpeechSynthesisVoice | null {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return null;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return null;

    // Prefer high-quality natural Apple voices on macOS
    const preferredNames = ["Samantha", "Karen", "Victoria", "Tara", "Tessa", "Moira", "Serena", "Natural", "Google UK English Female"];
    for (const name of preferredNames) {
      const found = voices.find(v => v.lang.startsWith("en") && v.name.toLowerCase().includes(name.toLowerCase()));
      if (found) {
        this.selectedVoice = found;
        return found;
      }
    }

    // Fallback to any English voice
    const fallback = voices.find(v => v.lang.startsWith("en")) || voices[0];
    this.selectedVoice = fallback || null;
    return this.selectedVoice;
  }

  public setMuted(muted: boolean) {
    this.isMuted = muted;
    if (muted) {
      this.stop();
    }
  }

  public getIsMuted(): boolean {
    return this.isMuted;
  }

  public cleanTextForSpeech(text: string): string {
    return text
      .replace(/```[\s\S]*?```/g, "Code omitted.") // Remove code blocks
      .replace(/`([^`]+)`/g, "$1")                  // Remove inline backticks
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")      // Strip markdown links
      .replace(/[#*~_>|]/g, " ")                    // Strip formatting marks
      .replace(/\s+/g, " ")                         // Normalize whitespace
      .trim();
  }

  public speak(
    rawText: string,
    callbacks?: {
      onStart?: () => void;
      onEnd?: () => void;
      onAudioPulse?: (intensity: number) => void;
    }
  ): void {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    if (this.isMuted) return;

    this.stop();

    const clean = this.cleanTextForSpeech(rawText);
    if (!clean) return;

    const utterance = new SpeechSynthesisUtterance(clean);
    const voice = this.selectedVoice || this.selectBestVoice();
    if (voice) {
      utterance.voice = voice;
    }

    utterance.rate = 1.05; // Grounded, efficient cadence
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    this.activeUtterance = utterance;

    // Pulse generator for 3D Neural Core
    let startTime = performance.now();
    const runPulse = () => {
      const elapsed = (performance.now() - startTime) / 1000;
      // Multi-frequency harmonic envelope simulating vocal formant energy
      const base = 0.45;
      const wave1 = Math.sin(elapsed * 18) * 0.25;
      const wave2 = Math.sin(elapsed * 32) * 0.15;
      const pulse = Math.min(Math.max(base + wave1 + wave2, 0.1), 0.95);

      if (callbacks?.onAudioPulse) {
        callbacks.onAudioPulse(pulse);
      }
      this.animFrameId = requestAnimationFrame(runPulse);
    };

    utterance.onstart = () => {
      if (callbacks?.onStart) callbacks.onStart();
      startTime = performance.now();
      runPulse();
    };

    const cleanup = () => {
      if (this.animFrameId !== null) {
        cancelAnimationFrame(this.animFrameId);
        this.animFrameId = null;
      }
      if (callbacks?.onAudioPulse) callbacks.onAudioPulse(0);
      if (callbacks?.onEnd) callbacks.onEnd();
      this.activeUtterance = null;
    };

    utterance.onend = cleanup;
    utterance.onerror = (e) => {
      console.warn("[Luna Speech] Synthesis ended with error:", e);
      cleanup();
    };

    window.speechSynthesis.speak(utterance);
  }

  public stop(): void {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    if (this.animFrameId !== null) {
      cancelAnimationFrame(this.animFrameId);
      this.animFrameId = null;
    }
    this.activeUtterance = null;
  }
}

export const lunaSpeech = new LunaSpeechEngine();
