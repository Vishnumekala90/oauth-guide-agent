import { FormEvent, useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { ConfidenceBadge, DifficultyBadge, SourceTag } from "../components/Chips";
import { friendlyError, validateQuery } from "../lib";
import type { GuideSummary } from "../types";

export default function Home() {
  const nav = useNavigate();
  const [query, setQuery] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [guides, setGuides] = useState<GuideSummary[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [filter, setFilter] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [source, setSource] = useState("");

  useEffect(() => {
    api.listGuides().then(setGuides).catch((e) => setLoadError(friendlyError(e)));
  }, []);

  async function submit(e: FormEvent) {
    e.preventDefault();
    const v = validateQuery(query);
    if (v) { setFormError(v); return; }
    setFormError(null);
    setBusy(true);
    try {
      const res = await api.generate(query.trim());
      if (res.existing || !res.job_id) nav(`/guides/${res.guide_id}`);
      else nav(`/generating/${res.job_id}`, { state: { query: query.trim() } });
    } catch (err) {
      setFormError(friendlyError(err));
    } finally {
      setBusy(false);
    }
  }

  const shown = useMemo(() => {
    const f = filter.trim().toLowerCase();
    return (guides ?? []).filter((g) =>
      (!f || [g.provider_name, g.tagline, g.category].some((t) => t.toLowerCase().includes(f))) &&
      (!difficulty || g.difficulty === difficulty) &&
      (!source || g.generated_by === source));
  }, [guides, filter, difficulty, source]);

  const field = "rounded-md border border-paper-line bg-white px-3 py-2 text-sm";

  return (
    <div>
      <section className="max-w-2xl">
        <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">OAuth Setup Guide</h1>
        <p className="mt-3 text-ink-soft">
          Before your agent’s users can connect an app, you may need to register an OAuth app with the provider and get it approved.
          Look up an app to see how hard that is, how long it takes, what could block you, and which parts an agent can do.
          Every claim is labelled verified, estimated or unknown.
        </p>
        <form onSubmit={submit} className="mt-6" noValidate>
          <label htmlFor="q" className="block text-sm font-medium">App name or website</label>
          <div className="mt-1 flex flex-col sm:flex-row gap-2">
            <input id="q" value={query} onChange={(e) => setQuery(e.target.value)} maxLength={200}
                   placeholder="e.g. Linear, or https://asana.com"
                   aria-invalid={!!formError} aria-describedby={formError ? "q-err" : undefined}
                   className={`${field} flex-1 py-2.5`} />
            <button type="submit" disabled={busy}
                    className="rounded-md bg-brand px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-dark disabled:opacity-60">
              {busy ? "Starting…" : "Generate guide"}
            </button>
          </div>
          {formError && <p id="q-err" role="alert" className="mt-2 text-sm text-rose-ink">{formError}</p>}
          <p className="mt-2 text-xs text-ink-faint">Curated apps open instantly. Anything else is researched live from official docs (takes about a minute).</p>
        </form>
      </section>

      <section className="mt-12" aria-labelledby="lib">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
          <h2 id="lib" className="text-xl font-semibold">Guide library</h2>
          <div className="flex flex-wrap gap-2">
            <label className="sr-only" htmlFor="f">Filter guides</label>
            <input id="f" type="search" value={filter} onChange={(e) => setFilter(e.target.value)} placeholder="Filter by name" className={field} />
            <label className="sr-only" htmlFor="d">Difficulty</label>
            <select id="d" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} className={field}>
              <option value="">Any difficulty</option><option value="easy">Easy</option><option value="moderate">Moderate</option><option value="hard">Hard</option>
            </select>
            <label className="sr-only" htmlFor="s">Origin</label>
            <select id="s" value={source} onChange={(e) => setSource(e.target.value)} className={field}>
              <option value="">Curated + generated</option><option value="seed">Curated</option><option value="agent">Agent-generated</option>
            </select>
          </div>
        </div>

        {loadError && <p role="alert" className="mt-4 rounded-md bg-rose-tint p-3 text-sm text-rose-ink">{loadError}</p>}
        {!guides && !loadError && <p className="mt-4 text-sm text-ink-faint" aria-busy="true">Loading guides…</p>}
        {guides && shown.length === 0 && <p className="mt-4 text-sm text-ink-faint">No guides match. Try clearing filters, or generate one above.</p>}

        <ul className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {shown.map((g) => (
            <li key={g.id}>
              <Link to={`/guides/${g.id}`} className="block h-full rounded-lg border border-paper-line bg-paper-card p-4 hover:border-brand">
                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-semibold">{g.provider_name}</h3>
                  <DifficultyBadge difficulty={g.difficulty} />
                </div>
                <p className="mt-1 text-sm text-ink-soft">{g.tagline}</p>
                <dl className="mt-3 space-y-1.5 text-xs">
                  <div><dt className="inline text-ink-faint">Your effort: </dt><dd className="inline">{g.effort_label}</dd></div>
                  <div className="rounded bg-paper px-2 py-1"><dt className="inline text-ink-faint">Approval wait: </dt><dd className="inline font-medium">{g.approval_label}</dd></div>
                </dl>
                <div className="mt-3 flex flex-wrap gap-1.5"><SourceTag generatedBy={g.generated_by} /><ConfidenceBadge confidence={g.overall_confidence} /></div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
