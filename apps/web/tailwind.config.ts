import type { Config } from "tailwindcss";

// SKLOS design tokens — "operational field notebook", not generic SaaS.
// Base: soft paper. Ink: near-black warm charcoal. Accent: kaizen gold.
// Secondary: growth teal (project health). Signal: brick (blockers).
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F7F5EF",
        ink: {
          DEFAULT: "#1C2321",
          soft: "#3C4542",
          faint: "#7A8480",
        },
        line: "#DED8C8",
        kaizen: {
          DEFAULT: "#B8860B",
          soft: "#E8D9AD",
        },
        growth: {
          DEFAULT: "#2E5F5B",
          soft: "#D9E6E4",
        },
        signal: {
          DEFAULT: "#A73B2E",
          soft: "#F1DAD5",
        },
      },
      fontFamily: {
        display: ["var(--font-space-grotesk)", "system-ui", "sans-serif"],
        body: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        card: "6px",
      },
    },
  },
  plugins: [],
};

export default config;
