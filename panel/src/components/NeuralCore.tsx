"use client";

import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";

export type CognitiveState = "idle" | "listening" | "thinking" | "speaking" | "tool_execution";

interface NeuralCoreProps {
  state?: CognitiveState;
  audioLevel?: number; // 0.0 to 1.0
  className?: string;
  size?: number;
  interactive?: boolean;
}

const vertexShader = `
  uniform float uTime;
  uniform float uAudio;
  uniform float uState; // 0: idle, 1: listening, 2: thinking, 3: speaking, 4: tool_execution
  uniform vec2 uPointer;

  attribute vec3 aRandom;
  attribute float aSize;

  varying vec3 vPosition;
  varying float vAudioIntensity;
  varying float vState;
  varying float vDist;

  // Simplex-inspired pseudo 3D noise
  float hash(vec3 p) {
    p = fract(p * 0.3183099 + 0.1);
    p *= 17.0;
    return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
  }

  float noise(vec3 x) {
    vec3 i = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    return mix(
      mix(mix(hash(i + vec3(0,0,0)), hash(i + vec3(1,0,0)), f.x),
          mix(hash(i + vec3(0,1,0)), hash(i + vec3(1,1,0)), f.x), f.y),
      mix(mix(hash(i + vec3(0,0,1)), hash(i + vec3(1,0,1)), f.x),
          mix(hash(i + vec3(0,1,1)), hash(i + vec3(1,1,1)), f.x), f.y), f.z
    );
  }

  void main() {
    vPosition = position;
    vState = uState;

    // Base speed and frequency modulated by cognitive state
    float speed = 0.6;
    float displacementAmp = 0.12;

    if (uState > 0.5 && uState < 1.5) { // LISTENING
      speed = 1.4;
      displacementAmp = 0.25 + uAudio * 0.45;
    } else if (uState >= 1.5 && uState < 2.5) { // THINKING (Intense rapid vortex)
      speed = 3.2;
      displacementAmp = 0.35;
    } else if (uState >= 2.5 && uState < 3.5) { // SPEAKING (Harmonic pulse)
      speed = 2.0;
      displacementAmp = 0.28 + sin(uTime * 4.0) * 0.12;
    } else if (uState >= 3.5) { // TOOL EXECUTION
      speed = 2.5;
      displacementAmp = 0.30;
    }

    // Dynamic orbital displacement
    vec3 norm = normalize(position);
    float n = noise(norm * 3.0 + uTime * speed);
    
    // Pointer influence (subtle tilt toward cursor)
    vec3 tilt = vec3(uPointer.x * 0.15, uPointer.y * 0.15, 0.0);

    // Harmonic respiratory pulse
    float breath = sin(uTime * 1.5 + aRandom.x * 6.28) * 0.06;
    
    // Audio kick
    float audioDisplacement = uAudio * (0.2 + aRandom.y * 0.3);
    vAudioIntensity = uAudio + n * 0.3;

    vec3 newPosition = position + norm * (breath + n * displacementAmp + audioDisplacement) + tilt;
    vDist = length(newPosition);

    vec4 mvPosition = modelViewMatrix * vec4(newPosition, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    // Perspective point sizing with smooth audio enlargement
    float pSize = aSize * (1.0 + vAudioIntensity * 1.6);
    gl_PointSize = max(1.5, pSize * (220.0 / -mvPosition.z));
  }
`;

const fragmentShader = `
  uniform float uState;
  uniform float uTime;

  varying vec3 vPosition;
  varying float vAudioIntensity;
  varying float vState;
  varying float vDist;

  void main() {
    // Render soft circular anti-aliased points
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    if (dist > 0.5) discard;

    // Smooth edge alpha falloff
    float alpha = smoothstep(0.5, 0.08, dist);

    // Color Palettes based on cognitive state
    // IDLE: Luminous Obsidian Cyan / Ice Blue
    vec3 cIdleA = vec3(0.08, 0.42, 0.75);
    vec3 cIdleB = vec3(0.24, 0.78, 0.95);

    // LISTENING: Warm Lunar Amber / Solar Gold
    vec3 cListenA = vec3(0.92, 0.58, 0.10);
    vec3 cListenB = vec3(0.98, 0.82, 0.32);

    // THINKING: High-Dimensional Amethyst / Cosmic Violet
    vec3 cThinkA = vec3(0.52, 0.22, 0.92);
    vec3 cThinkB = vec3(0.82, 0.48, 0.98);

    // SPEAKING: Luminous Electric White / Opal Pearl
    vec3 cSpeakA = vec3(0.92, 0.95, 1.00);
    vec3 cSpeakB = vec3(0.68, 0.84, 0.98);

    // TOOL EXECUTION: Surgical Emerald / Quantum Teal
    vec3 cToolA = vec3(0.05, 0.72, 0.48);
    vec3 cToolB = vec3(0.32, 0.94, 0.72);

    vec3 finalColor = mix(cIdleA, cIdleB, vAudioIntensity);

    if (uState > 0.5 && uState < 1.5) {
      finalColor = mix(cListenA, cListenB, vAudioIntensity * 1.2);
    } else if (uState >= 1.5 && uState < 2.5) {
      float pulse = sin(uTime * 6.0) * 0.5 + 0.5;
      finalColor = mix(cThinkA, cThinkB, pulse + vAudioIntensity * 0.5);
    } else if (uState >= 2.5 && uState < 3.5) {
      finalColor = mix(cSpeakA, cSpeakB, vAudioIntensity);
    } else if (uState >= 3.5) {
      finalColor = mix(cToolA, cToolB, vAudioIntensity * 1.4);
    }

    // Core glow enhancement
    float coreGlow = smoothstep(0.25, 0.0, dist) * 0.4;
    finalColor += vec3(coreGlow);

    gl_FragColor = vec4(finalColor, alpha * 0.88);
  }
`;

