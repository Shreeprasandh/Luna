"use client";

import React, { useState } from "react";
import { Lock, ShieldCheck, KeyRound } from "lucide-react";
import { LogoMark } from "./LogoMark";

interface LockScreenProps {
  onUnlock: (pin: string) => void;
}

export const LockScreen: React.FC<LockScreenProps> = ({ onUnlock }) => {
  const [pin, setPin] = useState("");
  const [error, setError] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (pin === "777777") {
      onUnlock(pin);
    } else {
      setError(true);
      setPin("");
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center p-6 bg-[#0F1012] text-[#E0E2EC]">
      <div className="w-full max-w-xs space-y-6 text-center border border-[#2B2D33] p-6 rounded-2xl bg-[#16171B] shadow-2xl">
        <div className="flex justify-center">
          <LogoMark size={42} />
        </div>

        <div className="space-y-1">
          <h2 className="text-lg font-semibold tracking-tight text-[#F0F2FA] flex items-center justify-center gap-2">
            <Lock className="w-4 h-4 text-[#C9B59C]" />
            Luna Security Lock
          </h2>
          <p className="text-xs text-[#9093A0]">
            Hacker Protection Enabled. Enter Master PIN to unlock mobile control.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <KeyRound className="absolute left-3 top-3 w-4 h-4 text-[#9093A0]" />
            <input
              type="password"
              maxLength={6}
              value={pin}
              onChange={(e) => {
                setError(false);
                setPin(e.target.value);
              }}
              placeholder="Enter 6-Digit PIN"
              aria-label="Master Access PIN"
              className="w-full pl-9 pr-4 py-2.5 rounded-lg bg-[#0F1012] border border-[#2B2D33] text-center font-mono text-base text-[#F0F2FA] focus:outline-none focus:border-[#C9B59C] transition-colors"
            />
          </div>

          {error && (
            <p className="text-xs text-rose-400 animate-bounce">
              Access Denied: Invalid Master PIN.
            </p>
          )}

          <button
            type="submit"
            className="w-full py-2.5 rounded-lg bg-[#C9B59C] text-[#0F1012] font-semibold text-sm hover:opacity-90 active:scale-98 transition-all flex items-center justify-center gap-2"
          >
            <ShieldCheck className="w-4 h-4" />
            Authenticate Access
          </button>
        </form>
      </div>
    </div>
  );
};
