import { ApiError, getClientId } from "./lib";
import type { GenerateResponse, GuideDetail, GuideSummary, Job, ProgressState } from "./types";

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: { "Content-Type": "application/json", "X-Client-Id": getClientId(), ...(init.headers ?? {}) },
  });
  let body: any = null;
  try { body = await res.json(); } catch { /* non-JSON */ }
  if (!res.ok) {
    const e = body?.error;
    throw new ApiError(res.status, e?.code ?? "error", e?.message ?? `Request failed (${res.status}).`);
  }
  return body as T;
}

export const api = {
  health: () => request<any>("/api/health"),
  listGuides: () => request<GuideSummary[]>("/api/guides"),
  getGuide: (id: string) => request<GuideDetail>(`/api/guides/${encodeURIComponent(id)}`),
  generate: (query: string, force = false) =>
    request<GenerateResponse>("/api/guides/generate", { method: "POST", body: JSON.stringify({ query, force }) }),
  getJob: (id: string) => request<Job>(`/api/jobs/${encodeURIComponent(id)}`),
  patchProgress: (id: string, checked: Record<string, boolean>) =>
    request<ProgressState>(`/api/guides/${encodeURIComponent(id)}/progress`, { method: "PATCH", body: JSON.stringify({ checked }) }),
};
