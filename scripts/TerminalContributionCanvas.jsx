import React, { useEffect, useRef, useState, useCallback } from "react";
// Import pre-fetched github data (or pass as prop)
import githubData from "../data/github.json";

/**
 * Terminal Contribution Canvas Component
 *
 * Implements Avi Vashishta's animated terminal graph:
 * - Scrambles random ASCII characters and settles into . : + # @
 * - Pure function draw(ctx, w, h, t)
 * - IntersectionObserver (triggers at 40% visibility)
 * - requestAnimationFrame running only when visible
 * - devicePixelRatio (capped at 2)
 * - Accessible: prefers-reduced-motion renders settled state immediately
 * - Replay button to restart animation
 */

const GLYPHS = [".", ":", "+", "#", "@"];
const SCRAMBLE_CHARS = ".:+#@/\\|=-_~*&%$0123456789";

// GitHub colors matching prompt spec
const COLORS = {
  bg: "#ffffff",
  textPrompt: "#24292f",
  command: "#216e39",
  stats: "#216e39",
  levels: [
    "#ebedf0", // 0: empty
    "#9be9a8", // 1
    "#40c463", // 2
    "#30a14e", // 3
    "#216e39", // 4
  ],
};

// Pure animation draw function
function drawTerminal(ctx, width, height, t, data) {
  ctx.clearRect(0, 0, width, height);

  const username = data?.username || "ashmit";
  const levels = data?.levels || "";
  const total = data?.total || 0;
  const streak = data?.streak || 0;
  const bestDay = data?.bestDay || 0;

  // Responsive sizing calculations
  const cols = 53;
  const rows = 7;
  const paddingX = Math.max(16, width * 0.04);
  const availableW = width - paddingX * 2;
  const colSpacing = Math.min(16, availableW / cols);
  const rowSpacing = colSpacing * 1.15;
  const fontSize = Math.max(9, Math.min(13, colSpacing * 0.85));

  ctx.save();

  // 1. Terminal Command Prompt Typing Animation (0 to 1200ms)
  const fullCommand = `${username}@github ~ $ ./contributions.sh`;
  const typeDuration = 1200;
  const typeProgress = Math.min(1, t / typeDuration);
  const charsToShow = Math.floor(typeProgress * fullCommand.length);
  const currentText = fullCommand.slice(0, charsToShow);

  ctx.font = `600 ${fontSize + 1}px JetBrains Mono, "Courier New", monospace`;
  ctx.fillStyle = COLORS.textPrompt;
  ctx.fillText(currentText, paddingX, 36);

  // Blinking cursor
  if (t < typeDuration || Math.floor(t / 500) % 2 === 0) {
    const textMetric = ctx.measureText(currentText);
    ctx.fillStyle = COLORS.command;
    ctx.fillRect(paddingX + textMetric.width + 3, 23, 7, fontSize + 3);
  }

  // 2. ASCII Glyphs Scramble & Settle Animation
  // Begins at 1200ms, column by column reveal
  const gridStartY = 68;
  const gridStartTime = 1200;
  const timePerCol = 35; // ms per column wave

  ctx.font = `600 ${fontSize}px JetBrains Mono, "Courier New", monospace`;
  ctx.textAlign = "center";

  for (let c = 0; c < cols; c++) {
    const colX = paddingX + c * colSpacing + colSpacing / 2;
    const colStart = gridStartTime + c * timePerCol;
    const colAge = t - colStart;

    for (let r = 0; r < rows; r++) {
      const dayIndex = c * rows + r;
      if (dayIndex >= levels.length) continue;

      const targetLevel = parseInt(levels[dayIndex], 10) || 0;
      const targetGlyph = GLYPHS[targetLevel];
      const targetColor = COLORS.levels[targetLevel];
      const dayY = gridStartY + r * rowSpacing;

      if (colAge < 0) {
        // Not reached yet
        continue;
      } else if (colAge < 350 && t !== Infinity) {
        // Scrambling phase
        const randomGlyph = SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
        ctx.fillStyle = COLORS.levels[Math.floor(Math.random() * COLORS.levels.length)];
        ctx.fillText(randomGlyph, colX, dayY);
      } else {
        // Settled into correct level and glyph
        ctx.fillStyle = targetColor;
        ctx.fillText(targetGlyph, colX, dayY);
      }
    }
  }

  // 3. Bottom Stats Summary Bar (appears after grid finishes)
  const totalGridTime = gridStartTime + cols * timePerCol + 300;
  if (t > totalGridTime || t === Infinity) {
    const statsFade = t === Infinity ? 1 : Math.min(1, (t - totalGridTime) / 400);
    ctx.globalAlpha = statsFade;
    ctx.textAlign = "left";
    ctx.font = `500 ${Math.max(10, fontSize)}px JetBrains Mono, "Courier New", monospace`;
    ctx.fillStyle = COLORS.stats;
    const statsText = `${total.toLocaleString()} contributions   ·   ${streak} day streak   ·   best day ${bestDay}`;
    ctx.fillText(statsText, paddingX, gridStartY + rows * rowSpacing + 28);
  }

  ctx.restore();
}

