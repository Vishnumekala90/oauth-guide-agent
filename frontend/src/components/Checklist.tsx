import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import { friendlyError } from "../lib";
import type { Step } from "../types";
import { ActorBadge, Citations, Quote, StatusChip } from "./Chips";

export default function Checklist({ guideId, steps, initial }: { guideId: string; steps: Step[]; initial: Record<string, boolean> }) {
  const [checked, setChecked] = useState<Record<string, boolean>>(initial);
  const [error, setError] = useState<string | null>(null);
  const first = useRef(true);
  useEffect(() => { if (first.current) { first.current = false; return; } setChecked(initial); }, [initial]);

  const done = steps.filter((s) => checked[s.id]).length;

  async function toggle(id: string) {
    const next = !checked[id];
    const prev = checked;
    setChecked({ ...checked, [id]: next });
    setError(null);
    try {
      const res = await api.patchProgress(guideId, { [id]: next });
      setChecked(res.checked);
    } catch (e) {
      setChecked(prev);
      setError(`Could not save progress: ${friendlyError(e)}`);
    }
  }

  return (
    <section className="mt-8" aria-labelledby="h-steps">
      <div className="flex items-end justify-between gap-4">
        <h2 id="h-steps" className="text-lg font-semibold">Setup steps</h2>
        <p className="text-sm text-ink-soft" data-testid="progress-text">{done} of {steps.length} done</p>
      </div>
      <div className="mt-2 h-2 rounded bg-paper-line" role="progressbar" aria-valuemin={0} aria-valuemax={steps.length} aria-valuenow={done} aria-label="Checklist progress">
        <div className="h-2 rounded bg-brand" style={{ width: steps.length ? `${(done / steps.length) * 100}%` : "0%" }} />
      </div>
      {error && <p role="alert" className="mt-2 text-sm text-rose-ink">{error}</p>}
      <ol className="mt-4 space-y-3">
        {steps.map((s, i) => (
          <li key={s.id} className="rounded-md border border-paper-line bg-paper-card p-3">
            <div className="flex gap-3">
              <input id={`chk-${s.id}`} type="checkbox" className="mt-1 h-5 w-5 accent-brand shrink-0"
                     checked={!!checked[s.id]} onChange={() => toggle(s.id)} />
              <div className="flex-1 min-w-0">
                <label htmlFor={`chk-${s.id}`} className={`font-medium cursor-pointer ${checked[s.id] ? "line-through text-ink-faint" : ""}`}>
                  <span className="font-mono text-ink-faint mr-1">{i + 1}.</span>{s.title}
                </label>
                <div className="mt-1 flex flex-wrap gap-1.5"><ActorBadge actor={s.actor} /><StatusChip status={s.status} /></div>
                <p className="mt-2 text-sm text-ink-soft">{s.detail}<Citations ids={s.source_ids} /></p>
                <Quote quote={s.quote} />
              </div>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
