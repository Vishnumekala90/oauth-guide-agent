import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { api } from "../api";
import Timeline from "../components/Timeline";
import { friendlyError } from "../lib";
import type { Job } from "../types";

export default function GeneratingPage() {
  const { jobId = "" } = useParams();
  const nav = useNavigate();
  const loc = useLocation();
  const [job, setJob] = useState<Job | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let stop = false;
    let timer: ReturnType<typeof setTimeout>;
    async function tick() {
      try {
        const j = await api.getJob(jobId);
        if (stop) return;
        setJob(j);
        if (j.status === "done") { setTimeout(() => !stop && nav(`/guides/${j.guide_id}`, { replace: true }), 700); return; }
        if (j.status === "error") return;
      } catch (e) {
        if (stop) return;
        setErr(friendlyError(e));
        return;
      }
      timer = setTimeout(tick, 1200);
    }
    tick();
    return () => { stop = true; clearTimeout(timer); };
  }, [jobId, nav]);

  const running = !!job && (job.status === "queued" || job.status === "running");
  const failed = job?.status === "error" || !!err;
  const query = job?.query ?? (loc.state as any)?.query;

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-semibold">Researching{query ? ` ${query}` : ""}…</h1>
      <p className="mt-2 text-sm text-ink-soft">The agent searches for official docs, reads the pages, then checks every quote against what it fetched. Nothing is shown as verified unless the quote was found.</p>
      <div className="mt-6 rounded-lg border border-paper-line bg-paper-card p-4">
        {!job && !err && <p className="text-sm text-ink-faint" aria-live="polite">Starting…</p>}
        {job && <Timeline events={job.events} running={running} />}
        {job?.status === "done" && <p className="mt-3 text-sm font-medium text-brand-dark">Guide ready. Opening it…</p>}
      </div>
      {failed && (
        <div role="alert" className="mt-4 rounded-md bg-rose-tint p-4 text-sm text-rose-ink">
          <p className="font-medium">The guide could not be generated.</p>
          <p className="mt-1">{err ?? job?.error ?? "Unknown error."}</p>
          <Link to="/" className="mt-3 inline-block rounded-md bg-brand px-4 py-2 text-white">Try again</Link>
        </div>
      )}
    </div>
  );
}
