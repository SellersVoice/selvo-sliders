import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, ChevronDown, Info } from "lucide-react";

// --- UI primitives (shadcn-like minimal stubs if not present) ---
const Button = ({ className = "", children, ...props }) => (
  <button
    className={`px-4 py-2 rounded-2xl border shadow-sm hover:shadow-md transition ${className}`}
    {...props}
  >
    {children}
  </button>
);

const Seg = ({ options, value, onChange }) => (
  <div className="inline-flex rounded-2xl border p-1 bg-white shadow-sm">
    {options.map((opt) => (
      <button
        key={opt}
        onClick={() => onChange(opt)}
        className={`px-3 py-1.5 rounded-xl text-sm transition ${
          value === opt ? "bg-black text-white" : "hover:bg-gray-100"
        }`}
      >
        {opt}
      </button>
    ))}
  </div>
);

const Card = ({ children, className = "" }) => (
  <div className={`rounded-3xl border bg-white shadow-sm ${className}`}>{children}</div>
);

const Pill = ({ children, tone = "slate" }) => (
  <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-medium bg-${tone}-100 text-${tone}-800`}>{children}</span>
);

// --- Domain strings ---
const TIMELINE = ["ASAP", "Soon", "Flexible"] as const;
const INVOLVEMENT = ["Minimal", "Moderate", "High"] as const;
const CONDITION = ["Needs Work", "Average", "Move-in Ready"] as const;

type Timeline = typeof TIMELINE[number];
type Involvement = typeof INVOLVEMENT[number];
type Condition = typeof CONDITION[number];

type Tier = "Cash (1%)" | "Core (2%)" | "Classic (3%)" | "Cosmetic (4%)" | "Comprehensive (5%)";

// --- Recommendation logic (rule-based, covers all 27 combos) ---
function recommend(t: Timeline, i: Involvement, c: Condition): { primary: Tier; alt: Tier; rationale: string[] } {
  // Helper to keep rationale succinct
  const r: string[] = [];
  if (t === "ASAP") r.push("Speed prioritized");
  if (t === "Flexible") r.push("Timing flexible");
  if (i === "Minimal") r.push("Low seller involvement");
  if (i === "High") r.push("High seller involvement OK");
  if (c === "Needs Work") r.push("Home needs work");
  if (c === "Move-in Ready") r.push("Home is show-ready");

  // Decision tree
  if (t === "ASAP") {
    if (c === "Needs Work") {
      if (i === "High") return { primary: "Cosmetic (4%)", alt: "Cash (1%)", rationale: r };
      return { primary: "Cash (1%)", alt: "Core (2%)", rationale: r };
    }
    if (c === "Average") {
      if (i === "Minimal") return { primary: "Core (2%)", alt: "Classic (3%)", rationale: r };
      return { primary: "Classic (3%)", alt: "Comprehensive (5%)", rationale: r };
    }
    // Move-in Ready
    if (i === "Minimal") return { primary: "Core (2%)", alt: "Classic (3%)", rationale: r };
    if (i === "Moderate") return { primary: "Classic (3%)", alt: "Core (2%)", rationale: r };
    return { primary: "Classic (3%)", alt: "Comprehensive (5%)", rationale: r };
  }

  if (t === "Soon") {
    if (c === "Needs Work") {
      if (i === "High") return { primary: "Cosmetic (4%)", alt: "Core (2%)", rationale: r };
      if (i === "Moderate") return { primary: "Core (2%)", alt: "Cash (1%)", rationale: r };
      return { primary: "Cash (1%)", alt: "Core (2%)", rationale: r };
    }
    if (c === "Average") {
      if (i === "Minimal") return { primary: "Core (2%)", alt: "Classic (3%)", rationale: r };
      if (i === "Moderate") return { primary: "Classic (3%)", alt: "Core (2%)", rationale: r };
      return { primary: "Comprehensive (5%)", alt: "Classic (3%)", rationale: r };
    }
    // Move-in Ready
    if (i === "Minimal") return { primary: "Core (2%)", alt: "Classic (3%)", rationale: r };
    if (i === "Moderate") return { primary: "Classic (3%)", alt: "Comprehensive (5%)", rationale: r };
    return { primary: "Comprehensive (5%)", alt: "Classic (3%)", rationale: r };
  }

  // Flexible
  if (c === "Needs Work") {
    if (i === "High") return { primary: "Comprehensive (5%)", alt: "Cosmetic (4%)", rationale: r };
    if (i === "Moderate") return { primary: "Cosmetic (4%)", alt: "Core (2%)", rationale: r };
    return { primary: "Core (2%)", alt: "Cash (1%)", rationale: r };
  }
  if (c === "Average") {
    if (i === "Minimal") return { primary: "Core (2%)", alt: "Classic (3%)", rationale: r };
    if (i === "Moderate") return { primary: "Classic (3%)", alt: "Comprehensive (5%)", rationale: r };
    return { primary: "Comprehensive (5%)", alt: "Classic (3%)", rationale: r };
  }
  // Move-in Ready
  if (i === "Minimal") return { primary: "Core (2%)", alt: "Classic (3%)", rationale: r };
  if (i === "Moderate") return { primary: "Classic (3%)", alt: "Core (2%)", rationale: r };
  return { primary: "Comprehensive (5%)", alt: "Classic (3%)", rationale: r };
}

// Tier blurbs (concise, for tooltips)
const TIER_BLURB: Record<Tier, string> = {
  "Cash (1%)": "Fast, off-MLS investor network. Lower prep, lower typical net.",
  "Core (2%)": "MLS syndication + essentials. Solid exposure, minimal hassle.",
  "Classic (3%)": "Showcase prep + upgraded media + tracked ads.",
  "Cosmetic (4%)": "Advisor-coordinated polish, light updates, and staging.",
  "Comprehensive (5%)": "Strategic, ROI-driven renovations with full support.",
};

export default function SelvoSlidersApp() {
  const [timeline, setTimeline] = useState<Timeline>("ASAP");
  const [involvement, setInvolvement] = useState<Involvement>("Minimal");
  const [condition, setCondition] = useState<Condition>("Needs Work");

  const rec = useMemo(() => recommend(timeline, involvement, condition), [timeline, involvement, condition]);

  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-gray-50 to-white flex items-start justify-center p-6">
      <div className="w-full max-w-5xl grid grid-cols-1 gap-6">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">Selvo Sliders</h1>
            <p className="text-sm text-gray-600 mt-1">Right Fee. Right Strategy. Right Results.</p>
          </div>
          <Pill tone="slate">Beta</Pill>
        </header>

        <Card className="p-6">
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-gray-500">Timeline</p>
              <Seg options={[...TIMELINE]} value={timeline} onChange={setTimeline} />
              <p className="mt-2 text-xs text-gray-500">How quickly do you want to close?</p>
            </div>
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-gray-500">Involvement</p>
              <Seg options={[...INVOLVEMENT]} value={involvement} onChange={setInvolvement} />
              <p className="mt-2 text-xs text-gray-500">How hands-on can you be?</p>
            </div>
            <div>
              <p className="mb-2 text-xs uppercase tracking-wide text-gray-500">Condition</p>
              <Seg options={[...CONDITION]} value={condition} onChange={setCondition} />
              <p className="mt-2 text-xs text-gray-500">Which best describes your home?</p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-start gap-4">
            <CheckCircle2 className="mt-1 h-5 w-5 text-emerald-600" />
            <div className="flex-1">
              <p className="text-sm text-gray-500">Recommended Primary Tier</p>
              <motion.h2
                key={rec.primary}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25 }}
                className="text-xl md:text-2xl font-semibold mt-1"
              >
                {rec.primary}
              </motion.h2>
              <p className="mt-2 text-sm text-gray-600">{TIER_BLURB[rec.primary]}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {rec.rationale.map((x, idx) => (
                  <Pill key={idx}>{x}</Pill>
                ))}
              </div>
            </div>
            <div className="w-px bg-gray-200 mx-2" />
            <div className="w-72 max-w-full">
              <p className="text-xs uppercase tracking-wide text-gray-500">Alternative</p>
              <div className="mt-1 text-sm font-medium">{rec.alt}</div>
              <p className="mt-1 text-xs text-gray-600">{TIER_BLURB[rec.alt]}</p>
            </div>
          </div>
        </Card>

        <Card className="p-5">
          <details className="group">
            <summary className="flex items-center gap-2 cursor-pointer">
              <ChevronDown className="h-4 w-4 transition group-open:rotate-180" />
              <span className="text-sm font-medium">How we choose tiers</span>
            </summary>
            <div className="mt-3 text-sm text-gray-600 leading-relaxed">
              <p>
                The rules balance <strong>timeline</strong> (speed), <strong>involvement</strong> (how hands-on you can be), and
                <strong> condition</strong> (prep required). Faster timelines or heavier prep lean toward Cash/Core/Cosmetic;
                flexible timelines with higher involvement and upgrade potential lean toward Comprehensive. Classic bridges
                mid-cases with showcase prep + upgraded media.
              </p>
            </div>
          </details>
        </Card>

        <footer className="pb-8 text-center text-xs text-gray-500">
          © Selvo — Home of the Five‑Fee Fit
        </footer>
      </div>
    </div>
  );
}
