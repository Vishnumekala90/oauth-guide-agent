import type { Actor, ClaimStatus, Confidence, Difficulty, WaitStatus } from "../types";

const base = "inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[11px] font-medium leading-4 whitespace-nowrap";

export function StatusChip({ status }: { status: ClaimStatus }) {
  const map = {
    verified: { cls: "bg-brand-tint text-brand-dark", label: "Verified", icon: "✓" },
    estimate: { cls: "bg-amber-tint text-amber-ink", label: "Estimate", icon: "≈" },
    unverified: { cls: "bg-rose-tint text-rose-ink", label: "Not verified", icon: "?" },
  }[status];
  return (
    <span className={`${base} ${map.cls}`} data-testid="status-chip">
      <span aria-hidden="true">{map.icon}</span>
      {map.label}
    </span>
  );
}

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  const cls = {
    easy: "bg-brand-tint text-brand-dark",
    moderate: "bg-amber-tint text-amber-ink",
    hard: "bg-rose-tint text-rose-ink",
  }[difficulty];
  return <span className={`${base} ${cls} uppercase tracking-wide`}>{difficulty}</span>;
}

export function ConfidenceBadge({ confidence }: { confidence: Confidence }) {
  return (
    <span className={`${base} border border-paper-line text-ink-soft`}>
      Confidence: {confidence}
    </span>
  );
}

export function SourceTag({ generatedBy }: { generatedBy: "seed" | "agent" }) {
  return (
    <span className={`${base} ${generatedBy === "seed" ? "bg-ink text-white" : "bg-white border border-ink text-ink"}`}>
      {generatedBy === "seed" ? "Curated" : "Agent-generated"}
    </span>
  );
}

export function ActorBadge({ actor }: { actor: Actor }) {
  const map = {
    agent: { label: "Agent can do", cls: "bg-ink text-white" },
    developer: { label: "You", cls: "bg-white border border-ink text-ink" },
    both: { label: "Agent + you", cls: "bg-paper border border-ink-faint text-ink" },
  }[actor];
  return <span className={`${base} ${map.cls}`}>{map.label}</span>;
}

export function waitStatusText(s: WaitStatus): string {
  return {
    documented: "Stated in the docs",
    estimate: "Our estimate",
    unknown: "Not stated: unknown",
    none_documented: "No review described in the docs",
  }[s];
}

export function Citations({ ids }: { ids: string[] }) {
  if (!ids.length) return null;
  return (
    <span className="inline-flex gap-1 ml-1">
      {ids.map((id) => (
        <a key={id} href={`#source-${id}`}
           className="font-mono text-[11px] rounded border border-paper-line px-1 text-brand hover:bg-brand-tint"
           aria-label={`Source ${id}`}>
          {id}
        </a>
      ))}
    </span>
  );
}

export function Quote({ quote }: { quote?: string | null }) {
  if (!quote) return null;
  return (
    <details className="mt-1 text-xs text-ink-soft">
      <summary className="cursor-pointer select-none">Evidence quote</summary>
      <blockquote className="mt-1 border-l-2 border-brand pl-2 italic">“{quote}”</blockquote>
    </details>
  );
}
