import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Checklist from "../components/Checklist";
import { StatusChip } from "../components/Chips";
import type { Step } from "../types";

describe("StatusChip", () => {
  it.each([["verified", "Verified"], ["unverified", "Not verified"], ["estimate", "Estimate"]] as const)("renders %s", (s, label) => {
    render(<StatusChip status={s} />);
    expect(screen.getByTestId("status-chip")).toHaveTextContent(label);
  });
});

const steps: Step[] = [
  { id: "step-1", title: "Create app", detail: "d", actor: "developer", status: "verified", source_ids: ["S1"] },
  { id: "step-2", title: "Exchange code", detail: "d", actor: "agent", status: "unverified", source_ids: [] },
];

describe("Checklist", () => {
  afterEach(() => vi.restoreAllMocks());

  it("toggles optimistically and PATCHes the API with the client id", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ checked: { "step-1": true } }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<Checklist guideId="github" steps={steps} initial={{}} />);
    await userEvent.click(screen.getByLabelText(/Create app/));
    expect(screen.getByTestId("progress-text")).toHaveTextContent("1 of 2 done");
    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("/api/guides/github/progress");
    expect(init.method).toBe("PATCH");
    expect(JSON.parse(init.body)).toEqual({ checked: { "step-1": true } });
    expect(init.headers["X-Client-Id"]).toMatch(/^[A-Za-z0-9_-]{8,64}$/);
  });

  it("rolls back and shows an error when saving fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ error: { code: "not_found", message: "Guide not found." } }), { status: 404 })));
    render(<Checklist guideId="github" steps={steps} initial={{}} />);
    await userEvent.click(screen.getByLabelText(/Create app/));
    expect(await screen.findByRole("alert")).toHaveTextContent(/Could not save progress/);
    expect(screen.getByTestId("progress-text")).toHaveTextContent("0 of 2 done");
  });

  it("restores saved progress", () => {
    render(<Checklist guideId="github" steps={steps} initial={{ "step-2": true }} />);
    expect(screen.getByLabelText(/Exchange code/)).toBeChecked();
    expect(screen.getByTestId("progress-text")).toHaveTextContent("1 of 2 done");
  });
});