export const NeuralCore: React.FC<NeuralCoreProps> = ({
  state = "idle",
  audioLevel = 0,
  className = "",
  size = 320,
  interactive = true,
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const uniformsRef = useRef<{
    uTime: THREE.IUniform<number>;
    uAudio: THREE.IUniform<number>;
    uState: THREE.IUniform<number>;
    uPointer: THREE.IUniform<THREE.Vector2>;
  }>({
    uTime: { value: 0 },
    uAudio: { value: 0 },
    uState: { value: 0 },
    uPointer: { value: new THREE.Vector2(0, 0) },
  });

  const stateToCode = (st: CognitiveState): number => {
    switch (st) {
      case "idle":
        return 0;
      case "listening":
        return 1;
      case "thinking":
        return 2;
      case "speaking":
        return 3;
      case "tool_execution":
        return 4;
      default:
        return 0;
    }
  };

  useEffect(() => {
    uniformsRef.current.uState.value = stateToCode(state);
  }, [state]);

  useEffect(() => {
    uniformsRef.current.uAudio.value = audioLevel;
  }, [audioLevel]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.z = 4.2;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: "high-performance",
    });
    renderer.setSize(size, size);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    container.innerHTML = "";
    container.appendChild(renderer.domElement);

    // 2. Geometry: 15,000 spherical points using Fibonacci / Archimedes distribution
    const particleCount = 14000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const randomness = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);

    const goldenRatio = (1 + Math.sqrt(5)) / 2;

    for (let i = 0; i < particleCount; i++) {
      const theta = (2 * Math.PI * i) / goldenRatio;
      const phi = Math.acos(1 - (2 * (i + 0.5)) / particleCount);
      const r = 1.35 + (Math.random() - 0.5) * 0.15;

      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);

      randomness[i * 3] = Math.random();
      randomness[i * 3 + 1] = Math.random();
      randomness[i * 3 + 2] = Math.random();

      sizes[i] = Math.random() * 2.2 + 1.2;
    }

    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute("aRandom", new THREE.BufferAttribute(randomness, 3));
    geometry.setAttribute("aSize", new THREE.BufferAttribute(sizes, 1));

    // 3. Shader Material with Additive Blending
    const material = new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms: uniformsRef.current,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // 4. Subtle Orbital Inner Core (Subtle glowing core density)
    const coreGeo = new THREE.SphereGeometry(0.75, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x051329,
      transparent: true,
      opacity: 0.35,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    scene.add(coreMesh);

    // 5. Pointer tracking
    const handlePointerMove = (e: MouseEvent) => {
      if (!interactive) return;
      const rect = container.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const y = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
      uniformsRef.current.uPointer.value.set(x, y);
    };

    if (interactive) {
      window.addEventListener("mousemove", handlePointerMove);
    }

    // 6. 60 FPS Render Loop using High-Precision Performance Timestamp
    const startTime = performance.now();
    let animationFrameId: number;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      const elapsedTime = (performance.now() - startTime) * 0.001;
      uniformsRef.current.uTime.value = elapsedTime;

      // Base gentle rotation
      particles.rotation.y = elapsedTime * 0.08;
      particles.rotation.x = Math.sin(elapsedTime * 0.05) * 0.1;

      renderer.render(scene, camera);
    };

    animate();

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      if (interactive) {
        window.removeEventListener("mousemove", handlePointerMove);
      }
      geometry.dispose();
      material.dispose();
      coreGeo.dispose();
      coreMat.dispose();
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [size, interactive]);

  return (
    <div
      className={`relative flex items-center justify-center select-none overflow-hidden ${className}`}
      style={{ width: size, height: size }}
    >
      <div ref={mountRef} className="w-full h-full" />
      {/* Subtle outer focal ring */}
      <div className="absolute inset-2 rounded-full border border-white/[0.04] pointer-events-none" />
      <div className="absolute inset-8 rounded-full border border-white/[0.02] pointer-events-none" />
    </div>
  );
};
