/** Pure helpers: validation, error mapping, client id, safe URLs. */

export function validateQuery(raw: string): string | null {
  const q = raw.trim();
  if (q.length < 2) return "Enter an app name or website (at least 2 characters).";
  if (q.length > 200) return "That is too long. Use 200 characters or fewer.";
  // eslint-disable-next-line no-control-regex
  if (/[\u0000-\u001f]/.test(q)) return "Control characters are not allowed.";
  return null;
}

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

const FRIENDLY: Record<string, string> = {
  llm_not_configured:
    "Live generation is not set up on this server: it needs a GEMINI_API_KEY. The six curated guides still work.",
  search_not_configured:
    "Live generation is not set up on this server: it needs a web-search API key (see SEARCH_PROVIDER in the README). The six curated guides still work.",
  unsafe_url: "That URL points somewhere we will not fetch (private, local or non-standard address). Use the provider's public website.",
  rate_limited: "Too many requests. Wait a minute and try again.",
  timeout: "Research took too long and was stopped. Try again, or paste the provider's developer-docs URL.",
};

export function friendlyError(err: unknown): string {
  if (err instanceof ApiError) {
    if (FRIENDLY[err.code]) return FRIENDLY[err.code];
    if (err.status === 404) return "We could not find that. The link may be wrong.";
    if (err.status >= 500) return err.message || "The server hit an error. Please try again.";
    return err.message || "Request failed.";
  }
  if (err instanceof TypeError) return "Could not reach the server. Check that the backend is running.";
  return "Something went wrong. Please try again.";
}

export function safeHref(url: string): string | null {
  try {
    const u = new URL(url);
    return u.protocol === "http:" || u.protocol === "https:" ? u.toString() : null;
  } catch {
    return null;
  }
}

const CLIENT_KEY = "oauth-guide-client-id";
export function getClientId(): string {
  try {
    let id = localStorage.getItem(CLIENT_KEY);
    if (!id || !/^[A-Za-z0-9_-]{8,64}$/.test(id)) {
      const bytes = new Uint8Array(16);
      crypto.getRandomValues(bytes);
      id = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
      localStorage.setItem(CLIENT_KEY, id);
    }
    return id;
  } catch {
    return "anonymous-session";
  }
}
