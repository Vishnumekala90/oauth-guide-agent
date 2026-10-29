export type ClaimStatus = "verified" | "estimate" | "unverified";
export type Difficulty = "easy" | "moderate" | "hard";
export type Actor = "agent" | "developer" | "both";
export type Confidence = "high" | "medium" | "low";
export type WaitStatus = "documented" | "estimate" | "unknown" | "none_documented";

export interface Source {
  id: string; title: string; url: string; verified_on: string;
  discovered_via: string; fetched: boolean; official: boolean; confidence: Confidence; note?: string | null;
}
export interface Fact { text: string; status: ClaimStatus; source_ids: string[]; quote?: string | null }
export interface Step { id: string; title: string; detail: string; actor: Actor; status: ClaimStatus; source_ids: string[]; quote?: string | null }
export interface Blocker { title: string; detail: string; resolution?: string | null; status: ClaimStatus; source_ids: string[]; quote?: string | null }
export interface ApprovalWait {
  short_label: string; summary: string; status: WaitStatus;
  min_days?: number | null; max_days?: number | null; source_ids: string[]; quote?: string | null;
}
export interface Effort { short_label: string; min_hours: number; max_hours: number; rationale: string }
export interface Guide {
  id: string; slug: string; provider_name: string; tagline: string; category: string; website?: string | null;
  generated_by: "seed" | "agent"; verified_on: string; overall_confidence: Confidence;
  difficulty: Difficulty; difficulty_explanation: string; effort: Effort; approval_wait: ApprovalWait;
  prerequisites: Fact[]; steps: Step[]; callback_requirements: Fact[]; scopes: Fact[]; testing: Fact[]; publishing: Fact[];
  blockers: Blocker[]; agent_can_do: string[]; developer_must_do: string[]; sources: Source[];
  unknowns: string[]; review_notes: string[];
}
export interface GuideSummary {
  id: string; slug: string; provider_name: string; tagline: string; category: string;
  generated_by: "seed" | "agent"; difficulty: Difficulty; effort_label: string; approval_label: string;
  approval_status: WaitStatus; overall_confidence: Confidence; verified_on: string;
}
export interface ProgressState { checked: Record<string, boolean>; updated_at?: string | null }
export interface GuideDetail { guide: Guide; progress: ProgressState }
export interface JobEvent { ts: string; stage: string; message: string; level: "info" | "warn" | "error" }
export interface Job {
  id: string; guide_id: string; query: string; status: "queued" | "running" | "done" | "error";
  events: JobEvent[]; error?: string | null; error_code?: string | null; created_at: string; updated_at: string;
}
export interface GenerateResponse { job_id?: string | null; guide_id: string; status: string; existing: boolean; share_path: string }
