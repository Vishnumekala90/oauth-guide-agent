import type { Fact } from "../types";
import { Citations, Quote, StatusChip } from "./Chips";

export default function FactList({ title, facts, empty }: { title: string; facts: Fact[]; empty?: string }) {
  return (
    <section className="mt-8" aria-labelledby={`h-${title}`}>
      <h2 id={`h-${title}`} className="text-lg font-semibold">{title}</h2>
      {facts.length === 0 ? (
        <p className="mt-2 text-sm text-ink-faint">{empty ?? "Nothing found in the sources read. See “Unknown” below."}</p>
      ) : (
        <ul className="mt-3 space-y-3">
          {facts.map((f, i) => (
            <li key={i} className="rounded-md border border-paper-line bg-paper-card p-3">
              <div className="flex flex-wrap items-start gap-2">
                <StatusChip status={f.status} />
                <p className="text-sm flex-1 min-w-[12rem]">{f.text}<Citations ids={f.source_ids} /></p>
              </div>
              <Quote quote={f.quote} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
