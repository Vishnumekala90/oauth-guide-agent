import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-white focus:p-2">Skip to content</a>
      <header className="border-b border-paper-line bg-paper-card">
        <div className="mx-auto max-w-5xl px-4 h-14 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 font-semibold">
            <span aria-hidden="true" className="inline-block h-5 w-5 rounded bg-brand" />
            OAuth Setup Guide
          </Link>
          <span className="text-xs text-ink-faint hidden sm:block">Evidence-labelled setup paths for provider OAuth apps</span>
        </div>
      </header>
      <main id="main" className="flex-1 mx-auto w-full max-w-5xl px-4 py-8">
        <Outlet />
      </main>
      <footer className="border-t border-paper-line py-6 text-center text-xs text-ink-faint">
        Guides are research aids, not provider policy. Always confirm against the linked official pages.
      </footer>
    </div>
  );
}
