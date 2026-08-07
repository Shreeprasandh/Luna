"use client";

import React from "react";

interface LogoMarkProps {
  size?: number;
  className?: string;
}

export const LogoMark: React.FC<LogoMarkProps> = ({ size = 28, className = "" }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Central Solid Square */}
      <rect x="32" y="32" width="36" height="36" fill="var(--surface-alt)" stroke="var(--border-strong)" strokeWidth="2" />

      {/* Left Path Bracket with Amber Node at top-left and bottom-left */}
      <path
        d="M 45 18 L 18 18 L 18 82 L 45 82"
        stroke="var(--text-secondary)"
        strokeWidth="5"
        strokeLinecap="square"
      />
      {/* Top Left Circular Node */}
      <circle cx="45" cy="18" r="7" fill="var(--accent)" stroke="var(--bg)" strokeWidth="2" />
      {/* Bottom Left Circular Node */}
      <circle cx="45" cy="82" r="7" fill="var(--accent)" stroke="var(--bg)" strokeWidth="2" />

      {/* Right Path Bracket with Directional Triangle pointing Left */}
      <path
        d="M 58 82 L 82 82 L 82 18 L 68 18"
        stroke="var(--text-secondary)"
        strokeWidth="5"
        strokeLinecap="square"
      />
      {/* Directional Triangle pointing Left */}
      <polygon points="68,10 52,18 68,26" fill="var(--text-primary)" />
    </svg>
  );
};
