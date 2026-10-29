import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import Checklist from "../components/Checklist";
import { ConfidenceBadge, DifficultyBadge, SourceTag, Citations, Quote, StatusChip, waitStatusText } from "../components/Chips";
import FactList from "../components/FactList";
import { friendlyError, safeHref } from "../lib";
import type { GuideDetail } from "../types";

async function copyText(text: string): Promise<boolean> {
  try { await navigator.clipboard.writeText(text); return true; } catch { /* fall through */ }
  try {
    const ta = document.createElement("textarea");
    ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  } catch { return false; }
}

function Tile({ label, value, sub, note }: { label: string; value: string; sub: string; note?: string }) {
  return (
    <div className="rounded-lg border border-paper-line bg-paper-card p-4">
      <p className="text-xs uppercase tracking-wide text-ink-faint">{label}</p>
      <p className="mt-1 text-xl font-semibold">{value}</p>
      <p className="mt-1 text-xs font-medium text-ink-soft">{sub}</p>
      {note && <p className="mt-2 text-sm text-ink-soft">{note}</p>}
    </div>
  );
}

export default function GuidePage() {
  const { id = "" } = useParams();
  const [data, setData] = useState<GuideDetail | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [copied, setCopied] = useState<"" | "ok" | "fail">("");

  useEffect(() => {
    setData(null); setErr(null);
    api.getGuide(id).then(setData).catch((e) => setErr(friendlyError(e)));
  }, [id]);

  if (err) return (
    <div role="alert" className="rounded-md bg-rose-tint p-4 text-rose-ink">
      <p>{err}</p><Link className="underline" to="/">Back to the library</Link>
    </div>
  );
  if (!data) return <p className="text-ink-faint" aria-busy="true">Loading guide…</p>;

  const { guide: g, progress } = data;
  const shareUrl = `${window.location.origin}/guides/${g.id}`;
  const w = g.approval_wait;
  const waitSub = waitStatusText(w.status);

  async function copy() { setCopied((await copyText(shareUrl)) ? "ok" : "fail"); setTimeout(() => setCopied(""), 2500); }

  return (
    <article>
      <Link to="/" className="text-sm text-brand hover:underline">← All guides</Link>
      <header className="mt-3">
        <div className="flex flex-wrap items-center gap-2">
          <h1 className="text-3xl font-semibold tracking-tight">{g.provider_name}</h1>
          <DifficultyBadge difficulty={g.difficulty} /><SourceTag generatedBy={g.generated_by} /><ConfidenceBadge confidence={g.overall_confidence} />
        </div>
        <p className="mt-2 text-ink-soft">{g.tagline}</p>
        <p className="mt-1 text-xs text-ink-faint">Checked {g.verified_on}{g.website && safeHref(g.website) ? <> · <a className="underline" rel="noopener noreferrer" target="_blank" href={safeHref(g.website)!}>{g.website}</a></> : null}</p>
        <div className="mt-4 flex flex-wrap items-center gap-2 rounded-md border border-paper-line bg-paper-card p-2">
          <label htmlFor="share" className="sr-only">Shareable link</label>
          <input id="share" readOnly value={shareUrl} onFocus={(e) => e.currentTarget.select()} className="flex-1 min-w-[12rem] bg-transparent px-2 py-1 font-mono text-xs" />
          <button onClick={copy} className="rounded bg-ink px-3 py-1.5 text-xs font-medium text-white hover:bg-black">Copy link</button>
          <span role="status" className="text-xs text-ink-soft">{copied === "ok" ? "Copied" : copied === "fail" ? "Copy failed: select the link and copy manually" : ""}</span>
        </div>
      </header>

      <section className="mt-6 rounded-lg border border-paper-line bg-paper-card p-4">
        <h2 className="font-semibold">How hard is it? <span className="uppercase text-sm text-ink-soft">{g.difficulty}</span></h2>
        <p className="mt-1 text-sm text-ink-soft">{g.difficulty_explanation}</p>
      </section>

      <section className="mt-4 grid gap-4 sm:grid-cols-2" aria-label="Time and effort">
        <Tile label="Your hands-on effort" value={g.effort.short_label} sub="Our estimate, not provider data" note={g.effort.rationale} />
        <Tile label="Approval wait (separate from effort)" value={w.short_label} sub={waitSub} note={w.summary} />
      </section>
      {w.source_ids.length > 0 && <p className="mt-1 text-xs text-ink-faint">Wait source: <Citations ids={w.source_ids} /></p>}
      <Quote quote={w.quote} />

      <FactList title="Prerequisites" facts={g.prerequisites} />
      <Checklist guideId={g.id} steps={g.steps} initial={progress.checked} />
      <FactList title="Callback URL requirements" facts={g.callback_requirements} />
      <FactList title="Scopes and permissions" facts={g.scopes} />
      <FactList title="Testing" facts={g.testing} />
      <FactList title="Publishing and verification" facts={g.publishing} />

      <section className="mt-8" aria-labelledby="h-blockers">
        <h2 id="h-blockers" className="text-lg font-semibold">Common blockers and troubleshooting</h2>
        {g.blockers.length === 0 ? <p className="mt-2 text-sm text-ink-faint">No blockers found in the sources read.</p> : (
          <ul className="mt-3 space-y-3">
            {g.blockers.map((b, i) => (
              <li key={i} className="rounded-md border border-paper-line bg-paper-card p-3">
                <div className="flex flex-wrap items-center gap-2"><StatusChip status={b.status} /><h3 className="font-medium">{b.title}</h3></div>
                <p className="mt-1 text-sm text-ink-soft">{b.detail}<Citations ids={b.source_ids} /></p>
                {b.resolution && <p className="mt-1 text-sm"><span className="font-medium">What to do: </span>{b.resolution}</p>}
                <Quote quote={b.quote} />
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="mt-8" aria-labelledby="h-split">
        <h2 id="h-split" className="text-lg font-semibold">What the agent can do vs what you must do</h2>
        <div className="mt-3 grid gap-4 md:grid-cols-2">
          <div className="rounded-md border border-ink bg-paper-card p-4"><h3 className="text-sm font-semibold">An agent can</h3>
            <ul className="mt-2 list-disc pl-5 space-y-1 text-sm">{g.agent_can_do.map((t, i) => <li key={i}>{t}</li>)}</ul></div>
          <div className="rounded-md border border-paper-line bg-paper-card p-4"><h3 className="text-sm font-semibold">You must</h3>
            <ul className="mt-2 list-disc pl-5 space-y-1 text-sm">{g.developer_must_do.map((t, i) => <li key={i}>{t}</li>)}</ul></div>
        </div>
      </section>

      <section className="mt-8 rounded-lg border border-amber-ink/30 bg-amber-tint p-4" aria-labelledby="h-unk">
        <h2 id="h-unk" className="text-lg font-semibold text-amber-ink">Unknown / not verified</h2>
        {g.unknowns.length === 0 ? <p className="mt-2 text-sm">No open unknowns were recorded. Still check the sources.</p> :
          <ul className="mt-2 list-disc pl-5 space-y-1 text-sm">{g.unknowns.map((u, i) => <li key={i}>{u}</li>)}</ul>}
      </section>

      <section className="mt-8" aria-labelledby="h-src">
        <h2 id="h-src" className="text-lg font-semibold">Sources</h2>
        <div className="mt-3 overflow-x-auto rounded-md border border-paper-line bg-paper-card">
          <table className="w-full text-left text-sm">
            <thead className="bg-paper text-xs uppercase text-ink-faint">
              <tr><th className="p-2">ID</th><th className="p-2">Page</th><th className="p-2">Checked</th><th className="p-2">Confidence</th><th className="p-2">Official</th><th className="p-2">Read</th></tr>
            </thead>
            <tbody>
              {g.sources.map((s) => {
                const href = safeHref(s.url);
                return (
                  <tr key={s.id} id={`source-${s.id}`} className="border-t border-paper-line align-top target:bg-brand-tint">
                    <td className="p-2 font-mono text-xs">{s.id}</td>
                    <td className="p-2 min-w-[14rem]">
                      {href ? <a href={href} target="_blank" rel="noopener noreferrer" className="text-brand underline">{s.title}</a> : s.title}
                      <div className="break-all text-[11px] text-ink-faint">{s.url}</div>
                      {s.note && <div className="text-xs text-amber-ink">{s.note}</div>}
                    </td>
                    <td className="p-2 whitespace-nowrap">{s.verified_on}</td>
                    <td className="p-2">{s.confidence}</td>
                    <td className="p-2">{s.official ? "Yes" : "No"}</td>
                    <td className="p-2">{s.fetched ? "Yes" : "Not read"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {g.review_notes.length > 0 && (
        <section className="mt-8 text-sm text-ink-soft" aria-labelledby="h-rn">
          <h2 id="h-rn" className="text-lg font-semibold text-ink">How this guide was checked</h2>
          <ul className="mt-2 list-disc pl-5 space-y-1">{g.review_notes.map((n, i) => <li key={i}>{n}</li>)}</ul>
        </section>
      )}
    </article>
  );
}