export default function TerminalContributionCanvas({ data = githubData }) {
  const containerRef = useRef(null);
  const canvasRef = useRef(null);
  const startTimeRef = useRef(null);
  const animFrameIdRef = useRef(null);
  const isVisibleRef = useRef(false);
  const [isPlaying, setIsPlaying] = useState(false);

  const startAnimation = useCallback(() => {
    startTimeRef.current = performance.now();
    setIsPlaying(true);
  }, []);

  const replay = () => {
    startAnimation();
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext("2d");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Handle high DPI scaling (capped at 2)
    const handleResize = () => {
      const rect = container.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = rect.width * dpr;
      canvas.height = 240 * dpr;
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `240px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      if (prefersReducedMotion) {
        drawTerminal(ctx, rect.width, 240, Infinity, data);
      }
    };

    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(container);
    handleResize();

    // Render loop
    const render = (now) => {
      if (!isVisibleRef.current) return;

      const rect = container.getBoundingClientRect();
      const elapsed = prefersReducedMotion ? Infinity : (now - (startTimeRef.current || now));

      drawTerminal(ctx, rect.width, 240, elapsed, data);

      if (!prefersReducedMotion && elapsed < 4500) {
        animFrameIdRef.current = requestAnimationFrame(render);
      } else {
        setIsPlaying(false);
      }
    };

    // IntersectionObserver (40% in view)
    const observer = new IntersectionObserver(
      ([entry]) => {
        isVisibleRef.current = entry.isIntersecting;
        if (entry.isIntersecting) {
          startAnimation();
          animFrameIdRef.current = requestAnimationFrame(render);
        } else {
          if (animFrameIdRef.current) {
            cancelAnimationFrame(animFrameIdRef.current);
          }
        }
      },
      { threshold: 0.4 }
    );

    observer.observe(container);

    return () => {
      observer.disconnect();
      resizeObserver.disconnect();
      if (animFrameIdRef.current) cancelAnimationFrame(animFrameIdRef.current);
    };
  }, [data, startAnimation]);

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        width: "100%",
        maxWidth: "920px",
        margin: "0 auto",
        background: "#ffffff",
        borderRadius: "8px",
        border: "1px solid #e1e4e8",
        padding: "12px 0 8px 0",
        fontFamily: 'JetBrains Mono, "Courier New", monospace',
        overflow: "hidden",
      }}
    >
      <canvas ref={canvasRef} style={{ display: "block" }} />

      {/* Small Replay Button */}
      <button
        onClick={replay}
        aria-label="Replay contribution terminal animation"
        style={{
          position: "absolute",
          bottom: "12px",
          right: "16px",
          background: "transparent",
          border: "1px solid #d0d7de",
          borderRadius: "4px",
          padding: "4px 8px",
          fontSize: "11px",
          color: "#57606a",
          cursor: "pointer",
          fontFamily: "inherit",
          transition: "all 0.2s ease",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = "#216e39";
          e.currentTarget.style.color = "#216e39";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = "#d0d7de";
          e.currentTarget.style.color = "#57606a";
        }}
      >
        ↻ REPLAY
      </button>
    </div>
  );
}

