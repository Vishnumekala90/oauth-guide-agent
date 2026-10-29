import type { JobEvent } from "../types";

const ICON: Record<string, string> = { search: "⌕", fetch: "↓", extract: "✎", verify: "✓", done: "●", error: "!" };

export default function Timeline({ events, running }: { events: JobEvent[]; running: boolean }) {
  return (
    <ol className="space-y-2" aria-live="polite" aria-label="Research progress">
      {events.map((e, i) => {
        const tone = e.level === "error" ? "text-rose-ink bg-rose-tint" : e.level === "warn" ? "text-amber-ink bg-amber-tint" : "text-brand-dark bg-brand-tint";
        return (
          <li key={i} className="flex gap-3 items-start">
            <span className={`mt-0.5 h-6 w-6 shrink-0 rounded-full text-center text-xs leading-6 font-mono ${tone}`} aria-hidden="true">
              {ICON[e.stage] ?? "·"}
            </span>
            <div>
              <p className="text-sm">{e.message}</p>
              <p className="text-[11px] text-ink-faint">
                {e.stage}{e.level !== "info" ? ` · ${e.level}` : ""}
              </p>
            </div>
          </li>
        );
      })}
      {running && <li className="text-sm text-ink-faint pl-9">Working…</li>}
    </ol>
  );
}
