/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"IBM Plex Sans"', "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "monospace"],
      },
      colors: {
        ink: { DEFAULT: "#16202a", soft: "#4a5764", faint: "#6b7886" },
        paper: { DEFAULT: "#f6f4ef", card: "#ffffff", line: "#dcd8cd" },
        brand: { DEFAULT: "#0f5c4d", dark: "#0a4136", tint: "#e3efe9" },
        amber: { tint: "#fbf0d6", ink: "#7a5200" },
        rose: { tint: "#fbe6e2", ink: "#9a2c1d" },
      },
    },
  },
  plugins: [],
};
