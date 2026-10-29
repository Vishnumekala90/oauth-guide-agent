import { ApiError, friendlyError, getClientId, safeHref, validateQuery } from "../lib";

describe("validateQuery", () => {
  it("accepts names and urls", () => {
    expect(validateQuery("Linear")).toBeNull();
    expect(validateQuery("  https://asana.com ")).toBeNull();
  });
  it("rejects short, long and control characters", () => {
    expect(validateQuery("a")).toMatch(/at least 2/);
    expect(validateQuery("   ")).toMatch(/at least 2/);
    expect(validateQuery("x".repeat(201))).toMatch(/too long/);
    expect(validateQuery("ab\u0001c")).toMatch(/Control/);
  });
});

describe("friendlyError", () => {
  it("explains missing configuration", () => {
    expect(friendlyError(new ApiError(503, "llm_not_configured", "raw"))).toMatch(/GEMINI_API_KEY/);
    expect(friendlyError(new ApiError(503, "search_not_configured", "raw"))).toMatch(/search/i);
  });
  it("maps unsafe url, 404 and network failures", () => {
    expect(friendlyError(new ApiError(422, "unsafe_url", "x"))).toMatch(/will not fetch/);
    expect(friendlyError(new ApiError(404, "not_found", "x"))).toMatch(/could not find/);
    expect(friendlyError(new TypeError("fetch failed"))).toMatch(/backend is running/);
  });
  it("passes through server messages for validation errors", () => {
    expect(friendlyError(new ApiError(422, "invalid_input", "Enter an app name."))).toBe("Enter an app name.");
  });
});

describe("safeHref / client id", () => {
  it("only allows http(s)", () => {
    expect(safeHref("https://a.com/x")).toBe("https://a.com/x");
    expect(safeHref("javascript:alert(1)")).toBeNull();
    expect(safeHref("not a url")).toBeNull();
  });
  it("generates a valid persistent client id", () => {
    const a = getClientId();
    expect(a).toMatch(/^[A-Za-z0-9_-]{8,64}$/);
    expect(getClientId()).toBe(a);
  });
});
