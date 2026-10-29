import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import GeneratingPage from "./pages/GeneratingPage";
import GuidePage from "./pages/GuidePage";
import Home from "./pages/Home";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/guides/:id" element={<GuidePage />} />
          <Route path="/generating/:jobId" element={<GeneratingPage />} />
          <Route path="*" element={<p className="text-ink-soft">Page not found.</p>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
