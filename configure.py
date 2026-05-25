CONFIGURE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preload" href="/static/MonaSansVF.woff2" as="font" type="font/woff2" crossorigin>
<title>AniList Catalogs — Configure</title>
<style nonce="__CSP_NONCE__">
  @font-face {
    font-family: 'Mona Sans VF';
    src: url('/static/MonaSansVF.woff2') format('woff2');
    font-weight: 200 900;
    font-stretch: 75% 125%;
    font-style: normal;
    font-display: swap;
  }
  @font-face {
    font-family: 'Mona Sans VF';
    src: url('/static/MonaSansVF.woff2') format('woff2');
    font-weight: 200 900;
    font-stretch: 75% 125%;
    font-style: italic;
    font-display: swap;
  }
  :root {
    --bg:           #060606;
    --bg-0:         #0b0b0c;
    --bg-1:         #111113;
    --panel:        rgba(17, 17, 19, 0.92);
    --card:         #171719;
    --card2:        #1e1f23;
    --card-hover:   #26282d;
    --fill:         rgba(255,255,255,0.08);
    --fill2:        rgba(255,255,255,0.045);
    --fill-strong:  rgba(255,255,255,0.12);
    --sep:          rgba(255,255,255,0.09);
    --sep-strong:   rgba(255,255,255,0.16);
    --text:         #f5f6f7;
    --text2:        rgba(245,246,247,0.72);
    --text3:        rgba(245,246,247,0.34);
    --text4:        rgba(245,246,247,0.16);
    --accent:       #f2f2f2;
    --accent-soft:  rgba(255,255,255,0.14);
    --shadow-lg:    0 28px 80px rgba(0,0,0,0.45);
    --shadow-md:    0 14px 36px rgba(0,0,0,0.32);
    --shadow-sm:    0 8px 22px rgba(0,0,0,0.22);
    --glow:         0 0 0 1px rgba(255,255,255,0.05), 0 16px 36px rgba(0,0,0,0.34);
    --radius:       18px;
    --radius-lg:    26px;
    --pill:         999px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body,
  button,
  input,
  select,
  textarea {
    font-family: 'Mona Sans VF', 'Mona Sans', 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-optical-sizing: auto;
    font-feature-settings: "ss05" on;
  }
  body {
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    letter-spacing: -0.01em;
    position: relative;
    overflow: hidden;
  }
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
      radial-gradient(circle at top left, rgba(255,255,255,0.06), transparent 28%),
      radial-gradient(circle at top right, rgba(91,103,122,0.12), transparent 24%),
      linear-gradient(180deg, #0c0c0e 0%, #070708 28%, #040404 100%);
    pointer-events: none;
    z-index: -2;
  }
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background:
      linear-gradient(90deg, transparent 0 18px, rgba(255,255,255,0.015) 18px 19px),
      linear-gradient(transparent 0 18px, rgba(255,255,255,0.015) 18px 19px);
    background-size: 19px 19px;
    opacity: 0.08;
    pointer-events: none;
    z-index: -1;
  }

  /* ── Layout ─────────────────────────────────── */
  .app { display: flex; flex-direction: column; height: 100vh; overflow: hidden; backdrop-filter: blur(8px); }

  header {
    border-bottom: 1px solid var(--sep);
    padding: 16px 28px 14px;
    display: flex;
    align-items: center;
    background: rgba(8,8,9,0.78);
    backdrop-filter: blur(24px) saturate(120%);
    -webkit-backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 10;
    box-shadow: 0 10px 34px rgba(0,0,0,0.28);
  }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-mark {
    width: 26px; height: 26px; border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    background: linear-gradient(180deg, #15243d 0%, #0c1422 100%);
    box-shadow: 0 8px 22px rgba(4, 10, 18, 0.34);
  }
  .brand-mark svg {
    width: 16px;
    height: 16px;
    display: block;
  }
  header h1 { font-size: 15px; font-weight: 600; letter-spacing: -0.02em; }
  .header-sub {
    font-size: 12px;
    color: var(--text3);
    margin-left: 10px;
    padding-left: 12px;
    border-left: 1px solid var(--sep);
  }
  .header-search {
    flex: 1 1 640px;
    max-width: 860px;
    min-width: 360px;
    margin: 0 auto;
    position: relative;
    z-index: 20;
  }
  .header-search-shell { position: relative; display: flex; flex-direction: column; gap: 7px; }
  .header-search-row { display: flex; align-items: center; gap: 10px; }
  .header-search-input-wrap {
    flex: 1;
    height: 44px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 14px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
  }
  .header-search-input-wrap:focus-within {
    border-color: rgba(255,255,255,0.22);
    background: rgba(255,255,255,0.055);
    box-shadow: 0 0 0 1px rgba(255,255,255,0.04);
  }
  .header-search-icon {
    color: var(--text3);
    flex-shrink: 0;
    opacity: 0.9;
  }
  #header-search-input {
    flex: 1;
    height: 100%;
    padding: 0;
    border: none;
    background: transparent;
    color: var(--text);
    font-size: 13px;
    outline: none;
  }
  #header-search-input:focus {
    border: none;
    background: transparent;
  }
  .search-mode-switch {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px;
    border-radius: var(--pill);
    border: 1px solid var(--sep);
    background: rgba(255,255,255,0.03);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    flex-shrink: 0;
  }
  .search-mode-btn {
    border: none;
    border-radius: var(--pill);
    padding: 7px 16px;
    background: transparent;
    color: var(--text3);
    font-size: 12px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
  }
  .search-mode-btn:hover:not(:disabled) { color: var(--text2); }
  .search-mode-btn.active {
    background: rgba(255,255,255,0.1);
    color: var(--text);
    box-shadow: 0 10px 22px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.06);
  }
  .search-mode-btn:disabled,
  .search-mode-btn.locked {
    color: var(--text4);
    cursor: not-allowed;
    opacity: 0.7;
  }
  .search-smart-hint {
    min-height: 14px;
    padding-left: 14px;
    font-size: 10px;
    color: var(--text3);
    letter-spacing: 0.02em;
    opacity: 0;
    transition: opacity 0.15s ease;
    pointer-events: none;
  }
  .search-smart-hint.visible { opacity: 1; }
  .header-search-dropdown {
    position: absolute;
    top: calc(100% + 9px);
    left: 0;
    right: 0;
    display: none;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(18,19,22,0.98);
    box-shadow: 0 18px 34px rgba(0,0,0,0.34);
    overflow: hidden;
  }
  .header-search-dropdown.open { display: block; }
  .search-dropdown-state {
    padding: 15px 16px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    color: var(--text2);
    font-size: 12px;
    line-height: 1.45;
  }
  .search-dropdown-state strong {
    font-size: 11px;
    font-weight: 800;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .search-result-list { max-height: 420px; overflow-y: auto; }
  .search-result-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 10px;
    padding: 10px 12px;
    border-top: 1px solid rgba(255,255,255,0.04);
    background: transparent;
    transition: background 0.15s, border-color 0.15s;
  }
  .search-result-row:first-child { border-top: none; }
  .search-result-row.active {
    background: linear-gradient(90deg, rgba(255,255,255,0.07), rgba(255,255,255,0.03));
    border-top-color: rgba(255,255,255,0.08);
  }
  .search-result-main {
    min-width: 0;
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr);
    gap: 11px;
    align-items: center;
    background: transparent;
    border: none;
    color: inherit;
    text-align: left;
    padding: 0;
    cursor: pointer;
    font-family: inherit;
  }
  .search-result-main:hover .search-result-title { color: #fff; }
  .search-result-thumb {
    width: 44px;
    height: 60px;
    border-radius: 10px;
    overflow: hidden;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 18px rgba(0,0,0,0.22);
  }
  .search-result-thumb img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
  }
  .search-result-copy { min-width: 0; display: flex; flex-direction: column; gap: 4px; }
  .search-result-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .search-result-meta {
    font-size: 11px;
    color: var(--text3);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .search-result-add-btn {
    align-self: center;
    height: 32px;
    padding: 0 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: var(--text2);
    font-size: 11px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
  }
  .search-result-add-btn:hover {
    background: rgba(255,255,255,0.08);
    color: var(--text);
    border-color: rgba(255,255,255,0.15);
  }

  main {
    display: grid;
    grid-template-columns: 365px 1fr;
    gap: 0;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  /* ── Left panel — builder ────────────────────── */
  .left-panel {
    padding: 24px 18px 0;
    border-right: 1px solid var(--sep);
    overflow-y: auto;
    background:
      linear-gradient(180deg, rgba(19,19,22,0.96) 0%, rgba(10,10,11,0.98) 55%, rgba(5,5,6,1) 100%);
    display: flex; flex-direction: column;
  }
  .left-panel-content { flex: 1; }
  .left-panel-footer {
    position: sticky; bottom: 0;
    border-top: 1px solid var(--sep);
    padding: 18px 4px 16px;
    background: linear-gradient(180deg, rgba(5,5,6,0) 0%, rgba(8,8,9,0.94) 18%, rgba(8,8,9,1) 100%);
    display: flex; flex-direction: column; align-items: center; gap: 8px;
  }
  .left-panel-footer .pane-footer-icons { display: flex; align-items: center; gap: 14px; }
  .left-panel-footer .pane-footer-text { font-size: 10px; color: var(--text3); }

  /* ── Mid panel — preview ─────────────────────── */
  .mid-panel {
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background:
      linear-gradient(180deg, rgba(8,8,9,0.82) 0%, rgba(5,5,6,0.96) 100%);
  }
  #preview-pane { overflow-y: auto; flex: 1; }

  /* ── Filter bar ──────────────────────────────── */
  .filter-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 16px 28px 12px;
    border-bottom: 1px solid var(--sep);
    flex-shrink: 0;
    flex-wrap: wrap;
  }
  /* Filter pill buttons (same style as genres btn) */
  .fb-filter-btn {
    display: flex; align-items: center; justify-content: center; gap: 5px;
    background: rgba(255,255,255,0.04);
    border: 1px solid transparent;
    border-radius: 10px; color: var(--text2); cursor: pointer;
    padding: 0 16px; font-size: 12px; font-family: inherit;
    height: 38px; flex: 1; min-width: 0;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.045);
    transition: background 0.18s, border-color 0.18s, color 0.18s, transform 0.18s, box-shadow 0.18s;
  }
  .fb-filter-btn:hover {
    background: rgba(255,255,255,0.07);
    border-color: var(--sep-strong); color: var(--text); transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }
  .fb-filter-btn.active {
    border-color: rgba(255,255,255,0.24); color: var(--text);
    background: rgba(255,255,255,0.10);
    box-shadow: none;
  }
  .fb-filter-btn.active .fb-chevron { transform: rotate(180deg); }
  .fb-filter-btn.has-value { color: var(--text); border-color: var(--sep-strong); }
  .year-dropdown { position: relative; display: flex; flex: 1.12 1 0; width: 0; min-width: 0; }
  .year-dropdown .fb-filter-btn { flex: 1 1 0; width: auto; }
  .year-dropdown .fb-filter-btn.open .fb-chevron { transform: rotate(180deg); }
  .year-menu {
    display: none;
    position: absolute;
    left: 0;
    top: calc(100% + 6px);
    min-width: 100%;
    max-height: 320px;
    overflow-y: auto;
    background: rgba(20,20,22,0.98);
    border-radius: 12px;
    border: 1px solid var(--sep);
    box-shadow: var(--shadow-lg);
    z-index: 110;
    padding: 6px 0;
    backdrop-filter: blur(18px);
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.2) transparent;
  }
  .year-menu.open { display: block; }
  .year-menu::-webkit-scrollbar { width: 8px; }
  .year-menu::-webkit-scrollbar-track { background: transparent; }
  .year-menu::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.18);
    border-radius: 999px;
    border: 2px solid transparent;
    background-clip: padding-box;
  }
  .year-menu::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.26); }
  .year-menu-item {
    display: block;
    width: 100%;
    padding: 9px 14px;
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 12px;
    color: var(--text2);
    font-family: inherit;
    transition: background 0.1s, color 0.1s;
  }
  .year-menu-item:hover { background: var(--fill); color: var(--text); }
  .year-menu-item.active {
    background: rgba(72,149,239,0.2);
    color: #9fc6ff;
    font-weight: 600;
  }
  .sort-icon-dim { opacity: 0.5; }
  /* Option pills inside the shared filter opts panel */
  .filter-opts-pills { display: flex; flex-wrap: wrap; gap: 6px; }
  .filter-opt-pill {
    padding: 6px 13px; border-radius: var(--pill);
    border: 1px solid var(--sep); background: rgba(255,255,255,0.035);
    color: var(--text2); font-size: 12px; font-family: inherit;
    cursor: pointer; transition: background 0.16s, color 0.16s, border-color 0.16s, transform 0.16s, box-shadow 0.16s;
  }
  .filter-opt-pill:hover {
    background: rgba(255,255,255,0.075); color: var(--text); border-color: var(--sep-strong);
    transform: translateY(-1px);
  }
  .filter-opt-pill.selected {
    background: #e7e7e7;
    border-color: transparent; color: #0a0a0a; font-weight: 600;
    box-shadow: none;
  }
  .filter-opt-pill.disabled { opacity: 0.35; cursor: default; }
  /* Name input + Add button inline in filter bar */
  .fb-name-input {
    height: 38px; border-radius: 15px; padding: 0 16px;
    font-size: 13px; background: rgba(255,255,255,0.04);
    border: 1px solid var(--sep); color: var(--text);
    font-family: inherit; min-width: 0; width: 100%;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.035);
  }
  .fb-name-input::placeholder { color: var(--text3); }
  .fb-name-input:focus { outline: none; background: rgba(255,255,255,0.055); border-color: rgba(255,255,255,0.24); }
  .btn-fb { height: 38px; padding: 0 16px; border-radius: 15px; font-size: 12px; }
  .fb-add-btn {
    height: 38px; padding: 0 18px; border-radius: 6px; font-size: 12px;
    font-family: inherit; font-weight: 700; cursor: pointer; flex-shrink: 0;
    background: #ececec;
    border: 1px solid transparent;
    color: #0d0d0d;
    box-shadow: none;
    transition: transform 0.16s, opacity 0.16s;
  }
  .fb-add-btn:hover { transform: translateY(-1px); }
  .fb-chevron { transition: transform 0.15s ease; font-size: 9px; opacity: 0.5; }
  .fb-sep { width: 1px; height: 22px; background: var(--sep); flex-shrink: 0; margin: 0 2px; }
  .fb-adult-toggle {
    display: flex; align-items: center; gap: 5px;
    background: rgba(255,255,255,0.04); border: 1px solid transparent;
    border-radius: 10px; color: var(--text2); cursor: pointer;
    padding: 0 12px; font-size: 12px; font-family: inherit;
    height: 38px; flex-shrink: 0; user-select: none;
    transition: background 0.15s, border-color 0.15s, color 0.15s, transform 0.15s;
  }
  .fb-adult-toggle:hover { background: rgba(255,255,255,0.075); border-color: var(--sep-strong); color: var(--text); transform: translateY(-1px); }
  .fb-adult-toggle.active { background: rgba(232,93,4,0.12); border-color: rgba(232,93,4,0.45); color: #e85d04; }
  .fb-adult-toggle input[type=checkbox] { width: 12px; height: 12px; accent-color: #e85d04; cursor: pointer; margin: 0; }
  /* Inline score slider in filter bar */
  .fb-slider-wrap {
    display: flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.04); border: 1px solid transparent;
    border-radius: 10px; padding: 0 14px; height: 38px;
    flex: 1.3; min-width: 0;
    transition: background 0.15s, border-color 0.15s, transform 0.15s;
  }
  .fb-slider-wrap:hover { background: rgba(255,255,255,0.075); border-color: var(--sep-strong); transform: translateY(-1px); }
  .fb-slider-label { font-size: 12px; color: var(--text3); white-space: nowrap; }
  .fb-slider-wrap input[type=range] {
    flex: 1; min-width: 40px; height: 3px; margin: 0;
    -webkit-appearance: none; border-radius: 2px;
    background: rgba(255,255,255,0.11); outline: none;
  }
  .fb-slider-wrap input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none; width: 13px; height: 13px;
    border-radius: 50%; background: #fff; cursor: pointer;
    box-shadow: 0 1px 4px rgba(0,0,0,0.5);
  }
  .fb-slider-val { font-size: 11px; font-weight: 500; color: var(--text2); min-width: 24px; }

  /* ── Always-visible options panel ───────────── */
  .options-panel {
    display: flex; flex-direction: column; gap: 10px;
    padding: 12px 28px 16px; border-bottom: 1px solid var(--sep);
    flex-shrink: 0; max-height: 150px; overflow-y: auto;
    background: rgba(255,255,255,0.01);
  }

  .fb-name-wrap { position: relative; flex: 1.8; min-width: 0; display: flex; }
  .fb-name-wrap .fb-name-input { flex: 1; }
  #catalog-name-error {
    display: none; position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%);
    font-size: 11px; color: #fff; background: #e85d04; border-radius: 6px;
    padding: 4px 10px; white-space: nowrap; pointer-events: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4); z-index: 20;
  }
  #catalog-name-error.visible { display: block; }
  #catalog-name-error::after {
    content: ''; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%);
    border: 5px solid transparent; border-bottom-color: #e85d04;
  }
  .fb-name-input.input-error { border-color: #e85d04; }

  /* ── Pane tab bar (Preview / Catalogs switch) ─── */
  .pane-tabbar {
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px; padding: 14px 28px 12px; flex-shrink: 0; flex-wrap: wrap;
    border-bottom: 1px solid var(--sep);
  }
  .pane-tabs {
    display: flex; background: rgba(255,255,255,0.03); border-radius: var(--pill);
    padding: 4px; gap: 4px; flex-shrink: 0;
    border: 1px solid var(--sep);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
  }
  .pane-tab {
    padding: 7px 16px; border-radius: var(--pill); border: none; cursor: pointer;
    font-size: 12px; font-family: inherit; font-weight: 600;
    color: var(--text3); background: transparent;
    transition: background 0.15s, color 0.15s;
  }
  .pane-tab:hover { color: var(--text2); }
  .pane-tab.active {
    background: rgba(255,255,255,0.10);
    color: var(--text); box-shadow: 0 10px 22px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.06);
  }
  .pane-tab-extras {
    display: flex; align-items: center; gap: 12px;
    flex-wrap: wrap; flex: 1; min-width: 0; justify-content: flex-end;
  }
  .panel-sub-inline { font-size: 11px; color: var(--text3); }
  .mid-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-shrink: 0;
  }

  /* ── Filter tags ─────────────────────────────── */
  .filter-tags { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; min-height: 24px; flex-shrink: 0; }
  .filter-tag {
    display: inline-flex; align-items: center; gap: 3px;
    padding: 4px 10px; border-radius: var(--pill);
    background: rgba(255,255,255,0.05); color: var(--text2);
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 11px; font-weight: 500; cursor: default;
    transition: background 0.15s, color 0.15s, border-color 0.15s, transform 0.15s; user-select: none;
  }
  .filter-tag:hover { background: rgba(255,255,255,0.085); color: var(--text); border-color: var(--sep-strong); transform: translateY(-1px); }
  .filter-tag-x {
    display: none; cursor: pointer; margin-left: 2px;
    color: var(--text3); font-size: 14px; line-height: 1; font-weight: 400;
    background: none; border: none; padding: 0; font-family: inherit;
  }
  .filter-tag:hover .filter-tag-x { display: inline; }
  .filter-tag-x:hover { color: var(--text); }
  .filter-tag-clear {
    display: none; background: none;
    border: 1px solid var(--sep); border-radius: var(--pill);
    color: var(--text3); font-size: 11px; font-family: inherit;
    padding: 5px 12px; cursor: pointer; gap: 5px;
    transition: color 0.15s, border-color 0.15s, background 0.15s;
  }
  .filter-tags:hover .filter-tag-clear { display: inline-flex; align-items: center; }
  .filter-tag-clear:hover { color: var(--text2); border-color: var(--text3); background: rgba(255,255,255,0.04); }

  /* ── Pane tabbar layout ──────────────────────── */
  .pane-tabbar-left { display: flex; align-items: center; gap: 12px; min-width: 0; flex: 1; }
  .filter-tags-wrap { display: flex; align-items: center; gap: 6px; min-width: 0; }
  .tags-icon { color: var(--text3); flex-shrink: 0; }

  /* ── Sort dropdown ───────────────────────────── */
  .sort-dropdown { position: relative; flex-shrink: 0; }
  .sort-btn {
    display: flex; align-items: center; gap: 5px;
    background: rgba(255,255,255,0.03); border: 1px solid transparent; cursor: pointer;
    font-size: 11px; color: var(--text3); padding: 7px 11px;
    border-radius: var(--pill); font-family: inherit;
    transition: background 0.15s, color 0.15s, border-color 0.15s, transform 0.15s;
  }
  .sort-btn:hover { background: rgba(255,255,255,0.075); color: var(--text2); border-color: var(--sep-strong); transform: translateY(-1px); }
  .sort-btn.open  { background: rgba(255,255,255,0.075); color: var(--text2); border-color: var(--sep-strong); }
  .sort-btn-label { font-weight: 600; color: var(--text2); }
  .sort-btn-chevron { font-size: 8px; opacity: 0.5; transition: transform 0.15s; }
  .sort-btn.open .sort-btn-chevron { transform: rotate(180deg); }
  .sort-menu {
    display: none; position: absolute; right: 0; top: calc(100% + 6px);
    background: rgba(20,20,22,0.98); border-radius: 16px;
    border: 1px solid var(--sep);
    box-shadow: var(--shadow-lg);
    min-width: 160px; z-index: 100; overflow: hidden;
    backdrop-filter: blur(18px);
  }
  .sort-menu.open { display: block; }
  .sort-menu-item {
    display: block; width: 100%;
    padding: 10px 16px; text-align: left;
    background: none; border: none; border-bottom: 1px solid rgba(255,255,255,0.05);
    cursor: pointer; font-size: 13px; color: var(--text2); font-family: inherit;
    transition: background 0.1s, color 0.1s;
  }
  .sort-menu-item:last-child { border-bottom: none; }
  .sort-menu-item:hover { background: var(--fill); color: var(--text); }
  .sort-menu-item.active { color: var(--text); font-weight: 500; }

  /* ── View controls ───────────────────────────── */
  .view-controls {
    display: flex; align-items: center; gap: 10px; flex-shrink: 0;
    padding: 0;
    border-radius: 0;
    background: transparent;
    border: none;
  }
  .view-sep { color: var(--sep); font-size: 14px; }
  .view-toggle {
    display: flex; gap: 3px;
    padding: 0;
    border-radius: 0;
    background: transparent;
    border: none;
  }
  .view-btn {
    background: none; border: none; cursor: pointer;
    color: var(--text3); padding: 7px; border-radius: 10px;
    display: flex; align-items: center;
    transition: background 0.15s, color 0.15s, transform 0.15s;
  }
  .view-btn:hover { background: rgba(255,255,255,0.07); color: var(--text2); transform: translateY(-1px); }
  .view-btn.active {
    background: rgba(255,255,255,0.10);
    color: var(--text);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  }
  .poster-style-picker {
    display: flex; align-items: center; gap: 2px;
    height: 30px; padding: 2px;
    border-radius: 9px; border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.035);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
  }
  .poster-style-btn {
    height: 24px; min-width: 34px; padding: 0 8px;
    border: 0; border-radius: 7px;
    background: transparent; color: var(--text3);
    cursor: pointer; font-size: 10px; font-weight: 700; font-family: inherit;
    line-height: 1; white-space: nowrap;
    transition: background 0.15s, color 0.15s, transform 0.15s, box-shadow 0.15s;
  }
  .poster-style-btn:hover { color: var(--text2); background: rgba(255,255,255,0.065); transform: translateY(-1px); }
  .poster-style-btn.active {
    color: var(--text);
    background: rgba(255,255,255,0.10);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  }

  /* ── List view ───────────────────────────────── */
  .preview-list { display: flex; flex-direction: column; }
  .poster-lab-card .poster-img { aspect-ratio: 2 / 3; }
  .poster-lab-card .poster-img img { object-position: center; }
  .poster-lab-card .poster-title,
  .poster-lab-card .poster-score { margin-top: 8px; }
  .poster-lab-card {
    box-shadow: none;
    border-color: rgba(255,255,255,0.10);
  }
  .poster-lab-card:hover {
    box-shadow: none;
  }
  .list-item {
    display: grid;
    grid-template-columns: 44px 1fr 90px 120px 140px;
    gap: 20px; align-items: center;
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    text-decoration: none; color: inherit;
    border-radius: 10px;
    transition: background 0.15s, transform 0.15s, border-color 0.15s;
    border: 1px solid transparent;
  }
  .list-item:last-child { border-bottom: none; }
  .list-item:hover { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.07); transform: translateY(-1px); }
  .list-thumb {
    width: 44px; height: 62px; border-radius: 4px;
    overflow: hidden; background: var(--card); flex-shrink: 0;
    box-shadow: 0 10px 24px rgba(0,0,0,0.28);
  }
  .list-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .list-main { min-width: 0; }
  .list-title {
    font-size: 13px; font-weight: 500; letter-spacing: -0.1px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    margin-bottom: 6px; color: var(--text);
  }
  .list-genres { display: flex; flex-wrap: wrap; gap: 4px; }
  .genre-badge {
    display: inline-block; padding: 3px 8px; border-radius: 10px;
    font-size: 10px; font-weight: 500; line-height: 1.4;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.12);
  }
  .list-score { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }
  .list-score-pct { font-size: 13px; font-weight: 600; color: var(--text); display: flex; align-items: center; gap: 4px; }
  .al-logo-badge {
    display: inline-flex; align-items: center; justify-content: center;
    background: linear-gradient(180deg, #15243d 0%, #0c1422 100%);
    box-shadow: 0 4px 10px rgba(4, 10, 18, 0.24);
    flex-shrink: 0;
  }
  .list-al-icon {
    width: 11px; height: 11px; border-radius: 2px; opacity: 0.86;
    font-size: 8px; line-height: 1;
  }
  .list-stat { font-size: 11px; color: var(--text3); }
  .list-meta-col { display: flex; flex-direction: column; gap: 3px; }
  .list-meta-primary { font-size: 12px; color: var(--text2); }
  .list-meta-secondary { font-size: 11px; color: var(--text3); }

  /* ── Detail card view ───────────────────────── */
  .detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
    gap: 14px;
    padding: 20px 28px 28px;
  }
  .detail-card {
    display: flex; border-radius: 6px;
    overflow: hidden; background: linear-gradient(180deg, rgba(27,27,30,0.98), rgba(18,18,20,0.98));
    color: inherit; cursor: pointer;
    text-decoration: none;
    transition: background 0.18s, transform 0.18s, box-shadow 0.18s, border-color 0.18s;
    height: 270px;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: var(--shadow-sm);
    --studio-color: #ffffff;
    --studio-color-soft: #ffffff;
    --studio-banner: rgba(255,255,255,0.28125);
    --studio-banner-ink: rgba(44,46,50,0.38);
    --studio-banner-border: rgba(255,255,255,0.14);
    --detail-banner-height: 88px;
  }
  .detail-card:hover {
    background: linear-gradient(180deg, rgba(34,35,39,0.98), rgba(21,22,25,0.98));
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    border-color: rgba(255,255,255,0.11);
  }
  .detail-card:visited { color: inherit; }
  .detail-poster {
    flex: 0 0 35%; position: relative; overflow: hidden; background: var(--fill2);
  }
  .detail-poster img { width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; }
  .detail-poster-overlay {
    position: absolute; left: 0; right: 0; bottom: 0;
    top: calc(100% - var(--detail-banner-height));
    padding: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.02) 0%, rgba(0,0,0,0.38) 26%, rgba(0,0,0,0.82) 72%, rgba(0,0,0,0.96) 100%);
    pointer-events: none;
    display: flex;
    align-items: flex-end;
  }
  .detail-overlay-inner {
    width: 100%;
    background: linear-gradient(var(--studio-banner-ink), var(--studio-banner-ink)), var(--studio-banner);
    padding: 7px 14px;
    border-radius: 0;
    min-height: var(--detail-banner-height);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .detail-overlay-title {
    font-size: 14px; font-weight: 700; color: #fff;
    overflow: hidden;
    line-height: 1.18; letter-spacing: -0.035em;
    text-shadow: 0 1px 12px rgba(0,0,0,0.45);
    transition: color 0.18s ease;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
  }
  .detail-card:hover .detail-overlay-title { color: var(--studio-color-soft); }
  .detail-overlay-studio {
    font-size: 11px; font-weight: 600; margin-top: 4px;
    color: var(--studio-color-soft);
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    letter-spacing: 0.01em;
    text-shadow: 0 1px 10px rgba(0,0,0,0.3);
  }
  .detail-body {
    flex: 1; min-width: 0; padding: 16px 16px 14px;
    display: flex; flex-direction: column; gap: 4px;
    overflow: hidden;
  }
  .detail-header {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 8px;
    flex-shrink: 0;
  }
  .detail-header-left { display: flex; flex-direction: column; gap: 1px; min-width: 0; }
  .detail-period { font-size: 11px; color: var(--text3); }
  .detail-airing-label { font-size: 10px; color: var(--text3); }
  .detail-airing-time { font-size: 14px; font-weight: 700; color: var(--text); line-height: 1.25; letter-spacing: -0.3px; }
  .detail-score-badge {
    display: flex; align-items: center; gap: 4px; flex-shrink: 0;
    font-size: 12px; font-weight: 600; color: #fff;
    border-radius: var(--pill);
    padding: 4px 12px 4px 9px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.08);
    min-width: 78px;
    justify-content: center;
    white-space: nowrap;
  }
  .detail-score-icon {
    width: 14px; height: 14px; border-radius: 3px;
    line-height: 1;
  }
  .detail-meta { font-size: 11px; color: var(--text3); flex-shrink: 0; margin-top: 4px; }
  .detail-desc {
    font-size: 11px; color: var(--text2); line-height: 1.65;
    flex: 1; overflow-y: auto; min-height: 0;
    margin-top: 6px;
  }
  .detail-desc::-webkit-scrollbar { width: 3px; }
  .detail-desc::-webkit-scrollbar-track { background: transparent; }
  .detail-desc::-webkit-scrollbar-thumb { background: rgba(84,84,88,0.28); border-radius: 2px; }
  .detail-desc::-webkit-scrollbar-thumb:hover { background: rgba(84,84,88,0.5); }
  .detail-footer {
    display: flex; align-items: center; gap: 6px; flex-shrink: 0;
    margin: 8px -16px -14px;
    padding: 10px 16px 14px;
    background: rgba(0,0,0,0.28);
    border-top: 1px solid rgba(255,255,255,0.04);
  }
  .detail-genres { display: flex; flex-wrap: wrap; gap: 4px; }

  /* ── Pane footer ─────────────────────────────── */
  .pane-footer {
    border-top: 0.5px solid var(--sep);
    padding: 14px 28px;
    display: flex; align-items: center; gap: 12px;
    margin-top: 8px;
  }
  .pane-footer-icons { display: flex; align-items: center; gap: 10px; }
  .pane-footer-icon {
    color: var(--text3); text-decoration: none;
    display: flex; align-items: center;
    transition: color 0.15s, filter 0.15s;
  }
  .pane-footer-icon:hover { color: #fff; filter: drop-shadow(0 0 4px rgba(255,255,255,0.5)); }
  .pane-footer-text {
    font-size: 11px; color: var(--text3);
  }

  /* Preview states */
  #preview-area { padding: 12px 0 4px; }
  .preview-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 180px;
    color: var(--text3);
    font-size: 13px;
    text-align: center;
    gap: 12px;
    margin: 0 28px;
    border-radius: 24px;
    border: 1px dashed rgba(255,255,255,0.12);
    background: linear-gradient(180deg, rgba(255,255,255,0.025), rgba(255,255,255,0.015));
  }
  .preview-prompt-icon { font-size: 34px; opacity: 0.25; }
  .preview-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 180px;
  }
  .preview-list { padding: 12px 28px 0; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner {
    width: 22px; height: 22px;
    border: 2px solid var(--sep);
    border-top-color: var(--text2);
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
  }
  .preview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 18px;
    padding: 20px 28px 28px;
  }
  .poster {
    display: flex; flex-direction: column; gap: 9px; width: 210px; flex-shrink: 0;
    text-decoration: none; color: inherit; cursor: pointer;
    transition: transform 0.18s ease;
    --studio-color: #ffffff;
    --studio-color-soft: #ffffff;
    --studio-banner: rgba(255,255,255,0.28125);
    --studio-banner-ink: rgba(44,46,50,0.38);
  }
  .poster:hover { transform: translateY(-4px); }
  .poster-img {
    border-radius: 5px;
    overflow: hidden;
    aspect-ratio: 2/3;
    background: var(--card);
    position: relative;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: var(--shadow-md);
  }
  .poster-img img {
    width: 100%; height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.22s ease;
  }
  .poster:hover .poster-img img { transform: none; }
  .poster-genres {
    position: absolute;
    top: 0; left: 0; right: 0;
    padding: 8px 6px 20px;
    display: flex; flex-wrap: wrap; gap: 3px; justify-content: center;
    background: linear-gradient(180deg, rgba(0,0,0,0.78) 0%, transparent 100%);
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
  }
  .poster:hover .poster-genres { opacity: 1; }
  .poster-genres .genre-badge { font-size: 9px; padding: 2px 6px; }
  .genre-badge[data-genre] { cursor: pointer; }
  .genre--action { background:#e85d04bb;color:#fff;border:0.5px solid #e85d04dd; }
  .genre--adventure { background:#f48c06bb;color:#fff;border:0.5px solid #f48c06dd; }
  .genre--comedy { background:#a7c957bb;color:#fff;border:0.5px solid #a7c957dd; }
  .genre--drama { background:#4895efbb;color:#fff;border:0.5px solid #4895efdd; }
  .genre--ecchi { background:#f72585bb;color:#fff;border:0.5px solid #f72585dd; }
  .genre--fantasy { background:#7b2fbebb;color:#fff;border:0.5px solid #7b2fbedd; }
  .genre--horror { background:#9b2226bb;color:#fff;border:0.5px solid #9b2226dd; }
  .genre--mahou-shoujo { background:#f48fb1bb;color:#fff;border:0.5px solid #f48fb1dd; }
  .genre--mecha { background:#4361eebb;color:#fff;border:0.5px solid #4361eedd; }
  .genre--music { background:#c77dffbb;color:#fff;border:0.5px solid #c77dffdd; }
  .genre--mystery { background:#0077b6bb;color:#fff;border:0.5px solid #0077b6dd; }
  .genre--psychological { background:#bc6c25bb;color:#fff;border:0.5px solid #bc6c25dd; }
  .genre--romance { background:#e63946bb;color:#fff;border:0.5px solid #e63946dd; }
  .genre--sci-fi { background:#48cae4bb;color:#fff;border:0.5px solid #48cae4dd; }
  .genre--slice-of-life { background:#52b788bb;color:#fff;border:0.5px solid #52b788dd; }
  .genre--sports { background:#2dc653bb;color:#fff;border:0.5px solid #2dc653dd; }
  .genre--supernatural { background:#9d4eddbb;color:#fff;border:0.5px solid #9d4edddd; }
  .genre--thriller { background:#d62828bb;color:#fff;border:0.5px solid #d62828dd; }
  .genre-soft--action { background:#e85d0428;color:#e85d04;border:0.5px solid #e85d0455; }
  .genre-soft--adventure { background:#f48c0628;color:#f48c06;border:0.5px solid #f48c0655; }
  .genre-soft--comedy { background:#a7c95728;color:#a7c957;border:0.5px solid #a7c95755; }
  .genre-soft--drama { background:#4895ef28;color:#4895ef;border:0.5px solid #4895ef55; }
  .genre-soft--ecchi { background:#f7258528;color:#f72585;border:0.5px solid #f7258555; }
  .genre-soft--fantasy { background:#7b2fbe28;color:#7b2fbe;border:0.5px solid #7b2fbe55; }
  .genre-soft--horror { background:#9b222628;color:#9b2226;border:0.5px solid #9b222655; }
  .genre-soft--mahou-shoujo { background:#f48fb128;color:#f48fb1;border:0.5px solid #f48fb155; }
  .genre-soft--mecha { background:#4361ee28;color:#4361ee;border:0.5px solid #4361ee55; }
  .genre-soft--music { background:#c77dff28;color:#c77dff;border:0.5px solid #c77dff55; }
  .genre-soft--mystery { background:#0077b628;color:#0077b6;border:0.5px solid #0077b655; }
  .genre-soft--psychological { background:#bc6c2528;color:#bc6c25;border:0.5px solid #bc6c2555; }
  .genre-soft--romance { background:#e6394628;color:#e63946;border:0.5px solid #e6394655; }
  .genre-soft--sci-fi { background:#48cae428;color:#48cae4;border:0.5px solid #48cae455; }
  .genre-soft--slice-of-life { background:#52b78828;color:#52b788;border:0.5px solid #52b78855; }
  .genre-soft--sports { background:#2dc65328;color:#2dc653;border:0.5px solid #2dc65355; }
  .genre-soft--supernatural { background:#9d4edd28;color:#9d4edd;border:0.5px solid #9d4edd55; }
  .genre-soft--thriller { background:#d6282828;color:#d62828;border:0.5px solid #d6282855; }
  .theme-orange { --studio-color:#e85d04; --studio-color-soft:#ef8e4f; --studio-banner:rgba(232,93,4,0.28125); --studio-banner-border:rgba(232,93,4,0.12); }
  .theme-gold { --studio-color:#f48c06; --studio-color-soft:#f8af51; --studio-banner:rgba(244,140,6,0.28125); --studio-banner-border:rgba(244,140,6,0.12); }
  .theme-lime { --studio-color:#a7c957; --studio-color-soft:#c1d989; --studio-banner:rgba(167,201,87,0.28125); --studio-banner-border:rgba(167,201,87,0.12); }
  .theme-blue { --studio-color:#4895ef; --studio-color-soft:#7fb5f4; --studio-banner:rgba(72,149,239,0.28125); --studio-banner-border:rgba(72,149,239,0.12); }
  .theme-pink { --studio-color:#f72585; --studio-color-soft:#f966aa; --studio-banner:rgba(247,37,133,0.28125); --studio-banner-border:rgba(247,37,133,0.12); }
  .theme-purple { --studio-color:#7b2fbe; --studio-color-soft:#a36dd2; --studio-banner:rgba(123,47,190,0.28125); --studio-banner-border:rgba(123,47,190,0.12); }
  .theme-red { --studio-color:#e63946; --studio-color-soft:#ee747e; --studio-banner:rgba(230,57,70,0.28125); --studio-banner-border:rgba(230,57,70,0.12); }
  .theme-cyan { --studio-color:#48cae4; --studio-color-soft:#7fdaec; --studio-banner:rgba(72,202,228,0.28125); --studio-banner-border:rgba(72,202,228,0.12); }
  .theme-green { --studio-color:#52b788; --studio-color-soft:#86cdac; --studio-banner:rgba(82,183,136,0.28125); --studio-banner-border:rgba(82,183,136,0.12); }
  .theme-violet { --studio-color:#9d4edd; --studio-color-soft:#ba83e7; --studio-banner:rgba(157,78,221,0.28125); --studio-banner-border:rgba(157,78,221,0.12); }
  .theme-sky { --studio-color:#0077b6; --studio-color-soft:#4d82cc; --studio-banner:rgba(0,119,182,0.28125); --studio-banner-border:rgba(0,119,182,0.12); }
  .theme-amber { --studio-color:#f4c430; --studio-color-soft:#f8d66e; --studio-banner:rgba(244,196,48,0.28125); --studio-banner-border:rgba(244,196,48,0.12); }
  .theme-coral { --studio-color:#ff7a59; --studio-color-soft:#ffa28b; --studio-banner:rgba(255,122,89,0.28125); --studio-banner-border:rgba(255,122,89,0.12); }
  .theme-mint { --studio-color:#26c485; --studio-color-soft:#67d6aa; --studio-banner:rgba(38,196,133,0.28125); --studio-banner-border:rgba(38,196,133,0.12); }
  .theme-rose { --studio-color:#ff5d8f; --studio-color-soft:#ff8eb1; --studio-banner:rgba(255,93,143,0.28125); --studio-banner-border:rgba(255,93,143,0.12); }
  .theme-ocean { --studio-color:#118ab2; --studio-color-soft:#58adc9; --studio-banner:rgba(17,138,178,0.28125); --studio-banner-border:rgba(17,138,178,0.12); }
  .theme-indigo { --studio-color:#3a86ff; --studio-color-soft:#75aaff; --studio-banner:rgba(58,134,255,0.28125); --studio-banner-border:rgba(58,134,255,0.12); }
  .theme-magenta { --studio-color:#ff006e; --studio-color-soft:#ff4d9a; --studio-banner:rgba(255,0,110,0.28125); --studio-banner-border:rgba(255,0,110,0.12); }
  .detail-banner-lines-1 { --detail-banner-height: 51px; }
  .detail-banner-lines-2 { --detail-banner-height: 68px; }
  .detail-banner-lines-3 { --detail-banner-height: 85px; }
  .detail-banner-lines-4 { --detail-banner-height: 102px; }
  .poster-bottom-tags {
    position: absolute;
    left: 10px;
    right: 10px;
    bottom: 12px;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 6px;
    z-index: 1;
    pointer-events: none;
    opacity: 0;
    transition: bottom 0.2s ease, opacity 0.2s ease;
  }
  .poster:hover .poster-bottom-tags { opacity: 1; }
  .poster.has-banner .poster-bottom-tags { bottom: 46px; }
  .poster-neutral-tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 9px;
    border-radius: 10px;
    background: rgba(214, 218, 224, 0.52);
    border: 1px solid rgba(214, 218, 224, 0.58);
    color: rgba(12, 14, 18, 0.92);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: -0.01em;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.14);
  }
  .poster-meta {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 10px 14px;
    background: linear-gradient(var(--studio-banner-ink), var(--studio-banner-ink)), var(--studio-banner);
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
    text-align: center;
  }
  .poster:hover .poster-meta { opacity: 1; }
  .poster-meta-row {
    font-size: 12px; color: rgba(255,255,255,0.96); font-weight: 700;
    letter-spacing: -0.02em;
    text-shadow: 0 1px 12px rgba(0,0,0,0.4);
  }
  .poster-title {
    font-size: 13px;
    color: var(--text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: 600;
    letter-spacing: -0.02em;
    transition: color 0.18s ease;
  }
  .poster:hover .poster-title { color: var(--studio-color-soft); }
  .preset-name.ai-title {
    display: block;
  }
  .ai-star-icon {
    width: 15px;
    height: 15px;
    color: #a78bfa;
    flex-shrink: 0;
    filter: drop-shadow(0 0 8px rgba(167,139,250,0.28));
  }
  .poster-score {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    color: var(--text2);
    margin-top: -2px;
  }
  .poster-anilist-logo {
    width: 13px; height: 13px; border-radius: 3px;
    font-size: 9px; line-height: 1;
  }
  .al-logo-badge svg {
    width: 100%;
    height: 100%;
    display: block;
  }
  .poster-score-value,
  .list-score-value,
  .detail-score-value {
    display: inline-block;
    line-height: 1;
    letter-spacing: -0.02em;
  }
  .detail-score-value {
    min-width: 38px;
    text-align: right;
    color: #fff;
  }
  .score-high { color: #4a9f79; }
  .score-mid { color: #63b68f; }
  .score-low { color: #f48c06; }
  .score-poor { color: #e63946; }
  .score-none { color: var(--text3); }
  .detail-score-badge.detail-score-high { background: #4a9f79; }
  .detail-score-badge.detail-score-mid { background: #63b68f; }
  .detail-score-badge.detail-score-low { background: #f48c06; }
  .detail-score-badge.detail-score-poor { background: #e63946; }
  .detail-score-badge.detail-score-none { background: rgba(255,255,255,0.07); }
  .hidden { display: none !important; }
  .pane-hidden { display: none !important; }
  .pointer-disabled { pointer-events: none !important; }
  .ai-badge {
    background: rgba(139,92,246,0.12);
    color: #a78bfa;
    border-color: rgba(139,92,246,0.3);
  }
  .account-source-badge {
    background: rgba(232,93,4,0.12);
    color: #f48c06;
    border-color: rgba(232,93,4,0.3);
  }
  .catalog-type-badge.account-type-badge {
    background: rgba(232,93,4,0.12);
    color: #f48c06;
    border-color: rgba(232,93,4,0.3);
  }
  .catalog-type-badge.ai-type-badge {
    background: rgba(139,92,246,0.12);
    color: #a78bfa;
    border-color: rgba(139,92,246,0.3);
  }
  .ai-connected-hidden { display: none; }
  .select-hidden { display: none; }
  .catalogs-hidden { display: none !important; }
  .catalog-meta-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 20px;
  }
  .catalog-recipe-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 12px 14px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    background: rgba(255,255,255,0.035);
  }
  .catalog-recipe-copy { min-width: 0; }
  .catalog-recipe-title {
    font-size: 12px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .catalog-recipe-sub {
    margin-top: 4px;
    font-size: 11px;
    color: var(--text3);
    line-height: 1.35;
  }
  .smart-row-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-top: 10px;
    padding: 12px 14px;
    border: 1px solid rgba(139,92,246,0.20);
    border-radius: 8px;
    background: rgba(139,92,246,0.055);
    position: relative;
    transition: opacity 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
  }
  .smart-row-bar.smart-auth-missing {
    opacity: 0.52;
  }
  .smart-row-bar.smart-key-missing {
    border-color: rgba(220,38,38,0.48);
    box-shadow: inset 0 0 0 1px rgba(220,38,38,0.12);
  }
  .smart-row-bar.smart-key-missing:hover {
    border-color: rgba(220,38,38,0.72);
  }
  .smart-row-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }
  .smart-settings-wrap {
    position: relative;
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
  }
  .smart-row-note,
  .smart-missing-note {
    position: absolute;
    z-index: 130;
    max-width: min(280px, calc(100vw - 64px));
    padding: 8px 10px;
    border: 1px solid rgba(248,113,113,0.26);
    border-radius: 8px;
    background: rgba(24,24,27,0.98);
    color: #fecaca;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.35;
    box-shadow: var(--shadow-lg);
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.14s ease, transform 0.14s ease, visibility 0.14s ease;
  }
  .smart-row-note {
    width: max-content;
    max-width: min(260px, calc(100vw - 64px));
    right: calc(100% + 10px);
    top: 50%;
    text-align: left;
    word-break: normal;
    overflow-wrap: break-word;
    transform: translateY(-50%) scale(0.98);
  }
  .smart-missing-note {
    right: 14px;
    top: calc(100% + 8px);
    transform: translateY(-3px);
  }
  .smart-row-bar.smart-has-note:hover .smart-row-note,
  .smart-row-bar.smart-has-note:focus-within .smart-row-note {
    opacity: 1;
    visibility: visible;
    transform: translateY(-50%) scale(1);
  }
  .catalog-item.smart-has-note:hover .smart-missing-note,
  .catalog-item.smart-has-note:focus-within .smart-missing-note {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
  .smart-settings-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.05);
    color: var(--text2);
    cursor: pointer;
    font-family: inherit;
  }
  .smart-settings-btn:hover { background: rgba(255,255,255,0.09); color: var(--text); }
  @media (max-width: 760px) {
    .smart-row-note {
      right: auto;
      left: 0;
      top: calc(100% + 8px);
      transform: translateY(-3px);
    }
    .smart-row-bar.smart-has-note:hover .smart-row-note,
    .smart-row-bar.smart-has-note:focus-within .smart-row-note {
      transform: translateY(0);
    }
  }
  .qr-section-tight { margin-top: 0; }
  .stack-end { margin-top: auto; }
  .divider-tight { margin: 12px 0; }
  .inline-hint {
    font-size: 11px;
    color: var(--text3);
    margin-top: 6px;
  }

  /* ── Section headings ────────────────────────── */
  .section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 12px;
    padding-left: 4px;
  }
  section { margin-bottom: 32px; }

  /* ── Preset list — Apple grouped rows ────────── */
  .presets-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .preset-card {
    background: rgba(24,24,27,0.98);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 16px 16px;
    cursor: pointer;
    transition: background 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
  }
  .preset-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: none;
    opacity: 0;
    transition: opacity 0.18s ease;
    pointer-events: none;
  }
  .preset-card:hover  {
    background: rgba(31,32,36,0.98);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    border-color: rgba(255,255,255,0.11);
  }
  .preset-card:hover::before { opacity: 1; }
  .preset-card:active { background: rgba(255,255,255,0.06); }
  .preset-info { flex: 1; min-width: 0; }
  .preset-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
    white-space: nowrap;
  }
  .preset-name { font-weight: 700; font-size: 15px; letter-spacing: -0.03em; }
  .preset-desc { font-size: 12px; color: var(--text2); margin-top: 4px; line-height: 1.45; }
  .preset-badge {
    font-size: 9px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    color: var(--text);
    flex-shrink: 0;
    display: none;
    border: 1px solid rgba(255,255,255,0.1);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .preset-card.added .preset-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .preset-chevron {
    color: var(--text3);
    font-size: 16px;
    flex-shrink: 0;
    line-height: 1;
    transition: color 0.15s, transform 0.15s;
  }
  .preset-card:hover .preset-chevron { color: var(--text2); transform: translateX(2px); }

  /* ── Advanced panel fields ───────────────────── */
  .field { display: flex; flex-direction: column; gap: 6px; }
  .field.full { grid-column: 1 / -1; }
  label { font-size: 11px; color: var(--text2); font-weight: 500; padding-left: 2px; letter-spacing: 0.01em; }

  input[type=text], select {
    background: var(--card);
    border: 0.5px solid var(--sep);
    border-radius: 10px;
    color: var(--text);
    padding: 9px 12px;
    font-size: 13px;
    font-family: inherit;
    width: 100%;
    outline: none;
    transition: border-color 0.18s, background 0.18s;
    appearance: none;
    -webkit-appearance: none;
    -webkit-font-smoothing: antialiased;
  }
  input[type=text]::placeholder { color: var(--text3); }
  input[type=text]:focus, select:focus {
    border-color: rgba(255,255,255,0.35);
    background: var(--card2);
  }
  select {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'%3E%3Cpath fill='rgba(235,235,245,0.3)' d='M5 7L1 3h8z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 11px center;
    padding-right: 30px;
    cursor: pointer;
  }
  select option { background: #1c1c1e; }

  /* ── Score slider ────────────────────────────── */
  .slider-row { display: flex; align-items: center; gap: 12px; }
  input[type=range] {
    flex: 1;
    -webkit-appearance: none;
    height: 3px;
    border-radius: 2px;
    background: var(--fill);
    outline: none;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px; height: 18px;
    border-radius: 50%;
    background: #ffffff;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.5);
    transition: transform 0.1s ease;
  }
  input[type=range]::-webkit-slider-thumb:hover { transform: scale(1.1); }
  .slider-val { font-size: 12px; font-weight: 500; color: var(--text2); min-width: 32px; text-align: right; }

  /* ── Catalogs pane ───────────────────────────── */
  #catalogs-pane { display: flex; flex-direction: row; min-height: 0; flex: 1; overflow: hidden; }
  .catalogs-list-col {
    flex: 1; min-width: 0; overflow-y: auto;
    padding: 20px 24px 24px;
    display: flex; flex-direction: column; gap: 10px;
  }
  .catalogs-side-col {
    flex: 0 0 340px; border-left: 1px solid var(--sep);
    padding: 12px 16px; display: flex; flex-direction: column; gap: 0;
    min-height: 0;
    overflow: hidden;
    --install-qr-size: 180px;
    background: linear-gradient(180deg, rgba(14,14,16,0.96), rgba(8,8,9,0.98));
  }
  .catalogs-side-col.compact {
    padding-top: 10px;
    padding-bottom: 10px;
    --install-qr-size: 148px;
  }
  .catalogs-side-col.compact .side-module { margin-bottom: 8px; }
  .catalogs-side-col.compact .qr-wrap { padding: 8px; }
  .catalogs-side-col.compact .qr-sub { font-size: 9px; line-height: 1.28; }
  .catalogs-side-col.compact .url-text { max-height: 54px; }
  .catalogs-side-col .divider { margin: 6px 0; }
  .side-module {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 10px;
    flex-shrink: 0;
  }
  .side-module:last-child { margin-bottom: 0; }
  .side-module.tight { gap: 5px; }
  .side-or {
    text-align: center;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: var(--text4);
    text-transform: uppercase;
    margin: 0 0 7px;
  }
  .import-row { display: flex; gap: 8px; }
  .import-row input { flex: 1; font-size: 12px; padding: 8px 11px; border-radius: 8px; }
  #import-feedback {
    font-size: 11px;
    margin-top: 6px;
    display: none;
    line-height: 1.6;
    color: var(--text2);
  }
  #import-feedback.visible { display: block; }
  #import-feedback.ok { color: var(--text2); }
  #import-feedback.err { color: #e85d04; }
  .recipe-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .recipe-mini-note { font-size: 10px; color: var(--text3); line-height: 1.45; }
  .recipe-modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.62);
    backdrop-filter: blur(14px);
    z-index: 200;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  .recipe-modal-overlay.open { display: flex; }
  .recipe-modal {
    width: min(720px, calc(100vw - 40px));
    max-height: min(780px, calc(100vh - 40px));
    overflow: hidden;
    background: rgba(20,21,24,0.98);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    box-shadow: var(--shadow-lg);
    display: flex;
    flex-direction: column;
  }
  .recipe-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 18px;
    border-bottom: 1px solid var(--sep);
  }
  .recipe-modal-title { font-size: 14px; font-weight: 800; color: var(--text); letter-spacing: -0.02em; }
  .recipe-modal-close {
    border: none; background: transparent; color: var(--text3);
    cursor: pointer; padding: 4px 8px; border-radius: 6px;
  }
  .recipe-modal-close:hover { color: var(--text); background: var(--fill); }
  .recipe-modal-body { padding: 18px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; }
  .recipe-form-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
  .recipe-label { font-size: 10px; font-weight: 800; color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; }
  .recipe-input, .recipe-textarea {
    background: var(--card);
    border: 1px solid var(--sep);
    border-radius: 8px;
    color: var(--text);
    font: inherit;
    font-size: 12px;
    padding: 9px 11px;
    outline: none;
  }
  .recipe-textarea { resize: vertical; min-height: 68px; line-height: 1.45; }
  .recipe-input:focus, .recipe-textarea:focus { border-color: rgba(255,255,255,0.34); background: var(--card2); }
  .recipe-summary {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .recipe-summary-title { font-size: 18px; font-weight: 800; color: var(--text); letter-spacing: -0.04em; }
  .recipe-summary-desc { font-size: 12px; color: var(--text2); line-height: 1.45; }
  .recipe-chip-row { display: flex; flex-wrap: wrap; gap: 6px; }
  .recipe-chip {
    font-size: 10px; font-weight: 800; color: var(--text2);
    padding: 4px 8px; border-radius: 10px;
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08);
    letter-spacing: 0.03em;
  }
  .recipe-list { display: flex; flex-direction: column; gap: 8px; }
  .recipe-list-item {
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    padding: 10px 11px; border-radius: 8px;
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
  }
  .recipe-list-copy { min-width: 0; flex: 1; }
  .recipe-list-name { font-size: 12px; font-weight: 700; color: var(--text); }
  .recipe-list-meta { font-size: 10px; color: var(--text3); margin-top: 3px; text-transform: uppercase; letter-spacing: 0.06em; }
  .recipe-list-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
  .recipe-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .recipe-section-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }
  .recipe-section-title {
    font-size: 11px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .recipe-section-sub {
    font-size: 11px;
    color: var(--text3);
    line-height: 1.45;
  }
  .recipe-preview-panel {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding-top: 14px;
    border-top: 1px solid rgba(255,255,255,0.08);
  }
  .recipe-preview-toolbar {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }
  .recipe-preview-select-wrap {
    min-width: min(260px, 100%);
  }
  .recipe-preview-select {
    min-width: 220px;
  }
  .recipe-preview-selected {
    font-size: 12px;
    font-weight: 700;
    color: var(--text2);
  }
  .recipe-preview-feedback {
    min-height: 16px;
    font-size: 11px;
    color: var(--text3);
    line-height: 1.45;
  }
  .recipe-preview-feedback.ok { color: var(--text); }
  .recipe-preview-feedback.err { color: #fca5a5; }
  .recipe-inline-preview {
    display: block;
    border-top: none;
    padding-top: 0;
  }
  .recipe-inline-preview .smart-preview-empty {
    min-height: 126px;
  }
  .recipe-gallery { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
  .recipe-card {
    display: flex; flex-direction: column; gap: 9px; min-height: 148px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px; padding: 12px;
  }
  .recipe-card-title { font-size: 14px; font-weight: 800; color: var(--text); letter-spacing: -0.03em; }
  .recipe-card-desc { font-size: 11px; color: var(--text2); line-height: 1.45; flex: 1; }
  .recipe-card-actions { display: flex; gap: 8px; }
  .recipe-empty { font-size: 12px; color: var(--text2); line-height: 1.5; }
  .recipe-feedback { font-size: 11px; color: var(--text2); line-height: 1.5; min-height: 16px; }
  .recipe-feedback.ok { color: var(--text); }
  .recipe-feedback.err { color: #fca5a5; }
  .recipe-modal-footer {
    display: flex; align-items: center; justify-content: flex-end; gap: 10px;
    padding: 14px 18px; border-top: 1px solid var(--sep);
  }
  .smart-modal-overlay {
    display: none; position: fixed; inset: 0; z-index: 1000;
    background: rgba(0,0,0,0.72); backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    align-items: center; justify-content: center;
  }
  .smart-modal-overlay.open { display: flex; }
  .smart-modal {
    width: 760px; max-width: calc(100vw - 32px); max-height: calc(100vh - 36px);
    background: var(--card); border: 1px solid var(--sep);
    border-radius: 8px; box-shadow: 0 24px 70px rgba(0,0,0,0.75);
    display: flex; flex-direction: column; overflow: hidden;
  }
  .smart-modal-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 18px; border-bottom: 1px solid var(--sep);
  }
  .smart-modal-title { font-size: 14px; font-weight: 800; color: var(--text); }
  .smart-modal-close {
    background: none; border: none; color: var(--text3); cursor: pointer;
    font-size: 16px; padding: 2px 6px; border-radius: 6px; font-family: inherit;
  }
  .smart-modal-close:hover { color: var(--text); background: var(--fill); }
  .smart-modal-body { padding: 18px; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; }
  .smart-locked {
    border: 1px solid rgba(248,113,113,0.18); background: rgba(248,113,113,0.07);
    border-radius: 8px; padding: 14px; font-size: 12px; color: var(--text2); line-height: 1.5;
  }
  .smart-template-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
  .smart-template {
    min-height: 86px; text-align: left; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.045); color: var(--text); padding: 10px;
    cursor: pointer; font-family: inherit; display: flex; flex-direction: column; gap: 5px;
  }
  .smart-template.active { border-color: rgba(255,255,255,0.28); background: rgba(255,255,255,0.09); }
  .smart-template strong { font-size: 12px; }
  .smart-template span { font-size: 10px; color: var(--text3); line-height: 1.35; }
  .smart-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .smart-field-full { grid-column: 1 / -1; }
  .smart-label { display: flex; flex-direction: column; gap: 6px; font-size: 10px; font-weight: 800; color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; }
  .smart-input, .smart-select {
    height: 36px; border-radius: 6px; padding: 0 10px; font-size: 12px;
    border: 1px solid rgba(255,255,255,0.09); background: var(--card2);
    color: var(--text); font-family: inherit;
  }
  .smart-format-row { display: flex; flex-wrap: wrap; gap: 7px; }
  .smart-check {
    display: inline-flex; align-items: center; gap: 5px; height: 28px; padding: 0 9px;
    border-radius: 999px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    color: var(--text2); font-size: 11px; font-weight: 700; letter-spacing: 0; text-transform: none;
  }
  .smart-check input { margin: 0; }
  .smart-preview-feedback { min-height: 16px; font-size: 11px; color: var(--text3); line-height: 1.45; }
  .smart-preview-feedback.ok { color: var(--text); }
  .smart-preview-feedback.err { color: #fca5a5; }
  .smart-inline-preview {
    display: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 14px;
    min-height: 0;
  }
  .smart-inline-preview.visible {
    display: block;
  }
  .smart-preview-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 10px;
  }
  .smart-preview-title {
    font-size: 11px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .smart-preview-count {
    font-size: 10px;
    color: var(--text3);
    white-space: nowrap;
  }
  .smart-preview-strip {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 118px;
    gap: 10px;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 2px 2px 10px;
    overscroll-behavior-x: contain;
    scrollbar-width: thin;
  }
  .smart-preview-card {
    display: block;
    color: var(--text);
    text-decoration: none;
    min-width: 0;
  }
  .smart-preview-poster {
    width: 100%;
    aspect-ratio: 2 / 3;
    border-radius: 7px;
    overflow: hidden;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.09);
  }
  .smart-preview-poster img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
  }
  .smart-preview-name {
    margin-top: 7px;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.25;
    color: var(--text2);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .smart-preview-empty {
    min-height: 104px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 8px;
    color: var(--text3);
    font-size: 12px;
    text-align: center;
    padding: 14px;
  }
  .smart-modal-footer {
    display: flex; align-items: center; justify-content: flex-end; gap: 10px;
    padding: 14px 18px; border-top: 1px solid var(--sep);
  }

  /* ── Buttons ─────────────────────────────────── */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 10px 16px;
    border-radius: 6px;
    border: 1px solid transparent;
    font-size: 13px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: opacity 0.15s, transform 0.1s ease, background 0.15s, border-color 0.15s, color 0.15s;
    white-space: nowrap;
    letter-spacing: -0.02em;
    -webkit-font-smoothing: antialiased;
  }
  .btn:hover  { opacity: 0.78; }
  .btn:active { transform: scale(0.97); opacity: 1; }
  .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
  .btn-primary { background: #e7e7e7; color: #000000; box-shadow: none; }
  .btn-ghost   { background: rgba(255,255,255,0.05); color: var(--text); border-color: rgba(255,255,255,0.07); }
  .btn-danger  { background: rgba(220,38,38,0.12); color: #fca5a5; border-color: rgba(248,113,113,0.15); }
  .btn-sm  { padding: 6px 11px; font-size: 11px; }
  .btn-full { width: 100%; }

  /* ── Panel headings ──────────────────────────── */
  .panel-title { font-size: 14px; font-weight: 700; color: var(--text); letter-spacing: -0.03em; }
  .panel-sub   { font-size: 12px; color: var(--text2); margin-top: 4px; line-height: 1.5; }

  /* ── Catalog list — spaced cards ────────────── */
  .catalog-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  /* ── Subtle scrollbars ───────────────────────── */
  .left-panel::-webkit-scrollbar,
  #preview-pane::-webkit-scrollbar { width: 3px; }
  .left-panel::-webkit-scrollbar-track,
  #preview-pane::-webkit-scrollbar-track { background: transparent; }
  .left-panel::-webkit-scrollbar-thumb,
  #preview-pane::-webkit-scrollbar-thumb {
    background: rgba(84,84,88,0.28);
    border-radius: 2px;
  }
  .left-panel::-webkit-scrollbar-thumb:hover,
  #preview-pane::-webkit-scrollbar-thumb:hover { background: rgba(84,84,88,0.50); }
  .catalog-item {
    background: rgba(23,23,26,0.98);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 16px 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: background 0.18s ease, transform 0.12s ease, box-shadow 0.12s ease, border-color 0.18s ease;
    position: relative;
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    isolation: isolate;
  }
  .catalog-item::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background:
      radial-gradient(circle at 14% 18%, rgba(255,255,255,0.12), transparent 44%),
      linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0));
    opacity: 0;
    transition: opacity 0.18s ease;
    pointer-events: none;
    z-index: -1;
  }
  .catalog-item:hover { background: rgba(30,31,35,0.98); border-color: rgba(255,255,255,0.12); box-shadow: var(--shadow-md); }
  .catalog-item.active-preview {
    background: rgba(32,33,37,0.98);
    border-color: rgba(255,255,255,0.14);
    box-shadow: inset 3px 0 0 rgba(255,255,255,0.22), var(--shadow-md);
  }
  .catalog-item.smart-auth-missing {
    opacity: 0.46;
    cursor: not-allowed;
  }
  .catalog-item.smart-auth-missing:hover,
  .catalog-item.smart-auth-missing:focus-within {
    opacity: 0.58;
  }
  .catalog-item.smart-key-missing {
    border-color: rgba(220,38,38,0.48);
    box-shadow: inset 0 0 0 1px rgba(220,38,38,0.10), var(--shadow-sm);
  }
  .catalog-item.smart-key-missing:hover,
  .catalog-item.smart-key-missing:focus-within {
    border-color: rgba(220,38,38,0.72);
  }
  .catalog-item.smart-key-missing.active-preview {
    border-color: rgba(220,38,38,0.68);
    box-shadow: inset 3px 0 0 rgba(220,38,38,0.44), var(--shadow-md);
  }
  .catalog-item.dragging { opacity: 0.35; }
  .catalog-item .drag-handle { color: var(--text3); cursor: grab; font-size: 13px; flex-shrink: 0; line-height: 1; }
  .catalog-item .drag-handle:active { cursor: grabbing; }
  .catalog-item-info { flex: 1; min-width: 0; }
  .catalog-item-name { font-size: 14px; font-weight: 700; letter-spacing: -0.03em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .catalog-item-type { font-size: 11px; color: var(--text3); margin-top: 4px; }
  .catalog-rename-input {
    font-size: 14px; font-weight: 600; letter-spacing: -0.03em;
    background: rgba(255,255,255,0.06); border: 1px solid rgba(235,235,245,0.24);
    border-radius: 12px; color: var(--text);
    padding: 8px 10px; width: 100%; outline: none;
  }
  .catalog-rename-input:focus { border-color: rgba(235,235,245,0.6); }
  .catalog-type-badge {
    font-size: 9px; font-weight: 700;
    padding: 3px 8px;
    border-radius: 10px;
    flex-shrink: 0;
    background: rgba(255,255,255,0.06); color: var(--text2);
    letter-spacing: 0.06em;
    border: 1px solid rgba(255,255,255,0.09);
    text-transform: uppercase;
  }
  .catalog-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
  .remove-btn, .shuffle-btn, .edit-btn {
    display: flex; align-items: center; gap: 5px;
    padding: 8px 12px; border-radius: 12px; border: 1px solid transparent;
    font-size: 11px; font-weight: 600; font-family: inherit;
    cursor: pointer; flex-shrink: 0;
    transition: background 0.15s, color 0.15s, opacity 0.15s, transform 0.15s, border-color 0.15s;
  }
  .edit-btn   { background: rgba(255,255,255,0.06); color: var(--text2); border-color: rgba(255,255,255,0.08); }
  .shuffle-btn { background: rgba(255,255,255,0.06); color: var(--text2); border-color: rgba(255,255,255,0.08); }
  .remove-btn { background: rgba(220,38,38,0.14); color: #fca5a5; border-color: rgba(248,113,113,0.14); }
  .edit-btn:hover   { background: rgba(255,255,255,0.1); color: var(--text); transform: translateY(-1px); }
  .shuffle-btn:hover { background: rgba(255,255,255,0.1); color: var(--text); transform: translateY(-1px); }
  .shuffle-btn.active {
    background: linear-gradient(180deg, rgba(245,246,247,0.2) 0%, rgba(245,246,247,0.14) 100%);
    color: var(--text);
    border-color: rgba(245,246,247,0.38);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.18), 0 0 0 1px rgba(255,255,255,0.08);
  }
  .remove-btn:hover { background: rgba(220,38,38,0.24); color: #fecaca; transform: translateY(-1px); }
  .catalog-num {
    flex-shrink: 0; width: 34px; height: 34px;
    border-radius: 4px; background: rgba(255,255,255,0.1);
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 800; color: rgba(255,255,255,0.98);
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
  }
  .catalog-count-badge {
    font-size: 11px; font-weight: 600; color: var(--text2);
    background: rgba(255,255,255,0.05); border-radius: 10px;
    padding: 6px 12px; flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.08);
  }

  /* ── Empty state ─────────────────────────────── */
  .empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text3);
    font-size: 13px;
    text-align: center;
    gap: 10px;
    padding: 32px;
    background: rgba(22,22,25,0.96);
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
  }
  .empty-icon { font-size: 28px; opacity: 0.35; }

  /* ── URL output ──────────────────────────────── */
  .btn-stremio {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; padding: 9px 12px; border-radius: 16px; border: 1px solid transparent;
    background: #e7e7e7; color: #0a0a0a;
    font-size: 12px; font-weight: 700; font-family: inherit;
    cursor: pointer; letter-spacing: -0.1px;
    transition: opacity 0.15s, transform 0.1s, background 0.15s, box-shadow 0.15s;
    -webkit-font-smoothing: antialiased;
    box-shadow: none;
  }
  .btn-stremio:hover  { transform: translateY(-1px); }
  .btn-stremio:active { transform: scale(0.97); }
  .url-alt-label { font-size: 11px; color: var(--text3); margin: 12px 0 8px; line-height: 1.6; }
  .qr-localhost-notice { font-size: 11px; color: var(--text3); text-align: center; line-height: 1.5; margin-top: 4px; }
  .url-box {
    background: rgba(22,22,25,0.98);
    border-radius: 8px;
    padding: 11px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shadow-sm);
  }
  .url-box-row { display: flex; align-items: flex-start; gap: 8px; }
  .url-text {
    font-family: 'Mona Sans VF', 'Mona Sans', 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-size: 10px; color: var(--text2);
    word-break: break-all; line-height: 1.65;
    max-height: 68px; overflow-y: auto;
    margin-bottom: 8px; cursor: text; user-select: all;
    scrollbar-width: thin; scrollbar-color: var(--sep) transparent;
    padding: 8px 10px;
    border-radius: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
  }
  .url-text::-webkit-scrollbar { width: 4px; }
  .url-text::-webkit-scrollbar-track { background: transparent; }
  .url-text::-webkit-scrollbar-thumb { background: var(--sep); border-radius: 2px; }
  .copy-icon-btn {
    flex-shrink: 0; background: var(--fill2); border: none; cursor: pointer;
    color: var(--text2); padding: 5px 10px; border-radius: 7px;
    font-size: 12px; font-weight: 500; font-family: inherit;
    display: flex; align-items: center; gap: 4px;
    transition: color 0.15s, background 0.15s;
    white-space: nowrap;
  }
  .copy-icon-btn:hover { color: var(--text); background: var(--fill); }
  .copy-row { display: flex; gap: 6px; }
  .qr-section { margin-top: 0; }
  .qr-wrap {
    background: rgba(22,22,25,0.98); border-radius: 8px; padding: 10px;
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shadow-sm);
  }
  #qr-canvas-wrap {
    width: min(var(--install-qr-size), 100%);
    max-width: 100%;
    margin: 2px auto;
    flex-shrink: 0;
  }
  #qr-canvas-wrap canvas,
  #qr-canvas-wrap img { border-radius: 8px; display: block; max-width: 100%; height: auto; }
  .qr-sub { font-size: 10px; color: var(--text3); text-align: center; line-height: 1.35; }
  .important-note {
    padding: 10px 12px;
    border: 0.5px solid var(--sep); border-radius: var(--radius);
    font-size: 11px; color: var(--text3); line-height: 1.6;
    background: var(--fill2);
  }
  .important-note strong { color: var(--text2); }

  /* ── Divider ─────────────────────────────────── */
  .divider { border: none; border-top: 1px solid var(--sep); margin: 24px 0; }

  /* ── Drag-over lift ─────────────────────────── */
  .catalog-item.drag-over {
    transform: translateX(10px) translateY(-5px) scale(1.02);
    background: rgba(38,39,45,0.99) !important;
    border-color: rgba(255,255,255,0.2);
    box-shadow: 0 18px 34px rgba(0,0,0,0.36), 0 0 0 1px rgba(255,255,255,0.05);
    z-index: 2;
    border-radius: var(--radius) !important;
  }
  .catalog-item.drag-over::before { opacity: 1; }
  .catalog-item.drag-over .catalog-num {
    transform: scale(1.08);
    border-color: rgba(255,255,255,0.2);
    box-shadow: 0 10px 18px rgba(0,0,0,0.26), inset 0 1px 0 rgba(255,255,255,0.12);
  }
  .catalog-item.drag-over .catalog-item-name { color: #fff; }
  .catalog-item.shift-down { transform: translateY(14px) scale(0.985); }
  .catalog-item.shift-up { transform: translateY(-14px) scale(0.985); }

  /* ── Auth header section ─────────────────────────── */
  .header-auth { margin-left: 0; display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
  .btn-connect {
    display: flex; align-items: center; gap: 6px;
    padding: 9px 16px; border-radius: var(--pill); border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.045); color: var(--text2);
    font-size: 12px; font-weight: 600; font-family: inherit;
    cursor: pointer; text-decoration: none;
    transition: background 0.15s, color 0.15s, border-color 0.15s, transform 0.15s, box-shadow 0.15s;
  }
  .auth-connect-icon { opacity: 0.7; }
  .btn-connect:hover { background: rgba(255,255,255,0.08); color: var(--text); border-color: rgba(255,255,255,0.18); transform: translateY(-1px); box-shadow: var(--shadow-sm); }
  .auth-connected {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 8px 6px 6px;
    border-radius: var(--pill);
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
  }
  .auth-avatar { width: 30px; height: 30px; border-radius: 50%; border: 1.5px solid rgba(255,255,255,0.1); object-fit: cover; flex-shrink: 0; }
  .auth-name { font-size: 12px; color: var(--text); font-weight: 600; }
  .btn-disconnect {
    padding: 6px 12px; border-radius: var(--pill); border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04); color: var(--text3); font-size: 11px; font-family: inherit;
    cursor: pointer; transition: color 0.15s, border-color 0.15s, background 0.15s;
  }
  .btn-disconnect:hover { color: #f87171; border-color: rgba(248,113,113,0.4); background: rgba(248,113,113,0.08); }

  /* ── Error / auth banners ────────────────────────── */
  .error-banner {
    display: none; padding: 10px 28px; flex-shrink: 0;
    background: rgba(220,38,38,0.12); border-bottom: 0.5px solid rgba(220,38,38,0.35);
    font-size: 12px; color: #f87171; font-weight: 500;
  }
  .error-banner.visible { display: block; }
  .url-warn-icon {
    display: none; position: relative; cursor: help;
    color: #fbbf24; padding: 4px 2px; flex-shrink: 0;
    align-items: center; font-size: 13px; line-height: 1;
  }
  .url-warn-icon.show { display: flex; }
  .url-warn-tooltip {
    display: none; position: absolute; bottom: calc(100% + 8px); right: 0;
    width: 210px; background: #1c1c1e; color: #fbbf24;
    font-size: 11px; padding: 8px 10px; border-radius: 8px;
    border: 0.5px solid rgba(234,179,8,0.4);
    pointer-events: none; z-index: 100; line-height: 1.5;
  }
  .url-warn-icon:hover .url-warn-tooltip { display: block; }

  /* ── Account preset pills ────────────────────────── */
  .preset-card.account-locked { opacity: 0.42; cursor: not-allowed; pointer-events: none; }
  .account-badge {
    font-size: 9px; font-weight: 700; padding: 3px 8px;
    border-radius: 10px; flex-shrink: 0;
    background: rgba(255,255,255,0.06); color: var(--text2);
    letter-spacing: 0.08em;
    border: 1px solid rgba(255,255,255,0.08);
    text-transform: uppercase;
  }
  .account-badge.account-source-badge {
    background: rgba(232,93,4,0.12);
    color: #f48c06;
    border-color: rgba(232,93,4,0.3);
  }
  .account-badge.ai-badge {
    background: rgba(139,92,246,0.12);
    color: #a78bfa;
    border-color: rgba(139,92,246,0.3);
  }
  .preset-card.ai-preset-card {
    padding-top: 18px;
  }
  .preset-card.ai-preset-card .preset-info {
    padding-right: 8px;
  }
  .ai-preset-corner-icon {
    position: absolute;
    top: 12px;
    right: 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    opacity: 0.92;
  }
  .ai-preset-corner-icon .ai-star-icon {
    width: 15px;
    height: 15px;
  }
  .ai-preset-actions {
    margin-left: auto;
    gap: 12px;
  }
  .ai-preset-actions .preset-chevron { margin-left: 2px; }

  /* ── AI Recommendations pill ─────────────────────── */
  .preset-card.ai-no-key { border: 0.5px solid rgba(220,38,38,0.45) !important; }
  .preset-card.ai-no-key:hover { border-color: rgba(220,38,38,0.7) !important; }
  .ai-gear-btn {
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px; border-radius: 50%; flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.05); color: var(--text3);
    cursor: pointer; font-size: 12px; line-height: 1;
    opacity: 0; visibility: hidden; pointer-events: none;
    transform: scale(0.92);
    transition: background 0.15s, color 0.15s, opacity 0.15s, transform 0.15s, visibility 0.15s;
  }
  .preset-card:not(.account-locked):hover .ai-gear-btn,
  .preset-card:not(.account-locked):focus-within .ai-gear-btn {
    opacity: 1; visibility: visible; pointer-events: auto; transform: scale(1);
  }
  .ai-gear-btn:hover { background: rgba(255,255,255,0.1); color: var(--text); }
  .ai-connected-tag {
    font-size: 9px; font-weight: 700; padding: 3px 8px;
    border-radius: 10px; flex-shrink: 0;
    background: rgba(34,197,94,0.10); color: #22c55e;
    letter-spacing: 0.08em; border: 1px solid rgba(34,197,94,0.3);
    text-transform: uppercase;
  }

  /* ── AI Settings Modal ───────────────────────────── */
  .ai-modal-overlay {
    display: none; position: fixed; inset: 0; z-index: 1000;
    background: rgba(0,0,0,0.72); backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    align-items: center; justify-content: center;
  }
  .ai-modal-overlay.open { display: flex; }
  .ai-modal {
    background: var(--card); border-radius: var(--radius-lg);
    border: 0.5px solid var(--sep);
    box-shadow: 0 24px 64px rgba(0,0,0,0.75);
    width: 420px; max-width: calc(100vw - 32px);
  }
  .ai-modal-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 20px 14px; border-bottom: 0.5px solid var(--sep);
  }
  .ai-modal-title { font-size: 14px; font-weight: 600; }
  .ai-modal-close {
    background: none; border: none; color: var(--text3); cursor: pointer;
    font-size: 16px; padding: 2px 6px; border-radius: 6px; font-family: inherit;
    transition: color 0.15s, background 0.15s;
  }
  .ai-modal-close:hover { color: var(--text); background: var(--fill); }
  .ai-modal-body { padding: 18px 20px; display: flex; flex-direction: column; gap: 16px; }
  .ai-modal-section { display: flex; flex-direction: column; gap: 6px; }
  .ai-modal-label {
    font-size: 10px; font-weight: 600; color: var(--text3);
    letter-spacing: 0.06em; text-transform: uppercase;
  }
  .ai-modal-select, .ai-modal-input {
    height: 34px; border-radius: 8px; padding: 0 12px;
    font-size: 12px; background: var(--card2);
    border: 0.5px solid var(--sep); color: var(--text);
    font-family: inherit; width: 100%;
    transition: border-color 0.15s, background 0.15s;
  }
  .ai-modal-select { cursor: pointer; padding: 0 10px; }
  #ai-model-custom { display: none; margin-top: 6px; }
  #ai-model-custom.visible { display: block; }
  .ai-modal-input::placeholder { color: var(--text3); }
  .ai-modal-input:focus, .ai-modal-select:focus {
    outline: none; border-color: rgba(255,255,255,0.25); background: #2c2c2e;
  }
  .ai-key-row { display: flex; gap: 8px; align-items: flex-start; }
  .ai-key-row .ai-modal-input { flex: 1; }
  .ai-test-btn {
    height: 34px; padding: 0 14px; border-radius: 8px; flex-shrink: 0;
    font-size: 12px; font-family: inherit; font-weight: 500; cursor: pointer;
    background: var(--fill); border: 0.5px solid var(--sep); color: var(--text2);
    transition: background 0.15s, border-color 0.15s, color 0.15s;
  }
  .ai-test-btn:hover { background: var(--card2); border-color: rgba(255,255,255,0.18); color: var(--text); }
  .ai-test-btn:disabled { opacity: 0.45; cursor: not-allowed; }
  .ai-key-feedback { font-size: 11px; min-height: 14px; margin-top: 2px; }
  .ai-key-feedback.ok  { color: #22c55e; }
  .ai-key-feedback.err { color: #f87171; }
  .ai-key-hint { font-size: 10px; color: var(--text3); }
  .ai-modal-footer {
    display: flex; justify-content: flex-end; gap: 8px;
    padding: 14px 20px; border-top: 0.5px solid var(--sep);
  }
  .ai-modal-cancel {
    height: 32px; padding: 0 16px; border-radius: 20px; font-size: 12px;
    font-family: inherit; cursor: pointer;
    background: none; border: 0.5px solid var(--sep); color: var(--text2);
    transition: background 0.15s, color 0.15s;
  }
  .ai-modal-cancel:hover { background: var(--fill); color: var(--text); }
  .ai-modal-save {
    height: 32px; padding: 0 18px; border-radius: 20px; font-size: 12px;
    font-family: inherit; font-weight: 500; cursor: pointer;
    background: #ffffff; border: none; color: #000000;
    transition: opacity 0.15s;
  }
  .preview-error-detail {
    font-size: 11px;
    color: var(--text3);
    margin-top: 6px;
  }
  .search-prototype-preview {
    margin: 18px 28px 26px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.025);
    box-shadow: 0 18px 36px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.04);
    overflow: hidden;
  }
  .search-prototype-hero {
    display: grid;
    grid-template-columns: 156px minmax(0, 1fr);
    gap: 18px;
    padding: 22px;
    align-items: start;
  }
  .search-prototype-poster {
    width: 156px;
    aspect-ratio: 2/3;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.05);
    box-shadow: 0 20px 34px rgba(0,0,0,0.3);
  }
  .search-prototype-poster img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
  }
  .search-prototype-copy { min-width: 0; display: flex; flex-direction: column; gap: 10px; }
  .search-prototype-topline {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
  }
  .search-prototype-mode,
  .search-prototype-local,
  .search-prototype-base {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 9px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: rgba(255,255,255,0.05);
    color: var(--text2);
    border: 1px solid rgba(255,255,255,0.08);
  }
  .search-prototype-mode {
    background: rgba(255,255,255,0.05);
  }
  .search-prototype-mode.smart {
    background: rgba(255,255,255,0.05);
    color: var(--text2);
    border-color: rgba(255,255,255,0.08);
  }
  .search-prototype-mode.metadata {
    background: rgba(255,255,255,0.05);
    color: var(--text2);
    border-color: rgba(255,255,255,0.08);
  }
  .search-prototype-local {
    background: rgba(255,255,255,0.05);
    color: var(--text3);
    border-color: rgba(255,255,255,0.08);
  }
  .search-prototype-base {
    color: var(--text3);
    text-transform: none;
    letter-spacing: 0;
    font-weight: 700;
  }
  .search-prototype-title {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: #fff;
    line-height: 1.05;
  }
  .search-prototype-row-name {
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: 11px 13px;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
  }
  .search-prototype-row-name strong {
    font-size: 10px;
    font-weight: 800;
    color: var(--text3);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .search-prototype-row-name span {
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
  }
  .search-prototype-meta-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }
  .search-prototype-block {
    padding: 13px 14px;
    border-radius: 16px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.06);
  }
  .search-prototype-block strong {
    display: block;
    font-size: 10px;
    font-weight: 800;
    color: var(--text3);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .search-prototype-chip-row { display: flex; flex-wrap: wrap; gap: 7px; }
  .search-prototype-chip {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    color: var(--text2);
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
  }
  .search-prototype-note {
    font-size: 12px;
    color: var(--text2);
    line-height: 1.6;
  }
  .search-prototype-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 0 22px 22px;
  }
  .search-prototype-actions .btn {
    min-width: 140px;
    justify-content: center;
  }
  .ai-modal-save:hover { opacity: 0.85; }
  .ai-modal-save:disabled { opacity: 0.4; cursor: not-allowed; }
  .prototype-install-note {
    display: none;
    font-size: 11px;
    line-height: 1.5;
    color: #fbbf24;
    padding: 10px 11px;
    border-radius: 10px;
    border: 1px solid rgba(251,191,36,0.22);
    background: rgba(251,191,36,0.08);
  }
  .prototype-install-note.visible { display: block; }
  .search-modal-overlay {
    position: fixed;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
    z-index: 1100;
    background: rgba(0,0,0,0.66);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
  .search-modal-overlay.open { display: flex; }
  .search-modal {
    width: min(680px, calc(100vw - 36px));
    max-height: min(760px, calc(100vh - 36px));
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: rgba(20,21,24,0.98);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    box-shadow: 0 28px 62px rgba(0,0,0,0.48);
  }
  .search-modal-header,
  .search-modal-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 16px 18px;
    border-bottom: 1px solid var(--sep);
  }
  .search-modal-footer {
    justify-content: flex-end;
    border-bottom: none;
    border-top: 1px solid var(--sep);
  }
  .search-modal-title {
    font-size: 15px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.03em;
  }
  .search-modal-sub {
    margin-top: 4px;
    font-size: 11px;
    color: var(--text3);
  }
  .search-modal-close {
    border: none;
    background: transparent;
    color: var(--text3);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 8px;
    font-family: inherit;
  }
  .search-modal-close:hover { color: var(--text); background: var(--fill); }
  .search-modal-body {
    padding: 18px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .search-modal-note,
  .search-modal-empty {
    font-size: 12px;
    line-height: 1.6;
    color: var(--text2);
    padding: 13px 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.045);
  }
  .search-modal-list { display: flex; flex-direction: column; gap: 9px; }
  .search-modal-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 12px 13px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
  }
  .search-modal-item-copy { min-width: 0; }
  .search-modal-item-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .search-modal-item-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 5px;
    font-size: 10px;
    color: var(--text3);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .search-modal-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: flex-end;
    flex-shrink: 0;
  }
  .search-modal-btn {
    height: 32px;
    padding: 0 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.04);
    color: var(--text2);
    font-size: 11px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
  }
  .search-modal-btn:hover {
    background: rgba(255,255,255,0.08);
    color: var(--text);
    border-color: rgba(255,255,255,0.16);
  }
  .search-modal-btn.overwrite:hover {
    color: #fca5a5;
    border-color: rgba(248,113,113,0.28);
    background: rgba(248,113,113,0.08);
  }

  @media (max-width: 1024px) {
    main { grid-template-columns: 326px 1fr; }
    .catalogs-side-col { flex-basis: 316px; }
    .preview-grid { grid-template-columns: repeat(auto-fill, minmax(188px, 1fr)); }
    .poster { width: 188px; }
    .detail-grid { grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); }
    .header-search {
      flex-basis: 540px;
      max-width: 760px;
      min-width: 260px;
      margin: 0 auto;
    }
  }
  @media (max-width: 768px) {
    main { grid-template-columns: 1fr; }
    .mid-panel { border-top: 1px solid var(--sep); }
    header { padding: 14px 20px; flex-wrap: wrap; align-items: flex-start; }
    .header-sub { display: none; }
    .header-search {
      order: 3;
      flex: 1 0 100%;
      min-width: 0;
      max-width: none;
      margin: 12px 0 0;
    }
    .header-search-row { flex-direction: column; align-items: stretch; }
    .search-mode-switch { align-self: flex-start; }
    .header-auth { margin-left: auto; margin-top: 10px; }
    .filter-bar,
    .options-panel,
    .pane-tabbar,
    .preview-grid,
    .detail-grid,
    .preview-list,
    .pane-footer,
    .catalogs-list-col,
    .catalogs-side-col { padding-left: 18px; padding-right: 18px; }
    #catalogs-pane { flex-direction: column; }
    .catalogs-side-col {
      flex: 0 0 auto;
      border-left: none;
      border-top: 1px solid var(--sep);
      overflow: visible;
      --install-qr-size: 180px;
    }
    .detail-grid { grid-template-columns: 1fr; }
    .detail-card { height: auto; min-height: 270px; }
    .preview-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px; }
    .poster { width: 100%; }
    .list-item { grid-template-columns: 44px 1fr; gap: 14px; }
    .list-score, .list-meta-col { display: none; }
    .pane-tab-extras { justify-content: flex-start; }
    .view-controls { width: 100%; justify-content: space-between; flex-wrap: wrap; }
    .poster-style-picker { order: 3; width: 100%; overflow-x: auto; }
    .poster-style-btn { flex: 1 0 auto; }
    .catalog-recipe-bar { align-items: stretch; flex-direction: column; }
    .smart-row-bar { align-items: stretch; flex-direction: column; }
    .smart-row-actions { flex-wrap: wrap; }
    .smart-template-grid, .smart-form-grid { grid-template-columns: 1fr; }
    .recipe-gallery { grid-template-columns: 1fr; }
    .recipe-modal-footer { flex-wrap: wrap; }
    .search-prototype-preview { margin-left: 18px; margin-right: 18px; }
    .search-prototype-hero { grid-template-columns: 1fr; }
    .search-prototype-poster { width: 152px; }
    .search-prototype-meta-grid { grid-template-columns: 1fr; }
    .search-modal-item { flex-direction: column; align-items: stretch; }
    .search-modal-actions { justify-content: stretch; }
    .search-modal-btn { flex: 1; }
  }
  @media (max-height: 880px) and (min-width: 769px) {
    .catalogs-side-col { --install-qr-size: 156px; }
    .qr-wrap { padding: 9px; }
    .url-text { max-height: 60px; }
  }
  @media (max-height: 760px) and (min-width: 769px) {
    .catalogs-side-col {
      padding-top: 10px;
      padding-bottom: 10px;
      --install-qr-size: 132px;
    }
    .side-module { margin-bottom: 8px; }
    .side-or { margin-bottom: 5px; }
    .qr-wrap { padding: 8px; }
    .qr-sub { font-size: 9px; line-height: 1.28; }
    .url-text { max-height: 52px; }
  }
</style>
<script src="/static/qrcode.min.js"></script>
</head>
<body>
<div class="app">
  <header>
    <div class="brand">
      <div class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" role="img" focusable="false" aria-hidden="true">
          <path fill="#02A9FF" d="M15.533 15.51V5.725c0-.561-.31-.87-.871-.87h-1.915c-.562 0-.871.309-.871.87v4.646c0 .131 1.261.739 1.294.868.961 3.754.209 6.758-.702 6.898 1.489.074 1.652.79.543.3.17-2.003.832-1.999 2.735-.073.016.016.39.8.414.8h4.496c.561 0 .871-.309.871-.87v-1.914c0-.562-.31-.871-.871-.871h-5.123Z"></path>
          <path fill="#FFFFFF" d="M8.071 4.855 3.04 19.164h3.908l.852-2.475h4.257l.832 2.475h3.889L11.766 4.855H8.071Zm.619 8.664 1.22-3.963 1.336 3.963H8.69Z"></path>
        </svg>
      </div>
      <h1>AniList Catalogs</h1>
    </div>
    <span class="header-sub">Configure</span>
    <div class="header-search" id="header-search">
      <div class="header-search-shell">
        <div class="header-search-row">
          <div class="header-search-input-wrap">
            <svg class="header-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="7"></circle>
              <line x1="20" y1="20" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" id="header-search-input" placeholder="Search anime to build a catalog..." autocomplete="off" spellcheck="false">
          </div>
          <div class="search-mode-switch" role="group" aria-label="Search mode">
            <button class="search-mode-btn active" type="button" id="search-mode-metadata" data-action="set-search-mode" data-mode="metadata">Basic</button>
            <button class="search-mode-btn locked" type="button" id="search-mode-smart" data-action="set-search-mode" data-mode="smart">Smart</button>
          </div>
        </div>
        <div class="search-smart-hint visible" id="search-smart-hint">Connect AniList + OpenRouter to unlock Smart search</div>
        <div class="header-search-dropdown" id="header-search-dropdown"></div>
      </div>
    </div>
    <div class="header-auth" id="header-auth"></div>
  </header>

  <div class="error-banner" id="error-banner"></div>

  <main>
    <!-- LEFT: Quick Add presets + Install URL + Import -->
    <div class="left-panel">
      <div class="left-panel-content">
      <section>
        <div class="section-title">Quick Add</div>
        <div class="presets-grid" id="quick-add-grid">
          <div class="preset-card" id="preset-anilist-popular-season" data-action="add-preset" data-id="anilist-popular-season" data-name="Popular This Season">
            <div class="preset-info">
              <div class="preset-name">Popular This Season</div>
              <div class="preset-desc">Top anime airing right now</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card" id="preset-anilist-airing-week" data-action="add-preset" data-id="anilist-airing-week" data-name="Airing This Week">
            <div class="preset-info">
              <div class="preset-name">Airing This Week</div>
              <div class="preset-desc">New episodes this week</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card" id="preset-anilist-trending" data-action="add-preset" data-id="anilist-trending" data-name="Trending Now">
            <div class="preset-info">
              <div class="preset-name">Trending Now</div>
              <div class="preset-desc">What everyone's watching</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card" id="preset-anilist-top-rated" data-action="add-preset" data-id="anilist-top-rated" data-name="Top Rated All Time">
            <div class="preset-info">
              <div class="preset-name">Top Rated All Time</div>
              <div class="preset-desc">Highest scored anime ever</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
        </div>
      </section>

      <hr class="divider">

      <section>
        <div class="section-title">AniList Profile Catalogs</div>
        <div class="presets-grid" id="account-presets-grid">
          <div class="preset-card account-locked" id="preset-anilist-watching-current" data-action="add-account-preset" data-id="anilist-watching-current" data-name="Currently Watching" data-status="CURRENT">
            <div class="preset-info"><div class="preset-name">Currently Watching</div><div class="preset-desc">Anime you're actively watching</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-planning" data-action="add-account-preset" data-id="anilist-watching-planning" data-name="Plan to Watch" data-status="PLANNING">
            <div class="preset-info"><div class="preset-name">Plan to Watch</div><div class="preset-desc">Your watch list</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-completed" data-action="add-account-preset" data-id="anilist-watching-completed" data-name="Completed" data-status="COMPLETED">
            <div class="preset-info"><div class="preset-name">Completed</div><div class="preset-desc">Anime you've finished</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-paused" data-action="add-account-preset" data-id="anilist-watching-paused" data-name="Paused" data-status="PAUSED">
            <div class="preset-info"><div class="preset-name">Paused</div><div class="preset-desc">On hold</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-dropped" data-action="add-account-preset" data-id="anilist-watching-dropped" data-name="Dropped" data-status="DROPPED">
            <div class="preset-info"><div class="preset-name">Dropped</div><div class="preset-desc">Anime you've stopped watching</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-repeating" data-action="add-account-preset" data-id="anilist-watching-repeating" data-name="Rewatching" data-status="REPEATING">
            <div class="preset-info"><div class="preset-name">Rewatching</div><div class="preset-desc">Currently rewatching</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-favourites" data-action="add-account-preset" data-id="anilist-favourites" data-name="My Favourites" data-status="FAVOURITES">
            <div class="preset-info"><div class="preset-name">My Favourites</div><div class="preset-desc">Your starred anime</div></div>
            <span class="account-badge account-source-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
        </div>
      </section>
      </div><!-- end .left-panel-content -->
      <div class="left-panel-footer">
        <div class="pane-footer-icons">
          <a class="pane-footer-icon" href="https://github.com/juuzocyber/anilist-catalogs" target="_blank" rel="noopener noreferrer" title="GitHub">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
          </a>
          <a class="pane-footer-icon" href="#" title="Buy me a coffee">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.89 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z"/></svg>
          </a>
        </div>
        <div class="pane-footer-text">Version: v1.6.0 &mdash; Developed by juuzo</div>
      </div>
    </div>

    <!-- MID: Filters + Preview + Catalogs -->
    <div class="mid-panel">

      <!-- Filter bar -->
      <div class="filter-bar">
        <select id="f-year" class="select-hidden">
          <option value="">Year</option>
          <option value="2027">2027</option>
<option value="2026">2026</option>
<option value="2025">2025</option>
<option value="2024">2024</option>
<option value="2023">2023</option>
<option value="2022">2022</option>
<option value="2021">2021</option>
<option value="2020">2020</option>
<option value="2019">2019</option>
<option value="2018">2018</option>
<option value="2017">2017</option>
<option value="2016">2016</option>
<option value="2015">2015</option>
<option value="2014">2014</option>
<option value="2013">2013</option>
<option value="2012">2012</option>
<option value="2011">2011</option>
<option value="2010">2010</option>
<option value="2009">2009</option>
<option value="2008">2008</option>
<option value="2007">2007</option>
<option value="2006">2006</option>
<option value="2005">2005</option>
<option value="2004">2004</option>
<option value="2003">2003</option>
<option value="2002">2002</option>
<option value="2001">2001</option>
<option value="2000">2000</option>
<option value="1999">1999</option>
<option value="1998">1998</option>
<option value="1997">1997</option>
<option value="1996">1996</option>
<option value="1995">1995</option>
<option value="1994">1994</option>
<option value="1993">1993</option>
<option value="1992">1992</option>
<option value="1991">1991</option>
<option value="1990">1990</option>
<option value="1989">1989</option>
<option value="1988">1988</option>
<option value="1987">1987</option>
<option value="1986">1986</option>
<option value="1985">1985</option>
<option value="1984">1984</option>
<option value="1983">1983</option>
<option value="1982">1982</option>
<option value="1981">1981</option>
<option value="1980">1980</option>
        </select>
        <div class="year-dropdown" id="year-dropdown">
          <button class="fb-filter-btn" id="btn-year" type="button" data-action="toggle-year-menu">
            <span id="lbl-year">Year</span>
            <span class="fb-chevron">&#9660;</span>
          </button>
          <div class="year-menu" id="year-menu">
            <button class="year-menu-item" type="button" data-action="set-year-value" data-value="">Any</button>
          </div>
        </div>
        <select id="f-daterange" class="select-hidden">
          <option value="">Date Range</option>
          <option value="this-week">This Week</option>
          <option value="this-month">This Month</option>
          <option value="last-month">Last Month</option>
          <option value="this-year">This Year</option>
          <option value="last-year">Last Year</option>
        </select>
        <button class="fb-filter-btn" id="btn-daterange" data-action="set-active-filter" data-filter="daterange">
          <span id="lbl-daterange">Date Range</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-season" class="select-hidden">
          <option value="">Season</option>
          <option value="CURRENT">Current Season</option>
          <option value="WINTER">Winter</option>
          <option value="SPRING">Spring</option>
          <option value="SUMMER">Summer</option>
          <option value="FALL">Fall</option>
        </select>
        <button class="fb-filter-btn" id="btn-season" data-action="set-active-filter" data-filter="season">
          <span id="lbl-season">Season</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-status" class="select-hidden">
          <option value="">Status</option>
          <option value="RELEASING">Airing</option>
          <option value="FINISHED">Finished</option>
          <option value="NOT_YET_RELEASED">Upcoming</option>
        </select>
        <button class="fb-filter-btn" id="btn-status" data-action="set-active-filter" data-filter="status">
          <span id="lbl-status">Status</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-format" class="select-hidden">
          <option value="">Format</option>
          <option value="TV">TV Series</option>
          <option value="TV_SHORT">TV Short</option>
          <option value="MOVIE">Movie</option>
          <option value="OVA">OVA</option>
          <option value="ONA">ONA</option>
          <option value="SPECIAL">Special</option>
        </select>
        <button class="fb-filter-btn" id="btn-format" data-action="set-active-filter" data-filter="format">
          <span id="lbl-format">Format</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <button class="fb-filter-btn" id="btn-genres" data-action="set-active-filter" data-filter="genres">
          <span id="lbl-genres">Genres</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-sort" class="select-hidden">
          <option value="POPULARITY_DESC">Popularity</option>
          <option value="TRENDING_DESC">Trending</option>
          <option value="SCORE_DESC">Score</option>
          <option value="START_DATE_DESC">Newest</option>
          <option value="FAVOURITES_DESC">Favourites</option>
        </select>
        <div class="fb-sep"></div>
        <div class="fb-slider-wrap">
          <span class="fb-slider-label">Score</span>
          <input type="range" id="f-score" min="0" max="90" step="10" value="0">
          <span class="fb-slider-val" id="score-val">Any</span>
        </div>
        <label class="fb-adult-toggle" id="adult-toggle">
          <input type="checkbox" id="f-adult">
          Adult
        </label>
        <div class="fb-sep"></div>
        <div class="fb-name-wrap" id="catalog-name-wrap">
          <input class="fb-name-input" type="text" id="catalog-name" placeholder="Catalog Name">
          <div id="catalog-name-error">Name required</div>
        </div>
        <button class="fb-add-btn" id="catalog-add-btn" data-action="add-custom">Add</button>
      </div>

      <!-- Always-visible options panel -->
      <div class="options-panel" id="options-panel">
        <div class="filter-opts-pills" id="filter-opts-pills"></div>
      </div>

      <!-- Pane tab bar: Preview / Catalogs switch -->
      <div class="pane-tabbar">
        <div class="pane-tabbar-left">
          <div class="pane-tabs">
            <button class="pane-tab active" id="tab-preview" data-action="set-pane-tab" data-pane="preview">Preview</button>
            <button class="pane-tab" id="tab-catalogs" data-action="set-pane-tab" data-pane="catalogs">Your Catalogs</button>
          </div>
          <div class="filter-tags-wrap">
            <svg class="tags-icon" width="13" height="13" viewBox="0 0 16 16" fill="currentColor">
              <path d="M2 2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 0 1.414l-4.586 4.586a1 1 0 0 1-1.414 0L2.293 8.293A1 1 0 0 1 2 7.586V2zm3 3.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>
            </svg>
            <div class="filter-tags" id="filter-tags"></div>
          </div>
        </div>
        <div class="pane-tab-extras" id="preview-tab-extras">
          <span class="panel-sub-inline" id="preview-sub">Set filters or click a catalog to preview</span>
          <div class="view-controls">
            <div class="sort-dropdown" id="sort-dropdown">
              <button class="sort-btn" id="sort-btn" data-action="toggle-sort-menu">
                <svg class="sort-icon-dim" width="11" height="11" viewBox="0 0 12 12" fill="currentColor"><path d="M3 2v8M3 10l-2-2M3 10l2-2M9 10V2M9 2L7 4M9 2l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/></svg>
                <span class="sort-btn-label" id="sort-btn-label">Popularity</span>
                <span class="sort-btn-chevron">&#9660;</span>
              </button>
              <div class="sort-menu" id="sort-menu">
                <button class="sort-menu-item active" data-action="set-sort-value" data-value="POPULARITY_DESC">Popularity</button>
                <button class="sort-menu-item" data-action="set-sort-value" data-value="TRENDING_DESC">Trending</button>
                <button class="sort-menu-item" data-action="set-sort-value" data-value="SCORE_DESC">Average Score</button>
                <button class="sort-menu-item" data-action="set-sort-value" data-value="START_DATE_DESC">Newest</button>
                <button class="sort-menu-item" data-action="set-sort-value" data-value="FAVOURITES_DESC">Favorites</button>
              </div>
            </div>
            <span class="view-sep">|</span>
            <div class="poster-style-picker" id="poster-style-picker" role="group" aria-label="Poster style">
              <button class="poster-style-btn active" type="button" data-action="set-poster-style" data-style="off" title="Standard posters">Off</button>
              <button class="poster-style-btn" type="button" data-action="set-poster-style" data-style="clean" title="Both Rank and Rating poster overlays">Both</button>
              <button class="poster-style-btn" type="button" data-action="set-poster-style" data-style="rank" title="Top rank banner posters">Rank</button>
              <button class="poster-style-btn" type="button" data-action="set-poster-style" data-style="rating" title="Bottom genre and rating banner posters">Rating</button>
            </div>
            <span class="view-sep">|</span>
            <div class="view-toggle">
              <button class="view-btn active" id="view-btn-grid" data-action="set-view" data-view="grid" title="Grid view">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><rect x="0" y="0" width="6" height="6" rx="1.5"/><rect x="8" y="0" width="6" height="6" rx="1.5"/><rect x="0" y="8" width="6" height="6" rx="1.5"/><rect x="8" y="8" width="6" height="6" rx="1.5"/></svg>
              </button>
              <button class="view-btn" id="view-btn-detail" data-action="set-view" data-view="detail" title="Detail view">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><rect x="0" y="0" width="5" height="6" rx="1"/><rect x="7" y="0" width="7" height="2" rx="0.75"/><rect x="7" y="3" width="5" height="1.5" rx="0.5"/><rect x="7" y="5" width="6" height="1" rx="0.5"/><rect x="0" y="8" width="5" height="6" rx="1"/><rect x="7" y="8" width="7" height="2" rx="0.75"/><rect x="7" y="11" width="5" height="1.5" rx="0.5"/><rect x="7" y="13" width="6" height="1" rx="0.5"/></svg>
              </button>
              <button class="view-btn" id="view-btn-list" data-action="set-view" data-view="list" title="List view">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><rect x="0" y="0" width="5" height="5" rx="1.5"/><rect x="7" y="1" width="7" height="1.5" rx="0.75"/><rect x="7" y="3.5" width="5" height="1" rx="0.5"/><rect x="0" y="7" width="5" height="5" rx="1.5"/><rect x="7" y="8" width="7" height="1.5" rx="0.75"/><rect x="7" y="10.5" width="5" height="1" rx="0.5"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Preview pane -->
      <div id="preview-pane">
        <div id="preview-area">
          <div class="preview-prompt">
            <div class="preview-prompt-icon">&#127916;</div>
            <div>Set filters or click a catalog<br>to preview matching titles</div>
          </div>
        </div>
      </div>

      <!-- Catalogs pane (hidden by default) -->
      <div id="catalogs-pane" class="catalogs-hidden">
        <div class="catalogs-list-col">
          <div class="catalog-recipe-bar">
            <div class="catalog-recipe-copy">
              <div class="catalog-recipe-title">Recipes</div>
              <div class="catalog-recipe-sub">Share and import public catalog bundles without account or AI auth keys.</div>
            </div>
            <div class="recipe-actions">
              <button class="btn btn-ghost btn-sm" data-action="open-share-recipe">Share Recipe</button>
              <button class="btn btn-ghost btn-sm" data-action="browse-recipes">Browse Recipes</button>
            </div>
          </div>
          <div class="smart-row-bar" id="smart-row-bar">
            <div class="catalog-recipe-copy">
              <div class="catalog-recipe-title">Smart Rows</div>
              <div class="catalog-recipe-sub">Build seed-based AI catalogs from a title, your 10/10s, or completed hidden gems.</div>
            </div>
            <div class="smart-row-actions">
              <div class="smart-settings-wrap">
                <button class="smart-settings-btn" data-action="open-ai-modal" title="OpenRouter settings" aria-label="OpenRouter settings">&#9881;</button>
                <div class="smart-row-note" id="smart-row-note"></div>
              </div>
              <button class="btn btn-primary btn-sm" data-action="open-smart-builder">Build Catalog</button>
            </div>
          </div>
          <div class="catalog-meta-row">
            <div class="panel-sub-inline">Drag to reorder &middot; click to preview</div>
            <span class="catalog-count-badge hidden" id="catalog-count-badge"></span>
          </div>
          <div class="catalog-list" id="catalog-list"></div>
        </div>
        <div class="catalogs-side-col">
          <div class="side-module tight">
            <div class="section-title">Install AniList Catalogs</div>
            <button class="btn-stremio" id="open-stremio-btn" data-action="open-stremio">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>
              Add to Stremio
            </button>
            <div class="prototype-install-note" id="prototype-install-note">Search prototype rows are not included in this install URL yet.</div>
          </div>
          <div class="side-or">OR</div>
          <div class="side-module">
            <div class="url-box">
              <div class="url-text" id="url-display">—</div>
              <div class="copy-row">
                <button class="btn btn-ghost btn-sm btn-full" id="copy-url-btn" data-action="copy-url">Copy URL</button>
                <div class="url-warn-icon" id="token-warning">
                  &#9888;
                  <div class="url-warn-tooltip">This URL contains a private auth key for your AniList account. Keep it private and do not share it. It stays valid until you disconnect AniList.</div>
                </div>
              </div>
            </div>
          </div>

          <div class="side-or">OR</div>
          <div class="side-module qr-section qr-section-tight">
            <div class="qr-wrap">
              <div class="qr-sub">Scan this QR code with your mobile device</div>
              <div id="qr-canvas-wrap"></div>
              <div class="qr-sub">The QR code contains the Stremio URL for your addon. Scan it with your smartphone to install in the Stremio mobile app.</div>
            </div>
          </div>

          <div class="stack-end">
            <hr class="divider divider-tight">
            <div class="side-module tight">
              <div class="section-title">Import Config</div>
              <div class="import-row">
                <input type="text" id="import-url" placeholder="Paste manifest or recipe URL...">
                <button class="btn btn-primary btn-sm" id="import-btn" data-action="import-config">Import</button>
              </div>
              <div id="import-feedback"></div>
            </div>
          </div>
        </div>
      </div>

    </div>

  </main>
</div>

<script nonce="__CSP_NONCE__">
const GENRES = ["Action","Adventure","Comedy","Drama","Ecchi","Fantasy","Horror","Mahou Shoujo","Mecha","Music","Mystery","Psychological","Romance","Sci-Fi","Slice of Life","Sports","Supernatural","Thriller"];
const BASE_URL = window.location.origin;
const ANILIST_MARK = '<span class="al-logo-badge" aria-hidden="true"><svg viewBox="0 0 24 24" role="img" focusable="false" aria-hidden="true"><path fill="#02A9FF" d="M15.533 15.51V5.725c0-.561-.31-.87-.871-.87h-1.915c-.562 0-.871.309-.871.87v4.646c0 .131 1.261.739 1.294.868.961 3.754.209 6.758-.702 6.898 1.489.074 1.652.79.543.3.17-2.003.832-1.999 2.735-.073.016.016.39.8.414.8h4.496c.561 0 .871-.309.871-.87v-1.914c0-.562-.31-.871-.871-.871h-5.123Z"></path><path fill="#FFFFFF" d="M8.071 4.855 3.04 19.164h3.908l.852-2.475h4.257l.832 2.475h3.889L11.766 4.855H8.071Zm.619 8.664 1.22-3.963 1.336 3.963H8.69Z"></path></svg></span>';
const POSTER_LAB_VERSION = 'v9';
const POSTER_STYLE_DEFAULT = 'clean';
const POSTER_STYLES = new Set(['off', 'clean', 'rank', 'rating']);
const POSTER_LAB_SEASONAL_STATUSES = new Set(['RELEASING', 'NOT_YET_RELEASED']);
const POSTER_LAB_RETURNING_RELATIONS = new Set(['PREQUEL']);
const POSTER_LAB_SPINOFF_RELATIONS = new Set(['PARENT']);
const POSTER_LAB_SOURCE_LABELS = {
  MANGA: 'Manga Adaptation',
  LIGHT_NOVEL: 'LN Adaptation',
  VIDEO_GAME: 'Game Adaptation',
};
const POSTER_LAB_ORIGINAL_SOURCE = 'ORIGINAL';
const POSTER_LAB_ANIME_SOURCE = 'ANIME';
const POSTER_LAB_MOVIE_PREMIERE_DAYS = 45;
const POSTER_LAB_RECENT_ADAPTATION_DAYS = 90;
const POSTER_LAB_AIRS_THIS_WEEK_SECONDS = 7 * 24 * 60 * 60;
const POSTER_LAB_TRENDING_TOP_N = 10;
const POSTER_LAB_TOP_RANK_PRIORITY_LIMIT = 100;

const GENRE_COLORS = {
  'Action':'#e85d04','Adventure':'#f48c06','Comedy':'#a7c957','Drama':'#4895ef',
  'Ecchi':'#f72585','Fantasy':'#7b2fbe','Horror':'#9b2226','Mahou Shoujo':'#f48fb1',
  'Mecha':'#4361ee','Music':'#c77dff','Mystery':'#0077b6','Psychological':'#bc6c25',
  'Romance':'#e63946','Sci-Fi':'#48cae4','Slice of Life':'#52b788',
  'Sports':'#2dc653','Supernatural':'#9d4edd','Thriller':'#d62828',
};
const THEME_KEYS = [
  'orange','gold','lime','blue','pink','purple','red','cyan','green',
  'violet','sky','amber','coral','mint','rose','ocean','indigo','magenta'
];
const STUDIO_THEMES = {
  'MAPPA':'orange','Ufotable':'purple','Kyoto Animation':'blue',
  'Wit Studio':'green','MADHOUSE':'cyan','Bones':'gold',
  'Toei Animation':'red','A-1 Pictures':'indigo','CloverWorks':'pink',
  'David Production':'amber','Trigger':'rose','J.C.Staff':'sky',
  'Shaft':'violet','Production I.G':'ocean','P.A. Works':'coral',
  'Doga Kobo':'lime','Studio KAI':'cyan','White Fox':'green',
  'Brains Base':'gold','Sunrise':'orange',
};
const PRESET_IDS = new Set([
  'anilist-popular-season','anilist-airing-week','anilist-trending','anilist-top-rated'
]);
const ACCOUNT_PRESET_IDS = new Set([
  'anilist-watching-current','anilist-watching-planning','anilist-watching-completed',
  'anilist-watching-paused','anilist-watching-dropped','anilist-watching-repeating',
  'anilist-favourites'
]);
const PRESET_DEFAULT_NAMES = {
  'anilist-popular-season': 'Popular This Season',
  'anilist-airing-week':    'Airing This Week',
  'anilist-trending':       'Trending Now',
  'anilist-top-rated':      'Top Rated All Time',
};
const SORT_LABELS = {
  POPULARITY_DESC:'Popularity', TRENDING_DESC:'Trending', SCORE_DESC:'Score',
  START_DATE_DESC:'Newest', FAVOURITES_DESC:'Favourites',
};
const FORMAT_LABELS = { TV:'TV Show', TV_SHORT:'TV Short', MOVIE:'Movie', OVA:'OVA', ONA:'ONA', SPECIAL:'Special' };
const SEASON_LABELS = { WINTER:'Winter', SPRING:'Spring', SUMMER:'Summer', FALL:'Fall' };
const STATUS_LABELS = { RELEASING:'Airing', FINISHED:'Finished', NOT_YET_RELEASED:'Upcoming', CANCELLED:'Cancelled' };
let currentView = 'grid';
let posterStyle = 'off';
let _posterLabTopLabelMap = new Map();

// ── Auth state ────────────────────────────────────
const _urlParams = new URLSearchParams(window.location.search);
const _hashParams = new URLSearchParams(window.location.hash.startsWith('#') ? window.location.hash.slice(1) : '');
// Auth key: a short token handed back by the OAuth callback.
// The actual encrypted AniList token lives server-side; only this key travels
// in the manifest URL (as "{config_token}~{session_key}").
let _sessionKey = _hashParams.get('s') || _urlParams.get('s') || null;
// OpenRouter state — populated from /api/me response on load.
let _hasOrKey = false;
let _orModel  = 'meta-llama/llama-3.3-70b-instruct';
const SMART_DEFAULTS = {
  title_seed: {
    label: 'More like a title',
    description: 'Use one anime as the main signal.',
    name: 'More like ',
    options: { formats: [], minScore: 70, popularityBias: 'balanced' },
  },
  top_rated: {
    label: 'More like my 10/10s',
    description: 'Use your highest-rated completed anime.',
    name: 'More like my 10/10s',
    options: { formats: [], minScore: 70, popularityBias: 'balanced' },
  },
  hidden_completed: {
    label: 'Hidden gems from completed',
    description: 'Find less obvious picks from your completed taste.',
    name: 'Hidden gems from Completed',
    options: { formats: [], minScore: 70, popularityBias: 'hidden' },
  },
};
let smartBuilderMode = 'title_seed';
let smartBuilderPreviewCatalog = null;
let smartBuilderPreviewMedia = [];
const SEARCH_MIN_CHARS = 3;
const SEARCH_RESULT_LIMIT = 8;
const SEARCH_DEBOUNCE_MS = 300;
let searchMode = 'metadata';
let searchQuery = '';
let searchResults = [];
let searchLoading = false;
let searchOpen = false;
let searchActiveIndex = -1;
let searchLookupToken = 0;
let searchLookupTimer = null;
let searchAbortController = null;
let activePrototypePreview = null;
let searchModalDraft = null;
// Clean the ?s= handoff param from the configure page URL immediately — it
// doesn't belong in the browser history and the key is now held in memory.
if (_sessionKey) {
  const _cleanUrl = new URL(window.location.href);
  _cleanUrl.searchParams.delete('s');
  _cleanUrl.hash = '';
  window.history.replaceState({}, '', _cleanUrl.toString());
}

// ── Pre-login catalog preservation ───────────────
// When the user clicks "Connect AniList", the page navigates away and back.
// We save the current catalogs to localStorage before leaving so they can be
// restored on return (identified by the presence of the ?s= auth key).
const _PENDING_CATALOGS_KEY = 'anilist_catalogs_pending';
let _pendingCatalogs = null;
if (_sessionKey) {
  try {
    const saved = localStorage.getItem(_PENDING_CATALOGS_KEY);
    if (saved) {
      _pendingCatalogs = JSON.parse(saved);
      localStorage.removeItem(_PENDING_CATALOGS_KEY);
    }
  } catch(e) { /* ignore storage errors */ }
}

let catalogs = _pendingCatalogs || [];

// ── Source tag state ──────────────────────────────
// activeSource: { id, name, listStatus?, type:'watching'|'ai' } | null
// Clicking an account/AI pill sets this, shows a tag in the filter bar, and
// fetches the source content. Additional filters apply client-side on top.
let activeSource = null;
let _sourceMedia = null;       // raw media array fetched for the active source
let _lastSuggestedName = '';   // tracks the last auto-generated catalog name suggestion

let selectedGenres = [];
let selectedFormats  = [];
let selectedStatuses = [];
let selectedYears    = [];
let selectedSeasons  = [];
let includeAdult     = false;

// ── Helpers ───────────────────────────────────────
function getCurrentSeason() {
  const m = new Date().getMonth() + 1;
  if (m <= 3) return 'WINTER';
  if (m <= 6) return 'SPRING';
  if (m <= 9) return 'SUMMER';
  return 'FALL';
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function cloneJson(value) {
  return value == null ? value : JSON.parse(JSON.stringify(value));
}

function freshCatalogId(prefix = 'custom') {
  return `${prefix}-` + Math.random().toString(36).slice(2, 10);
}

function compactMediaRef(ref) {
  if (!ref || typeof ref !== 'object') return null;
  const id = parseInt(ref.id, 10) || 0;
  const title = String(ref.title || '').trim();
  if (!id && !title) return null;
  const entry = {};
  if (id > 0) entry.i = id;
  if (title) entry.t = title.slice(0, 160);
  return Object.keys(entry).length ? entry : null;
}

function expandMediaRef(entry) {
  if (!entry || typeof entry !== 'object') return null;
  const id = parseInt(entry.i, 10) || 0;
  const title = String(entry.t || '').trim();
  if (!id && !title) return null;
  const ref = {};
  if (id > 0) ref.id = id;
  if (title) ref.title = title.slice(0, 160);
  return ref;
}

function sanitizeCatalogSnapshot(cat) {
  const snapshot = cloneJson(cat);
  if (!snapshot || typeof snapshot !== 'object') return null;
  delete snapshot.uiPrototype;
  delete snapshot.uiDraft;
  delete snapshot.uiPrototypeMode;
  delete snapshot.uiPrototypeLocalOnly;
  delete snapshot.uiPreviewOnly;
  delete snapshot.uiSelectedTitle;
  delete snapshot.uiBaseCatalogSnapshot;
  delete snapshot.uiDerivedMetadata;
  delete snapshot.uiCatalogDraft;
  return snapshot;
}

function catalogRequiresAuth(cat, depth = 0) {
  if (!cat || typeof cat !== 'object' || depth >= 5) return false;
  if (cat.type === 'watching' || cat.type === 'ai') return true;
  return catalogRequiresAuth(cat.baseCatalog, depth + 1);
}

function compactCatalogEntry(cat) {
  if (!cat || typeof cat !== 'object') return { i: '', n: '', f: {} };
  if (PRESET_IDS.has(cat.id)) {
    const entry = { i: cat.id };
    if (cat.name && cat.name !== PRESET_DEFAULT_NAMES[cat.id]) entry.n = cat.name;
    if (cat.randomize) entry.r = true;
    return entry;
  }
  if (cat.type === 'watching') {
    const entry = { i: cat.id, n: cat.name || cat.id, w: true };
    if (cat.listStatus) entry.s = cat.listStatus;
    if (cat.clientFilters && Object.keys(cat.clientFilters).length) entry.cf = cat.clientFilters;
    if (cat.sourceName) entry.sn = String(cat.sourceName).slice(0, 120);
    if (cat.randomize) entry.r = true;
    return entry;
  }
  if (cat.type === 'ai') {
    const entry = { i: cat.id, n: cat.name || cat.id, a: true };
    const defaultModel = 'meta-llama/llama-3.3-70b-instruct';
    if (cat.model && cat.model !== defaultModel) entry.m = cat.model;
    if (cat.aiMode) entry.am = cat.aiMode;
    if (cat.seedMediaId) entry.sid = cat.seedMediaId;
    if (cat.seedTitle) entry.st = cat.seedTitle;
    if (cat.smartOptions) entry.so = cat.smartOptions;
    if (cat.clientFilters && Object.keys(cat.clientFilters).length) entry.cf = cat.clientFilters;
    if (cat.sourceName) entry.sn = String(cat.sourceName).slice(0, 120);
    if (cat.randomize) entry.r = true;
    return entry;
  }
  const entry = { i: cat.id, n: cat.name || cat.id, f: cat.filters || {} };
  if (cat.clientFilters && Object.keys(cat.clientFilters).length) entry.cf = cat.clientFilters;
  if (cat.baseCatalog) entry.bc = compactCatalogEntry(cat.baseCatalog);
  if (Array.isArray(cat.includedMedia) && cat.includedMedia.length) {
    const included = cat.includedMedia.map(compactMediaRef).filter(Boolean);
    if (included.length) entry.im = included;
  }
  const seed = compactMediaRef(cat.searchSeed);
  if (seed) entry.ss = seed;
  if (cat.randomize) entry.r = true;
  return entry;
}

function expandCatalogEntry(entry) {
  if (!entry || typeof entry !== 'object') return null;
  const id = entry.i || '';
  if (PRESET_IDS.has(id)) {
    const cat = { id, name: entry.n || PRESET_DEFAULT_NAMES[id], type: 'preset' };
    if (entry.r) cat.randomize = true;
    return cat;
  }
  if (entry.w) {
    const cat = { id, name: entry.n || id, type: 'watching' };
    if (entry.s) cat.listStatus = entry.s;
    if (entry.cf && Object.keys(entry.cf).length) cat.clientFilters = entry.cf;
    if (entry.sn) cat.sourceName = entry.sn;
    if (entry.r) cat.randomize = true;
    return cat;
  }
  if (entry.a) {
    const cat = { id, name: entry.n || 'AI Recommendations', type: 'ai', model: entry.m || 'meta-llama/llama-3.3-70b-instruct' };
    if (entry.am) cat.aiMode = entry.am;
    if (entry.sid) cat.seedMediaId = entry.sid;
    if (entry.st) cat.seedTitle = entry.st;
    if (entry.so) cat.smartOptions = entry.so;
    if (entry.cf && Object.keys(entry.cf).length) cat.clientFilters = entry.cf;
    if (entry.sn) cat.sourceName = entry.sn;
    if (entry.r) cat.randomize = true;
    return cat;
  }
  const cat = { id, name: entry.n || id, type: 'custom', filters: entry.f || {} };
  if (entry.cf && Object.keys(entry.cf).length) cat.clientFilters = entry.cf;
  if (entry.bc) {
    const baseCatalog = expandCatalogEntry(entry.bc);
    if (baseCatalog) cat.baseCatalog = baseCatalog;
  }
  if (Array.isArray(entry.im) && entry.im.length) {
    const included = entry.im.map(expandMediaRef).filter(Boolean);
    if (included.length) cat.includedMedia = included;
  }
  if (entry.ss) {
    const seed = expandMediaRef(entry.ss);
    if (seed) cat.searchSeed = seed;
  }
  if (entry.r) cat.randomize = true;
  return cat;
}

function normalizePosterStyle(value, fallback = POSTER_STYLE_DEFAULT) {
  const style = String(value || '').toLowerCase();
  return POSTER_STYLES.has(style) ? style : fallback;
}

function posterStyleLabel(value) {
  const style = normalizePosterStyle(value);
  return {
    clean: 'Both',
    rank: 'Rank',
    rating: 'Rating',
  }[style] || 'Both';
}

function isPosterLabEnabled() {
  return posterStyle !== 'off';
}

function getSmartRequirementState() {
  const needsAniList = !_sessionKey;
  const needsOpenRouter = !_sessionKey || !_hasOrKey;
  let note = '';
  if (needsAniList && needsOpenRouter) note = 'Needs AniList login and OpenRouter key';
  else if (needsOpenRouter) note = 'Needs OpenRouter key';
  else if (needsAniList) note = 'Needs AniList login';
  return { needsAniList, needsOpenRouter, note };
}

function slugifyGenre(genre) {
  return String(genre || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function genreBadgeClass(genre, variant) {
  const prefix = variant === 'soft' ? 'genre-soft--' : 'genre--';
  return prefix + slugifyGenre(genre);
}

function studioThemeKey(studio) {
  if (studio && STUDIO_THEMES[studio]) return STUDIO_THEMES[studio];
  const key = String(studio || 'studio');
  let hash = 0;
  for (let i = 0; i < key.length; i++) hash = ((hash << 5) - hash + key.charCodeAt(i)) | 0;
  return THEME_KEYS[Math.abs(hash) % THEME_KEYS.length];
}

function studioThemeClass(studio) {
  return 'theme-' + studioThemeKey(studio);
}

function scoreClass(score) {
  if (!score) return 'score-none';
  if (score >= 80) return 'score-high';
  if (score >= 70) return 'score-mid';
  if (score >= 60) return 'score-low';
  return 'score-poor';
}

function detailScoreClass(score) {
  const cls = scoreClass(score);
  return 'detail-' + cls;
}

function detailBannerLineClass(title) {
  const titleLength = String(title || '').length;
  const titleLines = titleLength > 58 ? 4 : titleLength > 36 ? 3 : titleLength > 20 ? 2 : 1;
  return 'detail-banner-lines-' + titleLines;
}

function setHidden(el, hidden) {
  if (el) el.classList.toggle('hidden', hidden);
}

function setVisibleClass(el, className, visible) {
  if (el) el.classList.toggle(className, visible);
}

// ── Auth helpers ──────────────────────────────────
async function fetchMe() {
  if (!_sessionKey) { renderAuthUI(null); return; }
  try {
    const res = await fetch('/api/me', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session: _sessionKey }),
    });
    if (!res.ok) { _sessionKey = null; renderAuthUI(null); return; }
    const data = await res.json();
    _hasOrKey = data.has_or_key || false;
    _orModel  = data.or_model  || 'meta-llama/llama-3.3-70b-instruct';
    renderAuthUI(data);
  } catch(e) { _sessionKey = null; renderAuthUI(null); }
}

function renderAuthUI(user) {
  const el = document.getElementById('header-auth');
  if (!el) return;
  if (user) {
    el.innerHTML = '<div class="auth-connected">' +
      (user.avatar ? '<img class="auth-avatar" src="' + escHtml(user.avatar) + '" alt="">' : '') +
      '<span class="auth-name">' + escHtml(user.name) + '</span>' +
      '<button class="btn-disconnect" data-action="disconnect">Disconnect</button>' +
      '</div>';
  } else {
    el.innerHTML = '<a class="btn-connect" href="/oauth/login" data-action="save-config-before-login">' +
      '<svg class="auth-connect-icon" width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>' +
      'Connect AniList</a>';
  }
  updateAccountPills();
  updateSmartRowsStatus();
  render();
}

function updateAccountPills() {
  const locked = !_sessionKey;
  ACCOUNT_PRESET_IDS.forEach(id => {
    const card = document.getElementById('preset-' + id);
    if (card) {
      card.classList.toggle('account-locked', locked);
      card.classList.toggle('pointer-disabled', locked);
    }
  });
}

function updateSmartRowsStatus() {
  const bar = document.getElementById('smart-row-bar');
  const note = document.getElementById('smart-row-note');
  if (!bar && !note) return;
  const state = getSmartRequirementState();
  if (bar) {
    bar.classList.toggle('smart-auth-missing', state.needsAniList);
    bar.classList.toggle('smart-key-missing', state.needsOpenRouter);
    bar.classList.toggle('smart-has-note', !!state.note);
    bar.removeAttribute('title');
  }
  if (note) note.textContent = state.note;
}

function saveConfigBeforeLogin() {
  // Preserve the current catalog list across the OAuth redirect so the user's
  // custom catalogs and ordering survive the full-page navigation.
  try { localStorage.setItem(_PENDING_CATALOGS_KEY, JSON.stringify(catalogs)); } catch(e) {}
}

function disconnect() {
  // Tell the server to clear session + OR key caches, best-effort.
  if (_sessionKey) {
    fetch('/oauth/logout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session: _sessionKey }),
    }).catch(() => {});
  }
  _sessionKey = null;
  _hasOrKey   = false;
  _orModel    = 'meta-llama/llama-3.3-70b-instruct';
  // Clear source tag state if it was an account/AI source
  if (activeSource) {
    activeSource = null;
    _sourceMedia = null;
    _lastSuggestedName = '';
    renderFilterTags();
    updateNameInput();
  }
  catalogs = catalogs.filter(c => c.type !== 'watching' && c.type !== 'ai');
  renderAuthUI(null);
  render();
}

// ── Source filtering helpers ──────────────────────

// Returns true if any additional filter (genre/format/status/year/season/score/daterange)
// is active on top of the current source tag.
function freshPrototypeId() {
  return 'ui-prototype-' + Math.random().toString(36).slice(2, 10);
}

function isUiPrototype(cat) {
  return !!(cat && cat.uiPrototype);
}

function supportedCatalogs(sourceCatalogs = catalogs) {
  return sourceCatalogs.filter(cat => cat && !isUiPrototype(cat) && (_sessionKey || !catalogRequiresAuth(cat)));
}

function catalogTypeBadgeLabel(cat) {
  if (isUiPrototype(cat) || hasStoredClientFilters(cat)) return 'Custom';
  if (cat?.type === 'watching') return 'Account';
  if (cat?.type === 'ai') return 'AI';
  if (cat?.type === 'custom') return 'Custom';
  return 'Preset';
}

function catalogTypeBadgeClass(cat) {
  if (isUiPrototype(cat) || hasStoredClientFilters(cat)) return '';
  if (cat?.type === 'watching') return ' account-type-badge';
  if (cat?.type === 'ai') return ' ai-type-badge';
  return '';
}

function snapshotSearchItem(item) {
  return {
    id: item?.id || 0,
    title: item?.title || 'Selected Anime',
    coverImage: item?.coverImage || '',
    genres: [...(item?.genres || [])],
    format: item?.format || '',
    seasonYear: item?.seasonYear || null,
  };
}

function getResolvedSearchMode() {
  const state = getSmartRequirementState();
  if (searchMode === 'smart' && !state.needsAniList && !state.needsOpenRouter) return 'smart';
  return 'metadata';
}

function searchResultMetaText(item) {
  return [...(item.genres || []).slice(0, 2), FORMAT_LABELS[item.format] || item.format, item.seasonYear].filter(Boolean).join(' · ');
}

function buildSearchMetadataFilters(selected) {
  const filters = { sort: 'POPULARITY_DESC' };
  const genres = [...new Set((selected?.genres || []).filter(Boolean))].slice(0, 2);
  if (genres.length) filters.genres = genres;
  if (selected?.format) filters.formats = [selected.format];
  return filters;
}

function buildPrototypeCatalogDraft(item, mode = getResolvedSearchMode()) {
  const selected = item?.uiSelectedTitle ? snapshotSearchItem(item.uiSelectedTitle) : snapshotSearchItem(item);
  const safeMode = mode === 'smart' ? 'smart' : 'metadata';
  const title = selected.title || 'Selected Anime';
  const draftName = safeMode === 'smart' ? `More like ${title}` : `Inspired by ${title}`;
  const catalogDraft = safeMode === 'smart'
    ? {
        id: freshCatalogId('ai'),
        name: draftName,
        type: 'ai',
        model: _orModel || 'meta-llama/llama-3.3-70b-instruct',
        aiMode: 'title_seed',
        seedMediaId: selected.id || undefined,
        seedTitle: title,
        smartOptions: cloneJson(SMART_DEFAULTS.title_seed.options),
      }
    : {
        id: freshCatalogId('custom'),
        name: draftName,
        type: 'custom',
        filters: buildSearchMetadataFilters(selected),
        searchSeed: { id: selected.id || undefined, title },
      };
  return {
    id: freshPrototypeId(),
    name: draftName,
    uiDraft: true,
    uiPrototypeMode: safeMode,
    uiSelectedTitle: selected,
    uiBaseCatalogSnapshot: null,
    uiDerivedMetadata: {
      genres: [...((catalogDraft.filters?.genres) || selected.genres || [])],
      format: (catalogDraft.filters?.formats?.[0]) || selected.format || '',
      seasonYear: (catalogDraft.filters?.years?.[0]) || selected.seasonYear || null,
    },
    uiCatalogDraft: catalogDraft,
  };
}

function buildInjectedCatalogFromSearch(baseCatalog, item, { preserveName = false } = {}) {
  const selected = item?.uiSelectedTitle ? snapshotSearchItem(item.uiSelectedTitle) : snapshotSearchItem(item);
  const baseSnapshot = sanitizeCatalogSnapshot(baseCatalog);
  const title = selected.title || 'Selected Anime';
  return {
    id: preserveName ? (baseSnapshot?.id || freshCatalogId('custom')) : freshCatalogId('custom'),
    name: preserveName ? (baseCatalog?.name || title) : `${baseCatalog?.name || 'Catalog'} + ${title}`,
    type: 'custom',
    baseCatalog: baseSnapshot,
    includedMedia: [{ id: selected.id || 0, title }],
    randomize: !!baseCatalog?.randomize,
  };
}

function getPrototypeTags(prototype) {
  const tags = [];
  if (prototype?.uiBaseCatalogSnapshot?.name) tags.push({ label: prototype.uiBaseCatalogSnapshot.name });
  if (prototype?.uiSelectedTitle?.title) {
    tags.push({
      label: prototype.uiSelectedTitle.title,
      key: prototype?.uiDraft && prototype?.uiPrototypeMode === 'metadata' ? 'prototype-title' : '',
    });
  }
  return tags;
}

function renderDefaultPreviewPrompt() {
  document.getElementById('preview-sub').textContent = 'Set filters or click a catalog to preview';
  document.getElementById('preview-area').innerHTML = '<div class="preview-prompt"><div class="preview-prompt-icon">&#127916;</div><div>Set filters or click a catalog<br>to preview matching titles</div></div>';
}

function renderSearchPrototypePreview(prototype) {
  const area = document.getElementById('preview-area');
  const selected = prototype?.uiSelectedTitle || {};
  const title = escHtml(selected.title || 'Selected Anime');
  const poster = escHtml(selected.coverImage || '');
  const mode = prototype?.uiPrototypeMode === 'smart' ? 'smart' : 'metadata';
  const modeLabel = mode === 'smart' ? 'Smart Seed Draft' : 'Basic Draft';
  const modeNote = mode === 'smart'
    ? 'This preview only shows the future seed-based row shell. AI recommendation logic is not connected yet.'
    : 'This preview only shows the future metadata-based row shell. Genre and format matching are not connected yet.';
  const baseName = prototype?.uiBaseCatalogSnapshot?.name ? escHtml(prototype.uiBaseCatalogSnapshot.name) : '';
  const chips = [...(prototype?.uiDerivedMetadata?.genres || []), prototype?.uiDerivedMetadata?.format ? (FORMAT_LABELS[prototype.uiDerivedMetadata.format] || prototype.uiDerivedMetadata.format) : '']
    .filter(Boolean)
    .map(label => `<span class="search-prototype-chip">${escHtml(label)}</span>`)
    .join('');
  document.getElementById('preview-sub').textContent = mode === 'smart' ? 'Smart search draft' : 'Basic search draft';
  area.innerHTML = `
    <div class="search-prototype-preview">
      <div class="search-prototype-hero">
        <div class="search-prototype-poster"><img src="${poster}" alt="${title}" loading="lazy"></div>
        <div class="search-prototype-copy">
          <div class="search-prototype-topline">
            <span class="search-prototype-mode ${mode}">${modeLabel}</span>
            <span class="search-prototype-local">Local-only prototype</span>
            ${baseName ? `<span class="search-prototype-base">Base catalog: ${baseName}</span>` : ''}
          </div>
          <div class="search-prototype-title">${title}</div>
          <div class="search-prototype-row-name">
            <strong>Suggested row name</strong>
            <span>${escHtml(prototype?.name || '')}</span>
          </div>
          <div class="search-prototype-meta-grid">
            <div class="search-prototype-block">
              <strong>Selected anime</strong>
              <div class="search-prototype-note">${title}${selected.seasonYear ? ` · ${escHtml(selected.seasonYear)}` : ''}</div>
            </div>
            <div class="search-prototype-block">
              <strong>${mode === 'smart' ? 'Future seed metadata' : 'Derived metadata'}</strong>
              <div class="search-prototype-chip-row">${chips || '<span class="search-prototype-note">No metadata captured.</span>'}</div>
            </div>
          </div>
          <div class="search-prototype-note">${modeNote}</div>
        </div>
      </div>
      <div class="search-prototype-actions">
        <button class="btn btn-primary btn-sm" type="button" data-action="open-search-add-modal-from-preview">Add to Catalog</button>
        <button class="btn btn-ghost btn-sm" type="button" data-action="dismiss-search-prototype-preview">Close Preview</button>
      </div>
    </div>`;
}

function openPrototypePreview(prototype, { selectedId = null } = {}) {
  activePrototypePreview = cloneJson(prototype);
  previewingId = selectedId;
  if (currentPane === 'catalogs') setPaneTab('preview');
  render();
  renderFilterTags();
  renderSearchPrototypePreview(activePrototypePreview);
}

function clearPrototypePreview({ keepPreviewingId = false } = {}) {
  activePrototypePreview = null;
  if (!keepPreviewingId) previewingId = null;
  renderFilterTags();
}

function dismissPrototypePreview() {
  clearPrototypePreview();
  render();
  renderDefaultPreviewPrompt();
}

function getSearchResultById(resultId) {
  return searchResults.find(item => String(item.id) === String(resultId)) || null;
}

function renderSearchDropdown() {
  const dropdown = document.getElementById('header-search-dropdown');
  if (!dropdown) return;
  dropdown.classList.toggle('open', searchOpen);
  if (!searchOpen) {
    dropdown.innerHTML = '';
    return;
  }
  const query = String(searchQuery || '').trim();
  if (query.length < SEARCH_MIN_CHARS) {
    dropdown.innerHTML = `<div class="search-dropdown-state"><strong>Search Anime</strong><span>Type at least ${SEARCH_MIN_CHARS} characters to search AniList.</span></div>`;
    return;
  }
  if (searchLoading) {
    dropdown.innerHTML = '<div class="search-dropdown-state"><strong>Searching</strong><span>Looking up matching anime titles on AniList.</span></div>';
    return;
  }
  if (!searchResults.length) {
    dropdown.innerHTML = '<div class="search-dropdown-state"><strong>No Matches</strong><span>Try a broader title or a different spelling.</span></div>';
    return;
  }
  dropdown.innerHTML = '<div class="search-result-list">' + searchResults.map((item, idx) => `
    <div class="search-result-row ${idx === searchActiveIndex ? 'active' : ''}">
      <button class="search-result-main" type="button" data-action="search-result-preview" data-result-id="${escHtml(item.id)}">
        <div class="search-result-thumb"><img src="${escHtml(item.coverImage)}" alt="${escHtml(item.title)}" loading="lazy"></div>
        <div class="search-result-copy">
          <div class="search-result-title">${escHtml(item.title)}</div>
          <div class="search-result-meta">${escHtml(searchResultMetaText(item))}</div>
        </div>
      </button>
      <button class="search-result-add-btn" type="button" data-action="search-result-add" data-result-id="${escHtml(item.id)}">Add to Catalog</button>
    </div>
  `).join('') + '</div>';
}

function renderSearchUi() {
  const metadataBtn = document.getElementById('search-mode-metadata');
  const smartBtn = document.getElementById('search-mode-smart');
  const hint = document.getElementById('search-smart-hint');
  if (!metadataBtn || !smartBtn || !hint) return;
  const state = getSmartRequirementState();
  const smartUnlocked = !state.needsAniList && !state.needsOpenRouter;
  if (!smartUnlocked && searchMode === 'smart') searchMode = 'metadata';
  metadataBtn.classList.toggle('active', searchMode === 'metadata');
  smartBtn.classList.toggle('active', searchMode === 'smart' && smartUnlocked);
  smartBtn.disabled = !smartUnlocked;
  smartBtn.classList.toggle('locked', !smartUnlocked);
  hint.textContent = smartUnlocked ? '' : 'Connect AniList + OpenRouter to unlock Smart search';
  hint.classList.toggle('visible', !smartUnlocked);
  renderSearchDropdown();
}

function closeSearchDropdown() {
  searchOpen = false;
  searchActiveIndex = -1;
  renderSearchDropdown();
}

function scheduleSearchLookup(rawValue) {
  searchQuery = rawValue;
  searchOpen = true;
  clearTimeout(searchLookupTimer);
  if (searchAbortController) {
    searchAbortController.abort();
    searchAbortController = null;
  }
  const query = String(rawValue || '').trim();
  if (query.length < SEARCH_MIN_CHARS) {
    searchLoading = false;
    searchResults = [];
    searchActiveIndex = -1;
    renderSearchUi();
    return;
  }
  searchLoading = true;
  renderSearchUi();
  const token = ++searchLookupToken;
  searchLookupTimer = setTimeout(async () => {
    if (token !== searchLookupToken) return;
    const controller = new AbortController();
    searchAbortController = controller;
    try {
      const res = await fetch(`/api/search-anime?q=${encodeURIComponent(query)}`, {
        signal: controller.signal,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail || `HTTP ${res.status}`);
      }
      const json = await res.json();
      if (token !== searchLookupToken) return;
      searchResults = Array.isArray(json.media) ? json.media : [];
      searchLoading = false;
      searchActiveIndex = searchResults.length ? 0 : -1;
      renderSearchDropdown();
    } catch (err) {
      if (err?.name === 'AbortError') return;
      console.error('[search] lookup failed:', err);
      if (token !== searchLookupToken) return;
      searchResults = [];
      searchLoading = false;
      searchActiveIndex = -1;
      renderSearchDropdown();
    } finally {
      if (searchAbortController === controller) searchAbortController = null;
    }
  }, SEARCH_DEBOUNCE_MS);
}

async function previewSearchResult(item) {
  if (!item) return;
  const draft = buildPrototypeCatalogDraft(item, getResolvedSearchMode());
  activePrototypePreview = cloneJson(draft);
  previewingId = null;
  closeSearchDropdown();
  if (currentPane === 'catalogs') setPaneTab('preview');

  if (draft.uiCatalogDraft?.type === 'ai') {
    activeSource = {
      ...cloneJson(draft.uiCatalogDraft),
      sourceName: draft.uiSelectedTitle?.title || draft.uiCatalogDraft.seedTitle || draft.name,
      previewName: draft.name,
      type: 'ai',
    };
    _sourceMedia = null;
    _clearAdditionalFilters();
    renderFilterTags();
    updateNameInput();
    render();
    await fetchAndShowSource();
    return;
  }

  activeSource = null;
  _sourceMedia = null;
  _clearAdditionalFilters();
  loadFiltersIntoForm(draft.uiCatalogDraft?.filters || {});
  renderFilterTags();
  updateNameInput();
  render();
  await previewActiveSearchDraft();
}

function handleSearchKeydown(event) {
  const query = String(searchQuery || '').trim();
  if (event.key === 'Escape') {
    event.preventDefault();
    closeSearchDropdown();
    return;
  }
  if (query.length < SEARCH_MIN_CHARS || searchLoading || !searchResults.length) return;
  if (event.key === 'ArrowDown') {
    event.preventDefault();
    searchActiveIndex = (searchActiveIndex + 1 + searchResults.length) % searchResults.length;
    renderSearchDropdown();
    return;
  }
  if (event.key === 'ArrowUp') {
    event.preventDefault();
    searchActiveIndex = (searchActiveIndex - 1 + searchResults.length) % searchResults.length;
    renderSearchDropdown();
    return;
  }
  if (event.key === 'Enter') {
    event.preventDefault();
    previewSearchResult(searchResults[searchActiveIndex] || searchResults[0]);
  }
}

function setSearchCatalogModalOpen(open) {
  const overlay = document.getElementById('search-modal-overlay');
  if (!overlay) return;
  overlay.classList.toggle('open', !!open);
  if (open) setTimeout(() => overlay.querySelector('button')?.focus(), 0);
}

function renderSearchCatalogModal() {
  const titleEl = document.getElementById('search-modal-title');
  const subEl = document.getElementById('search-modal-sub');
  const bodyEl = document.getElementById('search-modal-body');
  if (!titleEl || !subEl || !bodyEl || !searchModalDraft) return;
  titleEl.textContent = 'Add Search Result';
  subEl.textContent = `${searchModalDraft.uiSelectedTitle?.title || 'Selected anime'} · Single entry`;
  const available = supportedCatalogs(catalogs).filter(cat => cat && cat.id !== searchModalDraft.id);
  if (!available.length) {
    bodyEl.innerHTML = '<div class="search-modal-empty">No existing catalogs yet. Add a preset, account row, or custom row first, then use this action to inject a single anime into it.</div>';
    return;
  }
  bodyEl.innerHTML = `
    <div class="search-modal-note">Choose any existing row below. Create Copy makes a new Custom row based on that catalog plus this anime. Overwrite replaces the selected row in place and converts it to a Custom row.</div>
    <div class="search-modal-list">
      ${available.map(cat => `
        <div class="search-modal-item">
          <div class="search-modal-item-copy">
            <div class="search-modal-item-name">${escHtml(cat.name)}</div>
            <div class="search-modal-item-meta">
              <span class="catalog-type-badge${catalogTypeBadgeClass(cat)}">${catalogTypeBadgeLabel(cat)}</span>
              <span>${catalogRequiresAuth(cat) ? 'Auth-backed' : 'Public-safe'}</span>
            </div>
          </div>
          <div class="search-modal-actions">
            <button class="search-modal-btn" type="button" data-action="search-modal-create-copy" data-target-id="${escHtml(cat.id)}">Create Copy</button>
            <button class="search-modal-btn overwrite" type="button" data-action="search-modal-overwrite" data-target-id="${escHtml(cat.id)}">Overwrite</button>
          </div>
        </div>
      `).join('')}
    </div>`;
}

function openSearchCatalogModal(draft) {
  const selected = draft?.uiSelectedTitle ? snapshotSearchItem(draft.uiSelectedTitle) : snapshotSearchItem(draft);
  searchModalDraft = {
    id: draft?.id || 'search-modal-draft',
    uiSelectedTitle: selected,
  };
  closeSearchDropdown();
  renderSearchCatalogModal();
  setSearchCatalogModalOpen(true);
}

function closeSearchCatalogModal() {
  searchModalDraft = null;
  setSearchCatalogModalOpen(false);
}

function applySearchDraftToCatalog(targetId, strategy) {
  if (!searchModalDraft) return;
  const targetIndex = catalogs.findIndex(cat => cat.id === targetId);
  if (targetIndex === -1) return;
  const target = catalogs[targetIndex];
  const next = buildInjectedCatalogFromSearch(target, searchModalDraft.uiSelectedTitle, {
    preserveName: strategy === 'overwrite',
  });
  if (strategy === 'overwrite') {
    catalogs.splice(targetIndex, 1, next);
    closeSearchCatalogModal();
    render();
    previewCatalog(next.id);
    return;
  }
  catalogs.push(next);
  closeSearchCatalogModal();
  render();
  previewCatalog(next.id);
}

function updatePrototypeInstallNote() {
  const note = document.getElementById('prototype-install-note');
  if (!note) return;
  const hasPrototypeRows = catalogs.some(isUiPrototype);
  const hasAuthOmissions = !_sessionKey && catalogs.some(cat => cat && !isUiPrototype(cat) && catalogRequiresAuth(cat));
  if (hasPrototypeRows) {
    note.textContent = 'Search prototype rows are not included in this install URL yet.';
    note.classList.add('visible');
    return;
  }
  if (hasAuthOmissions) {
    note.textContent = 'Reconnect AniList to include account-backed custom rows in this install URL.';
    note.classList.add('visible');
    return;
  }
  note.classList.remove('visible');
}

function hasActiveAdditionalFilters() {
  const score = parseInt(document.getElementById('f-score').value);
  const daterange = document.getElementById('f-daterange').value;
  return selectedGenres.length > 0 || selectedFormats.length > 0 ||
         selectedStatuses.length > 0 || selectedYears.length > 0 ||
         selectedSeasons.length > 0 || score > 0 || !!daterange;
}

function hasStoredClientFilters(cat) {
  return !!(cat && cat.clientFilters && Object.keys(cat.clientFilters).length);
}

function getSourceBaseName(source) {
  if (!source) return '';
  if (source.sourceName) return source.sourceName;
  if (source.type === 'ai' && source.aiMode) return source.name || 'Smart Row';
  if (source.type === 'ai') return 'AI Recommendations';
  switch (source.listStatus) {
    case 'CURRENT': return 'Currently Watching';
    case 'PLANNING': return 'Plan to Watch';
    case 'COMPLETED': return 'Completed';
    case 'PAUSED': return 'Paused';
    case 'DROPPED': return 'Dropped';
    case 'REPEATING': return 'Rewatching';
    case 'FAVOURITES': return 'My Favourites';
    default: return source.name || '';
  }
}

function getSourceDisplayName(source) {
  if (!source) return '';
  return source.previewName || source.name || getSourceBaseName(source);
}

// Clear additional filter state (genre/format/status/year/season/score/sort/daterange)
// without touching activeSource.
function _clearAdditionalFilters() {
  document.getElementById('f-sort').value = 'POPULARITY_DESC';
  document.getElementById('f-daterange').value = '';
  document.getElementById('f-score').value = 0;
  document.getElementById('score-val').textContent = 'Any';
  includeAdult = false;
  document.getElementById('f-adult').checked = false;
  document.getElementById('adult-toggle').classList.remove('active');
  selectedGenres = []; selectedFormats = []; selectedStatuses = [];
  selectedYears  = []; selectedSeasons = [];
  syncFilterBtnLabels();
  if (activeFbFilter) renderFilterOpts(activeFbFilter);
}

// Build a human-readable name suggestion from active source + filter tags.
function _buildSuggestedName() {
  if (activeSource?.type === 'ai' && activeSource.aiMode === 'title_seed' && activeSource.seedTitle) {
    const parts = [`More like ${activeSource.seedTitle}`];
    selectedGenres.forEach(g  => parts.push(g));
    selectedFormats.forEach(f  => parts.push(FORMAT_LABELS[f] || f));
    selectedYears.forEach(y    => parts.push(y));
    selectedSeasons.forEach(s  => parts.push(s === 'CURRENT' ? 'Current Season' : (SEASON_LABELS[s] || s)));
    selectedStatuses.forEach(s => parts.push(STATUS_LABELS[s] || s));
    const daterange = getSelectedDateRangeValue();
    if (daterange) parts.push(getDateRangeLabel(daterange));
    const score = parseInt(document.getElementById('f-score').value);
    if (score > 0) parts.push(score + '+ Score');
    return parts.join(' · ');
  }
  const parts = [getSourceBaseName(activeSource)];
  selectedGenres.forEach(g  => parts.push(g));
  selectedFormats.forEach(f  => parts.push(FORMAT_LABELS[f] || f));
  selectedYears.forEach(y    => parts.push(y));
  selectedSeasons.forEach(s  => parts.push(s === 'CURRENT' ? 'Current Season' : (SEASON_LABELS[s] || s)));
  selectedStatuses.forEach(s => parts.push(STATUS_LABELS[s] || s));
  const daterange = getSelectedDateRangeValue();
  if (daterange) parts.push(getDateRangeLabel(daterange));
  const score = parseInt(document.getElementById('f-score').value);
  if (score > 0) parts.push(score + '+ Score');
  return parts.join(' · ');
}

// Build a clientFilters object from the current DOM filter state.
function _buildClientFilters() {
  const f = {};
  const sort  = document.getElementById('f-sort').value;
  const score = parseInt(document.getElementById('f-score').value);
  const daterange = getSelectedDateRangeValue();
  if (sort && sort !== 'POPULARITY_DESC') f.sort = sort;
  if (selectedGenres.length)   f.genres   = [...selectedGenres];
  if (selectedFormats.length)  f.formats  = [...selectedFormats];
  if (selectedStatuses.length) f.statuses = [...selectedStatuses];
  if (selectedYears.length)    f.years    = [...selectedYears];
  if (selectedSeasons.length)  f.seasons  = [...selectedSeasons];
  if (daterange)               f.daterange = daterange;
  if (score > 0)               f.minScore = score;
  return f;
}

// Update the name-input state based on source/filter state.
// Source-backed catalogs should remain nameable/savable in Preview too.
function updateNameInput() {
  const wrap   = document.getElementById('catalog-name-wrap');
  const addBtn = document.getElementById('catalog-add-btn');
  if (!wrap || !addBtn) return;

  const hasFilters = hasActiveAdditionalFilters();
  const inp = document.getElementById('catalog-name');
  wrap.classList.remove('hidden');
  addBtn.classList.remove('hidden');

  if (activePrototypePreview?.uiDraft) {
    const suggested = activePrototypePreview.name || activePrototypePreview.uiCatalogDraft?.name || '';
    if (suggested && (!inp.value.trim() || inp.value === _lastSuggestedName)) {
      inp.value = suggested;
      _lastSuggestedName = suggested;
    }
  } else if (activeSource && (hasFilters || (activeSource.type === 'ai' && activeSource.aiMode === 'title_seed' && activeSource.seedTitle))) {
    const suggested = _buildSuggestedName();
    if (!inp.value.trim() || inp.value === _lastSuggestedName) {
      inp.value = suggested;
      _lastSuggestedName = suggested;
    }
  } else if (activeSource) {
    if (inp.value === _lastSuggestedName) inp.value = '';
    _lastSuggestedName = '';
  } else if (!activeSource) {
    _lastSuggestedName = '';
  }
}

// Apply current DOM filter state client-side to a media array.
// Pass an explicit cf object (stored clientFilters) to replay a saved catalog.
function _filterSourceMedia(media, cf) {
  const genres   = cf ? (cf.genres   || []) : selectedGenres;
  const formats  = cf ? (cf.formats  || []) : selectedFormats;
  const statuses = cf ? (cf.statuses || []) : selectedStatuses;
  const years    = cf ? (cf.years    || []) : selectedYears;
  const seasons  = cf ? (cf.seasons  || []) : selectedSeasons;
  const daterange = cf ? (cf.daterange || '') : getSelectedDateRangeValue();
  const score    = cf ? (cf.minScore || 0)  : parseInt(document.getElementById('f-score').value);
  const sort     = cf ? (cf.sort || 'POPULARITY_DESC') : document.getElementById('f-sort').value;

  let result = media;
  if (genres.length)   result = result.filter(m => genres.every(g => (m.genres || []).includes(g)));
  if (formats.length)  result = result.filter(m => formats.includes(m.format));
  if (statuses.length) result = result.filter(m => statuses.includes(m.status));
  if (years.length)    result = result.filter(m => years.includes(String(m.seasonYear)));
  if (seasons.length) {
    const resolved = seasons.map(s => s === 'CURRENT' ? getCurrentSeason() : s);
    result = result.filter(m => resolved.includes(m.season));
  }
  if (daterange) result = result.filter(m => mediaMatchesDateRange(m, daterange));
  if (score > 0) result = result.filter(m => (m.averageScore || 0) >= score);

  result = [...result];
  result.sort((a, b) => {
    switch (sort) {
      case 'SCORE_DESC':
        return (b.averageScore || 0) - (a.averageScore || 0);
      case 'START_DATE_DESC': {
        const da = (a.seasonYear || 0) * 100 + (a.startDate && a.startDate.month ? a.startDate.month : 0);
        const db = (b.seasonYear || 0) * 100 + (b.startDate && b.startDate.month ? b.startDate.month : 0);
        return db - da;
      }
      default:
        return (b.popularity || 0) - (a.popularity || 0);
    }
  });
  return result;
}

// Re-render preview using _sourceMedia + current filter state.
function _applySourcePreview() {
  if (!activeSource || !_sourceMedia) return;
  const filtered = _filterSourceMedia(_sourceMedia);
  const count = filtered.length;
  const total = _sourceMedia.length;
  const label = getSourceDisplayName(activeSource);
  const subtitle = count < total
    ? `${label} — ${count} of ${total} titles`
    : `${label} — ${count} titles`;
  renderPreview(filtered, subtitle);
}

async function previewPresetWithCurrentFilters(cat) {
  setPreviewLoading(cat.name);
  try {
    if (cat.id === 'anilist-airing-week') {
      const media = await fetchAiringWeekPreview();
      const filtered = _filterSourceMedia(media);
      const subtitle = filtered.length < media.length
        ? `${cat.name} — ${filtered.length} of ${media.length} titles`
        : `${cat.name} — ${filtered.length} titles`;
      renderPreview(filtered, subtitle);
      return;
    }

    const sort  = document.getElementById('f-sort').value;
    const score = parseInt(document.getElementById('f-score').value);
    const year   = selectedYears.length === 1 ? selectedYears[0] : '';
    const season = selectedSeasons.length === 1 ? selectedSeasons[0] : '';
    const sv = resolveSeasonVars(season, year);
    const variables = { ...PRESET_VARS[cat.id]() };

    if (sort)                    variables.sort = [sort];
    if (!includeAdult)           variables.isAdult = false;
    if (selectedFormats.length)  variables.format_in = [...selectedFormats];
    else delete variables.format_in;
    if (selectedStatuses.length) variables.status_in = [...selectedStatuses];
    else delete variables.status_in;
    if (sv.season)               variables.season = sv.season;
    else delete variables.season;
    if (sv.seasonYear)           variables.seasonYear = sv.seasonYear;
    else delete variables.seasonYear;
    if (score > 0)               variables.averageScore_greater = score;
    else delete variables.averageScore_greater;
    if (selectedGenres.length)   variables.genre_in = [...selectedGenres];
    else delete variables.genre_in;
    applyDateRangeToVariables(variables, getSelectedDateRangeValue());

    const media = await fetchPreview(variables);
    renderPreview(media, `${cat.name} — ${media.length} titles`);
  } catch (e) {
    console.error('[preset preview] Error:', e);
    document.getElementById('preview-sub').textContent = 'Failed to load preview';
    document.getElementById('preview-area').innerHTML =
      `<div class="preview-prompt"><div>Could not reach AniList API</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
  }
}

// Fetch source content from the server and then apply client-side filters.
async function fetchAndShowSource() {
  if (!activeSource) return;
  const captured = activeSource;

  if (activeSource.type === 'watching') {
    if (!_sessionKey) {
      document.getElementById('preview-sub').textContent = getSourceDisplayName(activeSource);
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#128274;</div><div>Account catalog<br><span class="preview-error-detail">Connect your AniList account to preview this list</span></div></div>';
      return;
    }
    setPreviewLoading(getSourceDisplayName(activeSource));
    try {
      const res = await fetch('/api/preview-watching', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session: _sessionKey, list_status: activeSource.listStatus }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail || `HTTP ${res.status}`);
      }
      const json = await res.json();
      if (activeSource !== captured) return; // source changed during async fetch
      _sourceMedia = json.media;
      _applySourcePreview();
    } catch(e) {
      console.error('[source] watching fetch error:', e);
      document.getElementById('preview-sub').textContent = 'Failed to load list';
      document.getElementById('preview-area').innerHTML =
        `<div class="preview-prompt"><div>Could not load account catalog</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
    }
    return;
  }

  if (activeSource.type === 'ai') {
    if (!_sessionKey) {
      document.getElementById('preview-sub').textContent = getSourceDisplayName(activeSource);
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#128274;</div><div>Account catalog<br><span class="preview-error-detail">Connect your AniList account to use AI recommendations</span></div></div>';
      return;
    }
    if (!_hasOrKey) {
      document.getElementById('preview-sub').textContent = getSourceDisplayName(activeSource);
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#9881;</div><div>OpenRouter key required<br><span class="preview-error-detail">Use Smart Rows settings to add your key</span></div></div>';
      return;
    }
    setPreviewLoading('AI is thinking… (this may take a moment)');
    try {
      const res = await fetch('/api/preview-ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session: _sessionKey, catalog: activeSource }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail || `HTTP ${res.status}`);
      }
      const json = await res.json();
      if (activeSource !== captured) return;
      _sourceMedia = json.media;
      _applySourcePreview();
    } catch(e) {
      console.error('[source] ai fetch error:', e);
      document.getElementById('preview-sub').textContent = 'Failed to load AI recommendations';
      document.getElementById('preview-area').innerHTML =
        `<div class="preview-prompt"><div>Could not load AI recommendations</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
    }
  }
}

function addAccountPreset(id, name, listStatus) {
  if (activePrototypePreview) clearPrototypePreview();
  if (!_sessionKey) return;
  const alreadyAdded = !!catalogs.find(c => c.id === id);
  // Set this as the active source (shows tag in filter bar + enables filtering on top)
  activeSource = { id, name, sourceName: name, previewName: name, listStatus, type: 'watching' };
  _sourceMedia = null;
  _lastSuggestedName = '';
  // Clear any previously active filters — new source starts fresh
  _clearAdditionalFilters();
  if (!alreadyAdded) {
    catalogs.push({ id, name, type: 'watching', listStatus });
    render();
    renderFilterTags();
    updateNameInput();
    setPaneTab('catalogs');
    fetchAndShowSource();
  } else {
    renderFilterTags();
    updateNameInput();
    setPaneTab('preview');
    render();
    fetchAndShowSource();
  }
}

// ── AI Settings Modal ─────────────────────────────
function openAiModal() {
  if (!_sessionKey) {
    saveConfigBeforeLogin();
    window.location.href = '/oauth/login';
    return;
  }
  const overlay = document.getElementById('ai-modal-overlay');
  if (!overlay) return;
  // Populate model selector
  const select = document.getElementById('ai-model-select');
  const customInput = document.getElementById('ai-model-custom');
  if (select && customInput) {
    const knownVals = Array.from(select.options).map(o => o.value).filter(v => v !== 'custom');
    if (knownVals.includes(_orModel)) {
      select.value = _orModel;
      customInput.classList.remove('visible');
    } else {
      select.value = 'custom';
      customInput.classList.add('visible');
      customInput.value = _orModel;
    }
  }
  // Never pre-fill the key input
  const keyInput = document.getElementById('ai-key-input');
  if (keyInput) keyInput.value = '';
  const fb = document.getElementById('ai-key-feedback');
  if (fb) { fb.textContent = _hasOrKey ? '(Key already saved — enter a new one to replace it)' : ''; fb.className = 'ai-key-feedback'; }
  overlay.classList.add('open');
}

function closeAiModal() {
  const overlay = document.getElementById('ai-modal-overlay');
  if (overlay) overlay.classList.remove('open');
}

function handleAiModelChange() {
  const select = document.getElementById('ai-model-select');
  const customInput = document.getElementById('ai-model-custom');
  if (!select || !customInput) return;
  if (select.value === 'custom') {
    customInput.classList.add('visible');
    customInput.focus();
  } else {
    customInput.classList.remove('visible');
  }
}

async function testOrKey() {
  const keyInput = document.getElementById('ai-key-input');
  const fb       = document.getElementById('ai-key-feedback');
  const btn      = document.getElementById('ai-test-btn');
  if (!keyInput || !keyInput.value.trim()) {
    if (fb) { fb.textContent = 'Enter an API key first.'; fb.className = 'ai-key-feedback err'; }
    return;
  }
  if (btn) { btn.disabled = true; btn.textContent = 'Testing…'; }
  if (fb) { fb.textContent = ''; fb.className = 'ai-key-feedback'; }
  try {
    const res = await fetch('/api/test-openrouter-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: keyInput.value.trim() }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data.valid) {
      if (fb) { fb.textContent = '✓ Key is valid.'; fb.className = 'ai-key-feedback ok'; }
    } else {
      if (fb) { fb.textContent = '✗ ' + (data.detail || 'Invalid key.'); fb.className = 'ai-key-feedback err'; }
    }
  } catch(e) {
    if (fb) { fb.textContent = '✗ Network error.'; fb.className = 'ai-key-feedback err'; }
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Test'; }
  }
}

async function saveOrKeyFromModal() {
  if (!_sessionKey) return;
  const keyInput  = document.getElementById('ai-key-input');
  const select    = document.getElementById('ai-model-select');
  const customInp = document.getElementById('ai-model-custom');
  const saveBtn   = document.getElementById('ai-modal-save-btn');
  const fb        = document.getElementById('ai-key-feedback');

  const key   = keyInput?.value.trim() || '';
  const model = select?.value === 'custom'
    ? (customInp?.value.trim() || 'meta-llama/llama-3.3-70b-instruct')
    : (select?.value || 'meta-llama/llama-3.3-70b-instruct');

  if (!key && !_hasOrKey) {
    if (fb) { fb.textContent = 'Enter an API key.'; fb.className = 'ai-key-feedback err'; }
    return;
  }
  if (saveBtn) { saveBtn.disabled = true; saveBtn.textContent = 'Saving…'; }
  try {
    const res = await fetch('/api/save-openrouter-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session: _sessionKey, key: key || null, model }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      const modelChanged = _orModel !== model;
      _hasOrKey = true;
      _orModel  = model;
      // Update any existing AI catalog entries with the new model
      catalogs.forEach(c => { if (c.type === 'ai') c.model = model; });
      updateAccountPills();
      updateSmartRowsStatus();
      render();
      closeAiModal();
      // If a Smart Row is being previewed, switching models should refresh it.
      if (modelChanged && activeSource?.type === 'ai') {
        _sourceMedia = null;
        renderFilterTags();
        updateNameInput();
        setPaneTab('preview');
        fetchAndShowSource();
      }
    } else {
      if (fb) { fb.textContent = '✗ ' + (data.detail || 'Failed to save.'); fb.className = 'ai-key-feedback err'; }
    }
  } catch(e) {
    if (fb) { fb.textContent = '✗ Network error.'; fb.className = 'ai-key-feedback err'; }
  } finally {
    if (saveBtn) { saveBtn.disabled = false; saveBtn.textContent = 'Save'; }
  }
}

// ── Filter bar helpers ────────────────────────────

// ── Inline filter panel helpers ────────────────────
// Smart Row builder
function setSmartModalOpen(open) {
  const overlay = document.getElementById('smart-modal-overlay');
  if (!overlay) return;
  overlay.classList.toggle('open', !!open);
  if (open) setTimeout(() => overlay.querySelector('button, input, select')?.focus(), 0);
}

function closeSmartBuilder() {
  setSmartModalOpen(false);
}

function resetSmartBuilderPreview() {
  smartBuilderPreviewCatalog = null;
  smartBuilderPreviewMedia = [];
  const preview = document.getElementById('smart-inline-preview');
  if (preview) {
    preview.classList.remove('visible');
    preview.innerHTML = '';
  }
  const feedback = document.getElementById('smart-preview-feedback');
  if (feedback) { feedback.textContent = ''; feedback.className = 'smart-preview-feedback'; }
  updateSmartSaveState();
}

function defaultSmartRowName(mode, seedTitle = '') {
  if (mode === 'title_seed') return seedTitle ? `More like ${seedTitle}` : 'More like this anime';
  return SMART_DEFAULTS[mode]?.name || 'Smart Row';
}

function setSmartTemplate(mode) {
  if (!SMART_DEFAULTS[mode]) return;
  smartBuilderMode = mode;
  const modeSelect = document.getElementById('smart-seed-mode');
  if (modeSelect) modeSelect.value = mode;
  const titleWrap = document.getElementById('smart-title-wrap');
  if (titleWrap) titleWrap.classList.toggle('hidden', mode !== 'title_seed');
  const defaults = SMART_DEFAULTS[mode];
  const rowName = document.getElementById('smart-row-name');
  const seedTitle = document.getElementById('smart-seed-title')?.value.trim() || '';
  if (rowName && (!rowName.value.trim() || rowName.dataset.autoname === '1')) {
    rowName.value = defaultSmartRowName(mode, seedTitle);
    rowName.dataset.autoname = '1';
  }
  const minScore = document.getElementById('smart-min-score');
  if (minScore) minScore.value = String(defaults.options.minScore || 0);
  const popularity = document.getElementById('smart-popularity');
  if (popularity) popularity.value = defaults.options.popularityBias || 'balanced';
  document.querySelectorAll('.smart-template').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === mode);
  });
  resetSmartBuilderPreview();
}

function parseSeedInput(raw) {
  const text = (raw || '').trim();
  if (!text) return { title: '', id: null };
  const urlMatch = text.match(/anilist\\.co\\/anime\\/(\\d+)/i);
  if (urlMatch) return { title: text.replace(/^https?:\\/\\//i, ''), id: parseInt(urlMatch[1], 10) };
  if (/^\\d+$/.test(text)) return { title: text, id: parseInt(text, 10) };
  return { title: text, id: null };
}

function buildSmartCatalogFromForm() {
  const mode = document.getElementById('smart-seed-mode')?.value || smartBuilderMode;
  const seed = parseSeedInput(document.getElementById('smart-seed-title')?.value || '');
  const formats = Array.from(document.querySelectorAll('[data-smart-format]:checked')).map(input => input.value);
  const minScore = parseInt(document.getElementById('smart-min-score')?.value || '0', 10) || 0;
  const popularityBias = document.getElementById('smart-popularity')?.value || 'balanced';
  const rowNameInput = document.getElementById('smart-row-name');
  const name = (rowNameInput?.value || '').trim() || defaultSmartRowName(mode, seed.title);
  const catalog = {
    id: 'ai-' + Math.random().toString(36).slice(2, 10),
    name,
    type: 'ai',
    model: _orModel,
    aiMode: mode,
    smartOptions: { formats, minScore, popularityBias },
  };
  if (mode === 'title_seed') {
    if (seed.id) catalog.seedMediaId = seed.id;
    catalog.seedTitle = seed.title;
  }
  return catalog;
}

function updateSmartSaveState() {
  const saveBtn = document.getElementById('smart-save-btn');
  if (saveBtn) saveBtn.disabled = !smartBuilderPreviewCatalog;
}

function renderSmartInlinePreview(media, catalog) {
  const preview = document.getElementById('smart-inline-preview');
  renderInlinePreviewInto(preview, media, catalog, { emptyMessage: 'No titles came back for this Smart Row.' });
}

function renderSmartInlinePreviewStatus(message) {
  const preview = document.getElementById('smart-inline-preview');
  renderInlinePreviewStatusInto(preview, message);
}

function renderSmartBuilder() {
  const body = document.getElementById('smart-modal-body');
  const footer = document.getElementById('smart-modal-footer');
  if (!body || !footer) return;
  smartBuilderPreviewCatalog = null;
  smartBuilderPreviewMedia = [];

  if (!_sessionKey || !_hasOrKey) {
    body.innerHTML = `<div class="smart-locked">
      Smart Rows need AniList auth and a saved OpenRouter key before they can generate catalogs.
      ${!_sessionKey ? 'Connect AniList first, then add your OpenRouter key.' : 'Open settings to add your OpenRouter key.'}
    </div>`;
    footer.innerHTML = '<button class="btn btn-ghost" data-action="close-smart-builder">Close</button><button class="btn btn-primary" data-action="open-ai-modal">Open Settings</button>';
    return;
  }

  body.innerHTML = `
    <div class="smart-template-grid">
      ${Object.entries(SMART_DEFAULTS).map(([mode, item]) => `
        <button class="smart-template ${mode === smartBuilderMode ? 'active' : ''}" type="button" data-action="smart-template" data-mode="${mode}">
          <strong>${escHtml(item.label)}</strong>
          <span>${escHtml(item.description)}</span>
        </button>
      `).join('')}
    </div>
    <div class="smart-form-grid">
      <label class="smart-label">Seed Type
        <select class="smart-select" id="smart-seed-mode">
          <option value="title_seed">More like a title</option>
          <option value="top_rated">More like my 10/10s</option>
          <option value="hidden_completed">Hidden gems from completed</option>
        </select>
      </label>
      <label class="smart-label">Popularity
        <select class="smart-select" id="smart-popularity">
          <option value="balanced">Balanced</option>
          <option value="hidden">Hidden gems</option>
          <option value="mainstream">Mainstream</option>
        </select>
      </label>
      <label class="smart-label smart-field-full" id="smart-title-wrap">Title, AniList ID, or AniList URL
        <input class="smart-input" id="smart-seed-title" placeholder="Frieren: Beyond Journey's End">
      </label>
      <label class="smart-label">Minimum Score
        <select class="smart-select" id="smart-min-score">
          <option value="0">Any</option>
          <option value="60">60+</option>
          <option value="70">70+</option>
          <option value="75">75+</option>
          <option value="80">80+</option>
        </select>
      </label>
      <label class="smart-label">Row Name
        <input class="smart-input" id="smart-row-name" data-autoname="1">
      </label>
      <div class="smart-label smart-field-full">Formats
        <div class="smart-format-row">
          ${['TV','MOVIE','OVA','ONA','TV_SHORT','SPECIAL'].map(fmt => `
            <label class="smart-check"><input type="checkbox" data-smart-format value="${fmt}">${escHtml(FORMAT_LABELS[fmt] || fmt)}</label>
          `).join('')}
        </div>
      </div>
    </div>
    <div class="smart-preview-feedback" id="smart-preview-feedback"></div>
    <div class="smart-inline-preview" id="smart-inline-preview"></div>`;
  footer.innerHTML = '<button class="btn btn-ghost" data-action="close-smart-builder">Cancel</button><button class="btn btn-ghost" data-action="smart-preview">Preview</button><button class="btn btn-primary" id="smart-save-btn" data-action="smart-save" disabled>Save Row</button>';
  setSmartTemplate(smartBuilderMode);
}

function openSmartBuilder() {
  renderSmartBuilder();
  setSmartModalOpen(true);
}

async function previewSmartRow() {
  if (!_sessionKey || !_hasOrKey) {
    openAiModal();
    return;
  }
  const feedback = document.getElementById('smart-preview-feedback');
  const previewBtn = document.querySelector('[data-action="smart-preview"]');
  const catalog = buildSmartCatalogFromForm();
  if (catalog.aiMode === 'title_seed' && !catalog.seedTitle && !catalog.seedMediaId) {
    if (feedback) { feedback.textContent = 'Enter a title, AniList ID, or AniList URL.'; feedback.className = 'smart-preview-feedback err'; }
    renderSmartInlinePreviewStatus('Preview results will appear here after you enter a seed.');
    return;
  }
  if (previewBtn) { previewBtn.disabled = true; previewBtn.textContent = 'Generating...'; }
  if (feedback) { feedback.textContent = 'Generating Smart Row...'; feedback.className = 'smart-preview-feedback'; }
  renderSmartInlinePreviewStatus('Generating preview...');
  try {
    const res = await fetch('/api/preview-ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session: _sessionKey, catalog }),
    });
    const json = await res.json().catch(() => null);
    if (!res.ok) throw new Error(json?.detail || `HTTP ${res.status}`);
    smartBuilderPreviewCatalog = catalog;
    smartBuilderPreviewMedia = json.media || [];
    renderSmartInlinePreview(smartBuilderPreviewMedia, catalog);
    if (feedback) { feedback.textContent = `Preview ready with ${smartBuilderPreviewMedia.length} titles.`; feedback.className = 'smart-preview-feedback ok'; }
  } catch(e) {
    smartBuilderPreviewCatalog = null;
    smartBuilderPreviewMedia = [];
    renderSmartInlinePreviewStatus('Preview failed. Adjust the row and try again.');
    if (feedback) { feedback.textContent = e instanceof Error ? e.message : String(e); feedback.className = 'smart-preview-feedback err'; }
  } finally {
    if (previewBtn) { previewBtn.disabled = false; previewBtn.textContent = 'Preview'; }
    updateSmartSaveState();
  }
}

function saveSmartRow() {
  if (!smartBuilderPreviewCatalog) return;
  catalogs.push(JSON.parse(JSON.stringify(smartBuilderPreviewCatalog)));
  closeSmartBuilder();
  setPaneTab('catalogs');
  render();
}

const FILTER_OPTS = {
  year: null, // built from hidden select options at runtime
  season: [
    { value: '', label: 'Any' },
    { value: 'CURRENT', label: 'Current Season' },
    { value: 'WINTER', label: 'Winter' },
    { value: 'SPRING', label: 'Spring' },
    { value: 'SUMMER', label: 'Summer' },
    { value: 'FALL', label: 'Fall' },
  ],
  format: [
    { value: '', label: 'Any' },
    { value: 'TV', label: 'TV Series' },
    { value: 'TV_SHORT', label: 'TV Short' },
    { value: 'MOVIE', label: 'Movie' },
    { value: 'OVA', label: 'OVA' },
    { value: 'ONA', label: 'ONA' },
    { value: 'SPECIAL', label: 'Special' },
  ],
  status: [
    { value: '', label: 'Any' },
    { value: 'RELEASING', label: 'Airing' },
    { value: 'FINISHED', label: 'Finished' },
    { value: 'NOT_YET_RELEASED', label: 'Upcoming' },
  ],
  sort: [
    { value: 'POPULARITY_DESC', label: 'Popularity' },
    { value: 'TRENDING_DESC', label: 'Trending' },
    { value: 'SCORE_DESC', label: 'Score' },
    { value: 'START_DATE_DESC', label: 'Newest' },
    { value: 'FAVOURITES_DESC', label: 'Favourites' },
  ],
  daterange: [
    { value: '', label: 'Any' },
    { value: 'this-week', label: 'This Week' },
    { value: 'this-month', label: 'This Month' },
    { value: 'last-month', label: 'Last Month' },
    { value: 'this-year', label: 'This Year' },
    { value: 'last-year', label: 'Last Year' },
  ],
};

const FILTER_PLACEHOLDERS = {
  genres: 'Genres', year: 'Year', season: 'Season', format: 'Format',
  status: 'Status', sort: 'Sort', daterange: 'Date Range',
};

let activeFbFilter = 'genres';

function clearActiveFilterPane() {
  document.querySelectorAll('.fb-filter-btn').forEach(b => b.classList.remove('active'));
  activeFbFilter = '';
  const pane = document.getElementById('filter-opts-pills');
  if (pane) pane.innerHTML = '';
}

function setActiveFilter(id) {
  closeYearMenu();
  document.querySelectorAll('.fb-filter-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('btn-' + id);
  if (btn) btn.classList.add('active');
  activeFbFilter = id;
  renderFilterOpts(id);
}

function toggleMultiVal(arr, val) {
  const i = arr.indexOf(val);
  if (i > -1) arr.splice(i, 1);
  else arr.push(val);
}

function updateFilterBtn(id) {
  if (id === 'year') {
    const value = selectedYears.length ? String(selectedYears[0]) : '';
    const lbl = document.getElementById('lbl-year');
    if (lbl) lbl.textContent = value || 'Year';
    const btn = document.getElementById('btn-year');
    if (btn) btn.classList.toggle('has-value', !!value);
    const sel = document.getElementById('f-year');
    if (sel) sel.value = value;
    renderYearMenu();
    return;
  }
  const btn = document.getElementById('btn-' + id);
  const lbl = document.getElementById('lbl-' + id);
  if (!btn || !lbl) return;
  const arr = id === 'genres'   ? selectedGenres
            : id === 'year'     ? selectedYears
            : id === 'season'   ? selectedSeasons
            : id === 'format'   ? selectedFormats
            : id === 'status'   ? selectedStatuses
            : null;
  if (arr !== null) {
    const placeholder = FILTER_PLACEHOLDERS[id] || id;
    if (arr.length === 0) {
      lbl.textContent = placeholder;
    } else if (arr.length === 1) {
      // show the label, not the value
      const opts = id === 'genres' ? null : FILTER_OPTS[id];
      if (opts) {
        const found = opts.find(o => o.value === arr[0]);
        lbl.textContent = found ? found.label : arr[0];
      } else {
        lbl.textContent = arr[0]; // year: use value directly
      }
    } else {
      lbl.textContent = `${placeholder} (${arr.length})`;
    }
    btn.classList.toggle('has-value', arr.length > 0);
  }
}

function renderFilterOpts(id) {
  const pane = document.getElementById('filter-opts-pills');
  pane.innerHTML = '';

  if (id === 'genres') {
    const atMax = selectedGenres.length >= 3;
    GENRES.forEach(g => {
      const btn = document.createElement('button');
      const isSel = selectedGenres.includes(g);
      btn.className = 'filter-opt-pill' + (isSel ? ' selected' : '') + (!isSel && atMax ? ' disabled' : '');
      btn.textContent = g;
      btn.onclick = () => {
        if (!isSel && selectedGenres.length >= 3) return;
        toggleMultiVal(selectedGenres, g);
        updateFilterBtn('genres');
        renderFilterOpts('genres');
        renderFilterTags();
        scheduleAutoPreview();
      };
      pane.appendChild(btn);
    });
    return;
  }

  const multiIds = ['season', 'format', 'status'];
  const arr = id === 'season'   ? selectedSeasons
            : id === 'format'   ? selectedFormats
            : id === 'status'   ? selectedStatuses
            : null;

  const opts = FILTER_OPTS[id];

  if (!opts) return;

  opts.forEach(opt => {
    const btn = document.createElement('button');
    if (arr !== null) {
      // multi-select
      const isSel = arr.includes(opt.value);
      btn.className = 'filter-opt-pill' + (isSel ? ' selected' : '');
      btn.textContent = opt.label;
      btn.dataset.value = opt.value;
      btn.onclick = () => {
        toggleMultiVal(arr, opt.value);
        updateFilterBtn(id);
        renderFilterOpts(id);
        renderFilterTags();
        scheduleAutoPreview();
      };
    } else {
      // single-select (sort, daterange)
      const sel = document.getElementById('f-' + id);
      const curVal = sel ? sel.value : '';
      btn.className = 'filter-opt-pill' + (opt.value === curVal ? ' selected' : '');
      btn.textContent = opt.label;
      btn.dataset.value = opt.value;
      btn.onclick = () => setFilterValue(id, opt.value, opt.label);
    }
    pane.appendChild(btn);
  });
}

function setFilterValue(id, value, label) {
  const sel = document.getElementById('f-' + id);
  if (sel) sel.value = value;
  // Update button label
  const dispLabel = value ? label : FILTER_PLACEHOLDERS[id];
  const lbl = document.getElementById('lbl-' + id);
  if (lbl) lbl.textContent = dispLabel;
  const btn = document.getElementById('btn-' + id);
  if (btn) btn.classList.toggle('has-value', !!value);
  // Update pill highlights
  document.querySelectorAll('#filter-opts-pills .filter-opt-pill').forEach(p => {
    p.classList.toggle('selected', p.dataset.value === value);
  });
  // Fire appropriate onChange
  if (id === 'daterange') { onDateRangeChange({ value }); return; }
  scheduleAutoPreview();
}

function renderYearMenu() {
  const menu = document.getElementById('year-menu');
  const sel = document.getElementById('f-year');
  if (!menu || !sel) return;
  const current = selectedYears.length ? String(selectedYears[0]) : '';
  const opts = [...sel.options].map(o => ({ value: String(o.value || ''), label: o.value ? o.text : 'Any' }));
  menu.innerHTML = opts.map(opt =>
    `<button class="year-menu-item${opt.value === current ? ' active' : ''}" type="button" data-action="set-year-value" data-value="${escHtml(opt.value)}">${escHtml(opt.label)}</button>`
  ).join('');
}

function toggleYearMenu() {
  const menu = document.getElementById('year-menu');
  const btn = document.getElementById('btn-year');
  if (!menu || !btn) return;
  const isOpen = menu.classList.contains('open');
  if (isOpen) {
    closeYearMenu();
    return;
  }
  closeSortMenu();
  clearActiveFilterPane();
  renderYearMenu();
  menu.classList.add('open');
  btn.classList.add('open', 'active');
}

function closeYearMenu() {
  const menu = document.getElementById('year-menu');
  if (menu) menu.classList.remove('open');
  const btn = document.getElementById('btn-year');
  if (btn) btn.classList.remove('open', 'active');
}

function setYearValue(value) {
  const normalized = value ? String(value) : '';
  selectedYears = normalized ? [normalized] : [];
  const sel = document.getElementById('f-year');
  if (sel) sel.value = normalized;
  closeYearMenu();
  clearActiveFilterPane();
  syncFilterBtnLabels();
  renderFilterTags();
  updateNameInput();
  scheduleAutoPreview();
}

function syncFilterBtnLabels() {
  ['genres', 'year', 'season', 'format', 'status'].forEach(id => updateFilterBtn(id));
  // single-select: daterange
  [['daterange','Date Range']].forEach(([id, placeholder]) => {
    const sel = document.getElementById('f-' + id);
    if (!sel) return;
    const val = sel.value;
    const lbl = document.getElementById('lbl-' + id);
    if (lbl) lbl.textContent = val ? (sel.options[sel.selectedIndex] ? sel.options[sel.selectedIndex].text : val) : placeholder;
    const btn = document.getElementById('btn-' + id);
    if (btn) btn.classList.toggle('has-value', !!val);
  });
}

// ── Preset filter definitions ─────────────────────
const PRESET_VARS = {
  'anilist-popular-season': () => ({
    sort: ['POPULARITY_DESC'],
    season: getCurrentSeason(),
    seasonYear: new Date().getFullYear(),
    status: 'RELEASING',
  }),
  'anilist-airing-week': () => ({
    sort: ['TRENDING_DESC'],
    status: 'RELEASING',
  }),
  'anilist-trending': () => ({
    sort: ['TRENDING_DESC'],
  }),
  'anilist-top-rated': () => ({
    sort: ['SCORE_DESC'],
  }),
};

// ── AniList preview fetch ─────────────────────────
const PREVIEW_QUERY = `
  query($sort:[MediaSort],$format_in:[MediaFormat],$season:MediaSeason,$seasonYear:Int,$status_in:[MediaStatus],$genre_in:[String],$averageScore_greater:Int,$startDate_greater:FuzzyDateInt,$startDate_lesser:FuzzyDateInt,$isAdult:Boolean,$id_in:[Int]){
    Page(page:1,perPage:50){
      media(type:ANIME,isAdult:$isAdult,sort:$sort,format_in:$format_in,season:$season,seasonYear:$seasonYear,status_in:$status_in,genre_in:$genre_in,averageScore_greater:$averageScore_greater,startDate_greater:$startDate_greater,startDate_lesser:$startDate_lesser,id_in:$id_in){
        id title{romaji english} coverImage{extraLarge large color} averageScore popularity trending source(version:2)
        genres format episodes status season seasonYear startDate{year month day} description(asHtml:false)
        rankings{rank type allTime context}
        relations{edges{relationType(version:2) node{type}}}
        studios(isMain:true){nodes{name}}
        nextAiringEpisode{episode timeUntilAiring}
      }
    }
  }
`;

async function fetchPreview(variables) {
  console.log('[fetchPreview] variables:', JSON.stringify(variables, null, 2));
  let res;
  try {
    res = await fetch('/anilist-proxy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: PREVIEW_QUERY, variables }),
    });
  } catch (networkErr) {
    console.error('[fetchPreview] Network error:', networkErr);
    throw networkErr;
  }
  console.log('[fetchPreview] HTTP status:', res.status, res.statusText);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    console.error('[fetchPreview] Error body:', body);
    const msg = body?.errors?.[0]?.message || `HTTP ${res.status} error`;
    throw new Error(msg);
  }
  const json = await res.json();
  if (json.errors) {
    console.error('[fetchPreview] GraphQL errors:', json.errors);
    throw new Error(json.errors[0].message);
  }
  console.log('[fetchPreview] Got', json.data.Page.media.length, 'results');
  return json.data.Page.media;
}

const PREVIEW_QUERY_AIRING = `
  query($start:Int,$end:Int){
    Page(page:1,perPage:50){
      airingSchedules(airingAt_greater:$start airingAt_lesser:$end sort:TIME){
        media{
          id title{romaji english} coverImage{extraLarge large color} averageScore isAdult popularity trending source(version:2)
          genres format episodes status season seasonYear startDate{year month day} description(asHtml:false)
          rankings{rank type allTime context}
          relations{edges{relationType(version:2) node{type}}}
          studios(isMain:true){nodes{name}}
          nextAiringEpisode{episode timeUntilAiring}
        }
      }
    }
  }
`;

async function fetchAiringWeekPreview() {
  const mon = getWeekStart();
  const sun = new Date(mon);
  sun.setDate(mon.getDate() + 6);
  sun.setHours(23, 59, 59, 999);
  const vars = { start: Math.floor(mon.getTime() / 1000), end: Math.floor(sun.getTime() / 1000) };
  console.log('[fetchAiringWeekPreview] variables:', JSON.stringify(vars));
  let res;
  try {
    res = await fetch('/anilist-proxy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: PREVIEW_QUERY_AIRING, variables: vars }),
    });
  } catch (networkErr) {
    console.error('[fetchAiringWeekPreview] Network error:', networkErr);
    throw networkErr;
  }
  console.log('[fetchAiringWeekPreview] HTTP status:', res.status, res.statusText);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    console.error('[fetchAiringWeekPreview] Error body:', body);
    const msg = body?.errors?.[0]?.message || `HTTP ${res.status} error`;
    throw new Error(msg);
  }
  const json = await res.json();
  if (json.errors) {
    console.error('[fetchAiringWeekPreview] GraphQL errors:', json.errors);
    throw new Error(json.errors[0].message);
  }
  const seen = new Set();
  const media = [];
  for (const s of json.data.Page.airingSchedules) {
    const m = s.media;
    if (!seen.has(m.id) && (includeAdult || !m.isAdult)) { seen.add(m.id); media.push(m); }
  }
  return media;
}

async function fetchPreviewByIds(ids) {
  const uniqueIds = [...new Set((ids || []).map(id => parseInt(id, 10)).filter(id => id > 0))];
  if (!uniqueIds.length) return [];
  return await fetchPreview({ id_in: uniqueIds, isAdult: false, sort: ['POPULARITY_DESC'] });
}

function mergePreviewMedia(primaryMedia, secondaryMedia) {
  const merged = [];
  const seen = new Set();
  [...(primaryMedia || []), ...(secondaryMedia || [])].forEach(media => {
    if (!media?.id || seen.has(media.id)) return;
    seen.add(media.id);
    merged.push(media);
  });
  return merged;
}

async function fetchCatalogPreviewMedia(cat) {
  if (!cat) return [];
  if (PRESET_IDS.has(cat.id) || cat.type === 'preset') {
    if (cat.id === 'anilist-airing-week') return await fetchAiringWeekPreview();
    return await fetchPreview({ ...(PRESET_VARS[cat.id] ? PRESET_VARS[cat.id]() : {}), isAdult: false });
  }
  if (cat.type === 'watching') {
    if (!_sessionKey) throw new Error('Connect your AniList account to preview this catalog.');
    const res = await fetch('/api/preview-watching', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session: _sessionKey, list_status: cat.listStatus }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `HTTP ${res.status}`);
    }
    const json = await res.json();
    return Array.isArray(json.media) ? json.media : [];
  }
  if (cat.type === 'ai') {
    if (!_sessionKey) throw new Error('Connect your AniList account to preview this Smart search.');
    if (!_hasOrKey) throw new Error('Add an OpenRouter key to preview this Smart search.');
    const res = await fetch('/api/preview-ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session: _sessionKey, catalog: cat }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `HTTP ${res.status}`);
    }
    const json = await res.json();
    return Array.isArray(json.media) ? json.media : [];
  }
  if (cat.type === 'custom' && cat.baseCatalog) {
    const baseMedia = await fetchCatalogPreviewMedia(cat.baseCatalog);
    const extraMedia = await fetchPreviewByIds((cat.includedMedia || []).map(ref => ref?.id));
    const combined = mergePreviewMedia(extraMedia, baseMedia);
    return cat.clientFilters ? _filterSourceMedia(combined, cat.clientFilters) : combined;
  }
  if (cat.type === 'custom') {
    const media = await fetchPreview({ ...filtersToVars(cat.filters || {}), isAdult: false });
    return cat.clientFilters ? _filterSourceMedia(media, cat.clientFilters) : media;
  }
  return [];
}

function setPreviewLoading(subtitle) {
  document.getElementById('preview-sub').textContent = subtitle || 'Loading…';
  document.getElementById('preview-area').innerHTML = '<div class="preview-loading"><div class="spinner"></div></div>';
}

function posterLabSeasonForDate(now = new Date()) {
  const month = now.getUTCMonth() + 1;
  const year = now.getUTCFullYear();
  if (month <= 3) return { season: 'WINTER', year };
  if (month <= 6) return { season: 'SPRING', year };
  if (month <= 9) return { season: 'SUMMER', year };
  return { season: 'FALL', year };
}

function posterLabStartDate(m) {
  const start = m && m.startDate ? m.startDate : {};
  if (!Number.isInteger(start.year) || !Number.isInteger(start.month) || !Number.isInteger(start.day)) return null;
  const dt = new Date(Date.UTC(start.year, start.month - 1, start.day));
  return Number.isNaN(dt.getTime()) ? null : dt;
}

function posterLabRelationTypes(m) {
  const relationTypes = new Set();
  const edges = (((m || {}).relations || {}).edges);
  if (!Array.isArray(edges)) return relationTypes;
  for (const edge of edges) {
    const nodeType = String(edge && edge.node && edge.node.type || '').toUpperCase();
    if (nodeType !== 'ANIME') continue;
    const relationType = String(edge && edge.relationType || '').toUpperCase();
    if (relationType) relationTypes.add(relationType);
  }
  return relationTypes;
}

function posterLabRankInfo(m) {
  const rankings = Array.isArray(m.rankings) ? m.rankings : [];
  const candidates = [];
  const popular = rankings.find(r => r && String(r.type || '').toUpperCase() === 'POPULAR' && r.allTime === true && Number.isInteger(r.rank) && r.rank <= 200);
  if (popular) candidates.push({ rank: popular.rank, label: 'Most Popular' });
  const rated = rankings.find(r => r && String(r.type || '').toUpperCase() === 'RATED' && r.allTime === true && Number.isInteger(r.rank) && r.rank <= 200);
  if (rated) candidates.push({ rank: rated.rank, label: 'Highest Rated' });
  if (candidates.length) {
    candidates.sort((a, b) => a.rank - b.rank);
    return { rank: candidates[0].rank, label: `#${candidates[0].rank} ${candidates[0].label}` };
  }
  return { rank: null, label: '' };
}

function posterLabRankFallbackLabel(m) {
  return posterLabRankInfo(m).label;
}

function posterLabTrendingIds(media) {
  const items = Array.isArray(media) ? media : [];
  const ranked = [];
  items.forEach((m, index) => {
    if (!m || !Number.isInteger(m.id) || !Number.isInteger(m.trending) || m.trending <= 0) return;
    ranked.push({ id: m.id, trending: m.trending, index });
  });
  ranked.sort((a, b) => (b.trending - a.trending) || (a.index - b.index));
  return new Set(ranked.slice(0, POSTER_LAB_TRENDING_TOP_N).map(item => item.id));
}

function posterLabTopLabel(m, media = null, trendingIds = null, now = new Date()) {
  const today = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  const current = posterLabSeasonForDate(now);
  const season = String(m && m.season || '').toUpperCase();
  const seasonYear = m ? m.seasonYear : null;
  const status = String(m && m.status || '').toUpperCase();
  const format = String(m && m.format || '').toUpperCase();
  const source = String(m && m.source || '').toUpperCase();
  const relationTypes = posterLabRelationTypes(m);
  const startDate = posterLabStartDate(m);
  const rankInfo = posterLabRankInfo(m);
  const startDeltaDays = startDate ? Math.round((startDate.getTime() - today.getTime()) / 86400000) : null;
  const startAgeDays = startDate ? Math.round((today.getTime() - startDate.getTime()) / 86400000) : null;
  const isCurrentSeasonRelease = (
    season === current.season &&
    seasonYear === current.year &&
    POSTER_LAB_SEASONAL_STATUSES.has(status)
  );

  if (rankInfo.rank !== null && rankInfo.rank <= POSTER_LAB_TOP_RANK_PRIORITY_LIMIT) {
    return rankInfo.label;
  }

  if (isCurrentSeasonRelease && [...relationTypes].some(type => POSTER_LAB_RETURNING_RELATIONS.has(type))) {
    return 'Returning Series';
  }
  if ([...relationTypes].some(type => POSTER_LAB_SPINOFF_RELATIONS.has(type))) {
    return 'Spin-off';
  }
  if (isCurrentSeasonRelease) {
    return 'New Season';
  }
  if (format === 'MOVIE' && startDeltaDays !== null && Math.abs(startDeltaDays) <= POSTER_LAB_MOVIE_PREMIERE_DAYS) {
    return 'Movie Premiere';
  }
  if (POSTER_LAB_SOURCE_LABELS[source]) {
    return POSTER_LAB_SOURCE_LABELS[source];
  }
  if (
    source &&
    source !== POSTER_LAB_ORIGINAL_SOURCE &&
    source !== POSTER_LAB_ANIME_SOURCE &&
    startAgeDays !== null &&
    startAgeDays >= 0 &&
    startAgeDays <= POSTER_LAB_RECENT_ADAPTATION_DAYS
  ) {
    return 'Recently Adapted';
  }
  if (source === POSTER_LAB_ORIGINAL_SOURCE) {
    return 'Original Anime';
  }

  const timeUntilAiring = m && m.nextAiringEpisode ? m.nextAiringEpisode.timeUntilAiring : null;
  if (
    status === 'RELEASING' &&
    Number.isInteger(timeUntilAiring) &&
    timeUntilAiring >= 0 &&
    timeUntilAiring <= POSTER_LAB_AIRS_THIS_WEEK_SECONDS
  ) {
    return 'Airs This Week';
  }

  const effectiveTrendingIds = trendingIds || (Array.isArray(media) ? posterLabTrendingIds(media) : new Set());
  if (Number.isInteger(m && m.id) && effectiveTrendingIds.has(m.id)) {
    return 'Trending Now';
  }

  return rankInfo.label;
}

function buildPosterLabTopLabelMap(media) {
  const items = Array.isArray(media) ? media : [];
  const trendingIds = posterLabTrendingIds(items);
  const now = new Date();
  const labels = new Map();
  for (const item of items) {
    if (!item || !Number.isInteger(item.id)) continue;
    const label = posterLabTopLabel(item, items, trendingIds, now);
    if (label) labels.set(item.id, label);
  }
  return labels;
}

function posterLabBottomLabel(m) {
  const genre = Array.isArray(m.genres) && m.genres.length ? m.genres[0] : '';
  const score = m.averageScore ? (m.averageScore / 10).toFixed(1) : '';
  if (genre && score) return `${genre}|${score}`;
  return genre || score || '';
}

function buildPosterLabImageUrl(m) {
  const cover = m.coverImage || {};
  const src = cover.extraLarge || cover.large;
  if (!src) return '';
  const params = new URLSearchParams({
    src,
    top: _posterLabTopLabelMap.get(m.id) || '',
    bottom: posterLabBottomLabel(m),
    badge: cover.color || '',
    style: normalizePosterStyle(posterStyle),
    v: POSTER_LAB_VERSION,
  });
  return `${BASE_URL}/poster-lab/render.png?${params.toString()}`;
}

function renderPreview(media, subtitle) {
  _lastMedia = media; _lastSubtitle = subtitle;
  _posterLabTopLabelMap = buildPosterLabTopLabelMap(media);
  document.getElementById('preview-sub').textContent = subtitle;
  const area = document.getElementById('preview-area');
  if (!media || !media.length) {
    area.innerHTML = '<div class="preview-prompt"><div class="preview-prompt-icon">&#128269;</div><div>No titles matched these filters</div></div>';
    return;
  }
  area.innerHTML = currentView === 'list' ? renderListView(media) : currentView === 'detail' ? renderDetailView(media) : renderGridView(media);
}

function renderGridView(media) {
  return '<div class="preview-grid">' + media.map(m => {
    const title  = escHtml(m.title.english || m.title.romaji || '');
    const score  = m.averageScore ? (m.averageScore / 10).toFixed(1) : '';
    const studio = ((m.studios && m.studios.nodes && m.studios.nodes[0]) || {}).name || '';
    const themeClass = studioThemeClass(studio);
    const scoreCls = scoreClass(m.averageScore || 0);
    const fallbackPoster = (m.coverImage || {}).extraLarge || (m.coverImage || {}).large || '';
    if (isPosterLabEnabled()) {
      const posterUrl = buildPosterLabImageUrl(m) || fallbackPoster;
      return `<a class="poster poster-lab-card" href="https://anilist.co/anime/${m.id}" target="_blank" rel="noopener noreferrer">
        <div class="poster-img">
          <img src="${escHtml(posterUrl)}" alt="${title}" loading="lazy" onerror="this.onerror=null;this.src='${escHtml(fallbackPoster)}';">
        </div>
        <div class="poster-title">${title}</div>
        <div class="poster-score">
          ${score ? `${ANILIST_MARK.replace('al-logo-badge', 'al-logo-badge poster-anilist-logo')}<span class="poster-score-value ${scoreCls}">${score}</span>` : ''}
        </div>
      </a>`;
    }
    const genres = (m.genres || []).slice(0, 3).map(g => {
      return `<span class="genre-badge ${genreBadgeClass(g, 'hard')}" data-genre="${escHtml(g)}">${escHtml(g)}</span>`;
    }).join('');
    const fmt    = FORMAT_LABELS[m.format] || m.format || '';
    const eps    = m.episodes ? m.episodes + ' ep' + (m.episodes !== 1 ? 's' : '') : '';
    const neutralTags = [fmt, eps].filter(Boolean).map(tag =>
      `<span class="poster-neutral-tag">${escHtml(tag)}</span>`
    ).join('');
    let metaSub = '';
    if (m.nextAiringEpisode) {
      const t = m.nextAiringEpisode.timeUntilAiring;
      const d = Math.floor(t / 86400), h = Math.floor(t / 3600);
      if (d > 0) metaSub = `Episode ${m.nextAiringEpisode.episode} in ${d} day${d === 1 ? '' : 's'}`;
      else metaSub = `Episode ${m.nextAiringEpisode.episode} in ${h} hour${h === 1 ? '' : 's'}`;
    }
    return `<a class="poster ${themeClass} ${metaSub ? 'has-banner' : ''}" href="https://anilist.co/anime/${m.id}" target="_blank" rel="noopener noreferrer">
      <div class="poster-img">
        <img src="${escHtml(fallbackPoster)}" alt="${title}" loading="lazy">
        <div class="poster-genres">${genres}</div>
        ${neutralTags ? `<div class="poster-bottom-tags">${neutralTags}</div>` : ''}
        ${metaSub ? `<div class="poster-meta"><div class="poster-meta-row">${escHtml(metaSub)}</div></div>` : ''}
      </div>
      <div class="poster-title">${title}</div>
      <div class="poster-score">
        ${score ? `${ANILIST_MARK.replace('al-logo-badge', 'al-logo-badge poster-anilist-logo')}<span class="poster-score-value ${scoreCls}">${score}</span>` : ''}
      </div>
    </a>`;
  }).join('') + '</div>';
}

function renderListView(media) {
  function airingText(nae) {
    if (!nae) return '';
    const t = nae.timeUntilAiring;
    const d = Math.floor(t / 86400), h = Math.floor(t / 3600);
    return `Episode ${nae.episode} in ${d > 0 ? d + ' day' + (d === 1 ? '' : 's') : h + ' hour' + (h === 1 ? '' : 's')}`;
  }
  return '<div class="preview-list">' + media.map(m => {
    const title   = escHtml(m.title.english || m.title.romaji || '');
    const score   = m.averageScore ? m.averageScore + '%' : '—';
    const scoreCls = scoreClass(m.averageScore || 0);
    const users   = m.popularity ? (m.popularity >= 1000 ? (m.popularity / 1000).toFixed(0) + 'K' : m.popularity) + ' users' : '';
    const format  = escHtml(FORMAT_LABELS[m.format] || m.format || '');
    const eps     = m.episodes ? m.episodes + ' ep' + (m.episodes !== 1 ? 's' : '') : '';
    const period  = [SEASON_LABELS[m.season], m.seasonYear].filter(Boolean).map(escHtml).join(' ');
    const airing  = escHtml(airingText(m.nextAiringEpisode));
    const statusL = escHtml(STATUS_LABELS[m.status] || m.status || '');
    const genres  = (m.genres || []).slice(0, 3).map(g => {
      return `<span class="genre-badge ${genreBadgeClass(g, 'soft')}" data-genre="${escHtml(g)}">${escHtml(g)}</span>`;
    }).join('');
    return `<a class="list-item" href="https://anilist.co/anime/${m.id}" target="_blank" rel="noopener noreferrer">
      <div class="list-thumb"><img src="${escHtml(m.coverImage.extraLarge || m.coverImage.large)}" alt="${title}" loading="lazy"></div>
      <div class="list-main">
        <div class="list-title">${title}</div>
        <div class="list-genres">${genres}</div>
      </div>
      <div class="list-score">
        <div class="list-score-pct">${ANILIST_MARK.replace('al-logo-badge', 'al-logo-badge list-al-icon')}<span class="list-score-value ${scoreCls}">${score}</span></div>
        <div class="list-stat">${users}</div>
      </div>
      <div class="list-meta-col">
        <div class="list-meta-primary">${format}</div>
        <div class="list-meta-secondary">${eps}</div>
      </div>
      <div class="list-meta-col">
        <div class="list-meta-primary">${period}</div>
        <div class="list-meta-secondary">${airing || statusL}</div>
      </div>
    </a>`;
  }).join('') + '</div>';
}

// ── View toggle ───────────────────────────────────
let _lastMedia = null;
let _lastSubtitle = '';

function setView(v) {
  currentView = v;
  document.getElementById('view-btn-grid').classList.toggle('active', v === 'grid');
  document.getElementById('view-btn-detail').classList.toggle('active', v === 'detail');
  document.getElementById('view-btn-list').classList.toggle('active', v === 'list');
  if (_lastMedia) renderPreview(_lastMedia, _lastSubtitle);
}

function syncPosterLabToggle() {
  document.querySelectorAll('.poster-style-btn[data-style]').forEach(btn => {
    const active = btn.dataset.style === posterStyle;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
}

function setPosterStyle(style) {
  posterStyle = normalizePosterStyle(style, 'off');
  syncPosterLabToggle();
  if (isPosterLabEnabled() && currentView !== 'grid') {
    setView('grid');
  } else if (_lastMedia) {
    renderPreview(_lastMedia, _lastSubtitle);
  }
  updateUrl();
}

function setPosterLabEnabled(enabled) {
  setPosterStyle(enabled ? POSTER_STYLE_DEFAULT : 'off');
}

function renderDetailView(media) {
  function airingStr(nae) {
    if (!nae) return null;
    const t = nae.timeUntilAiring;
    const d = Math.floor(t / 86400);
    const h = Math.floor((t % 86400) / 3600);
    const min = Math.floor((t % 3600) / 60);
    return { ep: nae.episode, time: d > 0 ? `${d} days, ${h} hours` : `${h} hours, ${min} mins` };
  }
  return '<div class="detail-grid">' + media.map(m => {
    const rawTitle = m.title.english || m.title.romaji || '';
    const title   = escHtml(rawTitle);
    const score   = m.averageScore || 0;
    const scoreCls = scoreClass(score);
    const fmt     = FORMAT_LABELS[m.format] || m.format || '';
    const eps     = m.episodes ? m.episodes + (m.episodes !== 1 ? ' episodes' : ' episode') : '';
    const meta    = [fmt, eps].filter(Boolean).join(' · ');
    const period  = [SEASON_LABELS[m.season], m.seasonYear].filter(Boolean).join(' ');
    const airing  = airingStr(m.nextAiringEpisode);
    const studio  = ((m.studios && m.studios.nodes && m.studios.nodes[0]) || {}).name || '';
    const themeClass = studioThemeClass(studio);
    const bannerLineClass = detailBannerLineClass(rawTitle);
    const desc    = m.description ? escHtml(m.description.replace(/<[^>]*>/g, '').replace(/\\n/g, ' ')) : '';
    const genres  = (m.genres || []).slice(0, 3).map(g => {
      return `<span class="genre-badge ${genreBadgeClass(g, 'soft')}" data-genre="${escHtml(g)}">${escHtml(g)}</span>`;
    }).join('');
    const scoreBadge = score ? `<div class="detail-score-badge ${detailScoreClass(score)}">${ANILIST_MARK.replace('al-logo-badge', 'al-logo-badge detail-score-icon')}<span class="detail-score-value">${score}%</span></div>` : '';
    const headerLeft = airing
      ? `<div class="detail-airing-label">Ep ${airing.ep} airing in</div><div class="detail-airing-time">${escHtml(airing.time)}</div>`
      : `<div class="detail-period">${escHtml(period)}</div>`;
    return `<a class="detail-card ${themeClass} ${bannerLineClass}" href="https://anilist.co/anime/${m.id}" target="_blank" rel="noopener noreferrer">
      <div class="detail-poster">
        <img src="${escHtml(m.coverImage.extraLarge || m.coverImage.large)}" alt="${title}" loading="lazy">
        <div class="detail-poster-overlay">
          <div class="detail-overlay-inner">
            <div class="detail-overlay-title">${title}</div>
            ${studio ? `<div class="detail-overlay-studio">${escHtml(studio)}</div>` : ''}
          </div>
        </div>
      </div>
      <div class="detail-body">
        <div class="detail-header">
          <div class="detail-header-left">${headerLeft}</div>
          ${scoreBadge}
        </div>
        <div class="detail-meta">${escHtml(meta)}</div>
        ${desc ? `<div class="detail-desc">${desc}</div>` : ''}
        <div class="detail-footer">
          <div class="detail-genres">${genres}</div>
        </div>
      </div>
    </a>`;
  }).join('') + '</div>';
}

// ── Genre pill click-to-filter ────────────────────
function applyGenreFilter(g) {
  if (!selectedGenres.includes(g)) selectedGenres.push(g);
  scheduleAutoPreview();
}

// ── Sort dropdown ─────────────────────────────────
function setSortValue(val) {
  document.getElementById('f-sort').value = val;
  closeSortMenu();
  renderSortBtn();
  scheduleAutoPreview();
}
function toggleSortMenu() {
  const menu = document.getElementById('sort-menu');
  const isOpen = menu.classList.contains('open');
  if (isOpen) { closeSortMenu(); } else {
    closeYearMenu();
    menu.classList.add('open');
    document.getElementById('sort-btn').classList.add('open');
  }
}
function closeSortMenu() {
  const menu = document.getElementById('sort-menu');
  if (menu) menu.classList.remove('open');
  const btn = document.getElementById('sort-btn');
  if (btn) btn.classList.remove('open');
}
document.addEventListener('click', e => {
  if (!document.getElementById('sort-dropdown')?.contains(e.target)) closeSortMenu();
  if (!document.getElementById('year-dropdown')?.contains(e.target)) closeYearMenu();
});

// ── Pane tab switch (Preview / Catalogs) ──────────
let currentPane = 'preview';
function setPaneTab(tab) {
  currentPane = tab;
  const isPreview = tab === 'preview';
  const isCatalogs = tab === 'catalogs';
  document.getElementById('tab-preview').classList.toggle('active', isPreview);
  document.getElementById('tab-catalogs').classList.toggle('active', isCatalogs);
  document.getElementById('preview-pane').classList.toggle('pane-hidden', !isPreview);
  document.getElementById('catalogs-pane').classList.toggle('catalogs-hidden', !isCatalogs);
  document.getElementById('preview-tab-extras').classList.toggle('pane-hidden', !isPreview);
  updateNameInput();
  scheduleFitCatalogsSidePane();
}

// ── Filter tags ───────────────────────────────────
function renderSortBtn() {
  const sort = document.getElementById('f-sort').value;
  const lbl = document.getElementById('sort-btn-label');
  if (lbl) lbl.textContent = SORT_LABELS[sort] || sort;
  document.querySelectorAll('.sort-menu-item').forEach(item => {
    item.classList.toggle('active', item.dataset.value === sort);
  });
}

function renderFilterTags() {
  const score = parseInt(document.getElementById('f-score').value);
  const daterange = getSelectedDateRangeValue();
  renderSortBtn();
  syncFilterBtnLabels();
  const contextTags = activePrototypePreview ? getPrototypeTags(activePrototypePreview) : [];
  const tags = [];
  // Source tag always appears first when an account/AI source is active
  if (activeSource && !activePrototypePreview?.uiBaseCatalogSnapshot) tags.push({ key: 'source', label: getSourceBaseName(activeSource) });
  selectedFormats.forEach(f  => tags.push({ key: 'format:'  + f, label: FORMAT_LABELS[f]  || f }));
  selectedSeasons.forEach(s  => tags.push({ key: 'season:'  + s, label: s === 'CURRENT' ? 'Current Season' : (SEASON_LABELS[s] || s) }));
  selectedYears.forEach(y    => tags.push({ key: 'year:'    + y, label: y }));
  selectedStatuses.forEach(s => tags.push({ key: 'status:'  + s, label: STATUS_LABELS[s] || s }));
  if (daterange) tags.push({ key: 'daterange', label: getDateRangeLabel(daterange) });
  if (score > 0) tags.push({ key: 'score', label: score + '+ score' });
  if (includeAdult) tags.push({ key: 'adult', label: 'Adult' });
  selectedGenres.forEach(g   => tags.push({ key: 'genre:'   + g, label: g }));

  const container = document.getElementById('filter-tags');
  container.innerHTML = contextTags.map(tag =>
    `<span class="filter-tag">${escHtml(tag.label)}${tag.key ? `<button class="filter-tag-x" type="button" data-action="remove-filter" data-key="${escHtml(tag.key)}">&#10005;</button>` : ''}</span>`
  ).join('') + tags.map(t =>
    `<span class="filter-tag">${escHtml(t.label)}<button class="filter-tag-x" type="button" data-action="remove-filter" data-key="${escHtml(t.key)}">&#10005;</button></span>`
  ).join('') + (tags.length ? '<button class="filter-tag-clear" type="button" data-action="clear-all-filters">Clear All &#10005;</button>' : '');
}

function removeFilter(key) {
  if (key === 'source') {
    // Removing the source tag clears the source and returns to normal filter preview
    activeSource = null;
    _sourceMedia = null;
    _lastSuggestedName = '';
    renderFilterTags();
    updateNameInput();
    scheduleAutoPreview();
    return;
  }
  if (key === 'prototype-title') {
    if (activePrototypePreview?.uiDraft && activePrototypePreview?.uiPrototypeMode === 'metadata') {
      clearPrototypePreview({ keepPreviewingId: true });
      _lastSuggestedName = '';
    }
    updateNameInput();
    scheduleAutoPreview();
    return;
  }
  if      (key === 'score')            { document.getElementById('f-score').value = 0; document.getElementById('score-val').textContent = 'Any'; }
  else if (key === 'adult')            { includeAdult = false; document.getElementById('f-adult').checked = false; document.getElementById('adult-toggle').classList.remove('active'); }
  else if (key.startsWith('genre:'))   { toggleMultiVal(selectedGenres,  key.slice(6)); }
  else if (key.startsWith('format:'))  { toggleMultiVal(selectedFormats, key.slice(7)); }
  else if (key.startsWith('status:'))  { toggleMultiVal(selectedStatuses,key.slice(7)); }
  else if (key.startsWith('year:'))    { toggleMultiVal(selectedYears,   key.slice(5)); }
  else if (key.startsWith('season:'))  { toggleMultiVal(selectedSeasons, key.slice(7)); }
  else if (key === 'daterange')        { document.getElementById('f-daterange').value = ''; }
  syncFilterBtnLabels();
  if (activeFbFilter) renderFilterOpts(activeFbFilter);
  renderFilterTags();
  updateNameInput();
  scheduleAutoPreview();
}

function onAdultChange() {
  includeAdult = document.getElementById('f-adult').checked;
  document.getElementById('adult-toggle').classList.toggle('active', includeAdult);
  renderFilterTags();
  updateNameInput();
  scheduleAutoPreview();
}

function clearAllFilters() {
  activeSource = null;
  _sourceMedia = null;
  _lastSuggestedName = '';
  activePrototypePreview = null;
  document.getElementById('f-sort').value = 'POPULARITY_DESC';
  document.getElementById('f-daterange').value = '';
  document.getElementById('f-score').value   = 0;
  document.getElementById('score-val').textContent = 'Any';
  includeAdult = false; document.getElementById('f-adult').checked = false; document.getElementById('adult-toggle').classList.remove('active');
  selectedGenres = []; selectedFormats = []; selectedStatuses = [];
  selectedYears  = []; selectedSeasons = [];
  syncFilterBtnLabels();
  if (activeFbFilter) renderFilterOpts(activeFbFilter);
  renderFilterTags();
  updateNameInput();
  scheduleAutoPreview();
}


function resolveSeasonVars(season, year) {
  if (season === 'CURRENT') {
    return { season: getCurrentSeason(), seasonYear: new Date().getFullYear() };
  }
  return {
    season: season || undefined,
    seasonYear: year ? parseInt(year) : undefined,
  };
}

function filtersToVars(filters) {
  if (!filters) return {};
  const v = {};
  const year = Array.isArray(filters.years) && filters.years.length === 1 ? filters.years[0] : filters.year;
  const season = Array.isArray(filters.seasons) && filters.seasons.length === 1 ? filters.seasons[0] : filters.season;
  if (filters.sort)                                 v.sort             = [filters.sort];
  if (filters.formats  && filters.formats.length)   v.format_in        = filters.formats;
  else if (filters.format)                          v.format_in        = [filters.format];
  if (filters.statuses && filters.statuses.length)  v.status_in        = filters.statuses;
  else if (filters.status)                          v.status_in        = [filters.status];
  if (season)                                       v.season           = season;
  if (year)                                         v.seasonYear       = parseInt(year, 10);
  if (filters.minScore)                             v.averageScore_greater = filters.minScore;
  if (filters.genres && filters.genres.length)      v.genre_in         = filters.genres;
  applyDateRangeToVariables(v, filters.daterange);
  return v;
}

// ── Preset form defaults ──────────────────────────
const PRESET_FORM_DEFAULTS = {
  'anilist-popular-season': { sort: 'POPULARITY_DESC', formats: [], seasons: ['CURRENT'], statuses: ['RELEASING'], score: 0, genres: [] },
  'anilist-airing-week':    { sort: 'TRENDING_DESC',   formats: [], seasons: [],          statuses: ['RELEASING'], score: 0, genres: [] },
  'anilist-trending':       { sort: 'TRENDING_DESC',   formats: [], seasons: [],          statuses: [],           score: 0, genres: [] },
  'anilist-top-rated':      { sort: 'SCORE_DESC',      formats: [], seasons: [],          statuses: [],           score: 0, genres: [] },
};

function loadFiltersIntoForm(f) {
  if (!f) return;
  document.getElementById('f-sort').value      = f.sort      || 'POPULARITY_DESC';
  document.getElementById('f-daterange').value = f.daterange || '';
  const score = f.score || f.minScore || 0;
  document.getElementById('f-score').value = score;
  document.getElementById('score-val').textContent = score > 0 ? score + '+' : 'Any';
  selectedGenres  = [...(f.genres   || [])];
  selectedFormats = f.formats  ? [...f.formats]  : (f.format  ? [f.format]  : []);
  selectedStatuses= f.statuses ? [...f.statuses] : (f.status  ? [f.status]  : []);
  selectedYears   = f.years    ? f.years.map(String) : (f.year ? [String(f.year)] : []);
  selectedSeasons = f.seasons  ? [...f.seasons]  : (f.season  ? [f.season]  : []);
  syncFilterBtnLabels();
  if (activeFbFilter) renderFilterOpts(activeFbFilter);
  renderFilterTags();
}

// ── Date range helpers ────────────────────────────
function getWeekStart() {
  const now = new Date();
  const diff = now.getDay() === 0 ? -6 : 1 - now.getDay(); // Monday
  const mon = new Date(now);
  mon.setDate(now.getDate() + diff);
  mon.setHours(0, 0, 0, 0);
  return mon;
}

function toFuzzyDate(d) {
  return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
}

function getSelectedDateRangeValue() {
  return document.getElementById('f-daterange')?.value || '';
}

function getDateRangeLabel(value) {
  const opt = (FILTER_OPTS.daterange || []).find(o => o.value === value);
  return opt ? opt.label : value;
}

function addDays(d, days) {
  const next = new Date(d);
  next.setDate(next.getDate() + days);
  return next;
}

function getDateRangeBounds(value) {
  if (!value) return null;
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();

  switch (value) {
    case 'this-week': {
      const start = getWeekStart();
      const end = addDays(start, 6);
      return { start, end };
    }
    case 'this-month':
      return { start: new Date(year, month, 1), end: new Date(year, month + 1, 0) };
    case 'last-month':
      return { start: new Date(year, month - 1, 1), end: new Date(year, month, 0) };
    case 'this-year':
      return { start: new Date(year, 0, 1), end: new Date(year, 11, 31) };
    case 'last-year':
      return { start: new Date(year - 1, 0, 1), end: new Date(year - 1, 11, 31) };
    default:
      return null;
  }
}

function applyDateRangeToVariables(variables, value) {
  delete variables.startDate_greater;
  delete variables.startDate_lesser;
  const bounds = getDateRangeBounds(value);
  if (!bounds) return;
  variables.startDate_greater = toFuzzyDate(addDays(bounds.start, -1));
  variables.startDate_lesser = toFuzzyDate(addDays(bounds.end, 1));
}

function mediaMatchesDateRange(media, value) {
  const bounds = getDateRangeBounds(value);
  if (!bounds) return true;
  const sd = media.startDate || {};
  if (!sd.year || !sd.month) return false;
  const fuzzy = sd.year * 10000 + sd.month * 100 + (sd.day || 1);
  return fuzzy >= toFuzzyDate(bounds.start) && fuzzy <= toFuzzyDate(bounds.end);
}

// Relative date filters use real calendar ranges via AniList FuzzyDateInt vars.
// The "Airing This Week" PRESET is still handled separately via airingSchedules.
function onDateRangeChange(el) {
  document.getElementById('f-daterange').value = el.value || '';
  renderFilterTags();
  updateNameInput();
  scheduleAutoPreview();
}

// ── Preset add / preview ──────────────────────────
async function addPreset(id, name) {
  if (activePrototypePreview) clearPrototypePreview();
  // Clicking a preset pill clears any active source tag
  activeSource = null;
  _sourceMedia = null;
  _lastSuggestedName = '';
  updateNameInput();
  const alreadyAdded = !!catalogs.find(c => c.id === id);
  if (!alreadyAdded) {
    catalogs.push({ id, name, type: 'preset' });
    render();
    setPaneTab('catalogs');
  } else {
    previewCatalog(id);
  }
}

// ── Custom preview ────────────────────────────────
function buildCurrentCustomFiltersFromForm() {
  const filters = {};
  const sort = document.getElementById('f-sort').value;
  const score = parseInt(document.getElementById('f-score').value);
  if (sort) filters.sort = sort;
  if (selectedFormats.length) filters.formats = [...selectedFormats];
  if (selectedStatuses.length) filters.statuses = [...selectedStatuses];
  if (selectedYears.length) filters.years = selectedYears.map(String);
  if (selectedSeasons.length) filters.seasons = [...selectedSeasons];
  if (score > 0) filters.minScore = score;
  if (selectedGenres.length) filters.genres = [...selectedGenres];
  const daterange = getSelectedDateRangeValue();
  if (daterange) filters.daterange = daterange;
  return filters;
}

async function previewActiveSearchDraft() {
  const draft = activePrototypePreview?.uiCatalogDraft;
  const subtitle = activePrototypePreview?.name || draft?.name || 'Search Preview';
  if (!draft || draft.type !== 'custom') {
    await previewCustom();
    return;
  }
  setPreviewLoading(subtitle);
  try {
    const media = await fetchPreview({ ...filtersToVars(buildCurrentCustomFiltersFromForm()), isAdult: includeAdult ? undefined : false });
    renderPreview(media, `${subtitle} — ${media.length} titles`);
  } catch(e) {
    console.error('[preview] Error:', e);
    document.getElementById('preview-sub').textContent = 'Failed to load preview';
    document.getElementById('preview-area').innerHTML =
      `<div class="preview-prompt"><div>Could not reach AniList API</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
  }
}

async function previewCustom() {
  setPreviewLoading('Loading…');
  try {
    const media = await fetchPreview({ ...filtersToVars(buildCurrentCustomFiltersFromForm()), isAdult: includeAdult ? undefined : false });
    renderPreview(media, `${media.length} titles`);
  } catch(e) {
    console.error('[preview] Error:', e);
    document.getElementById('preview-sub').textContent = 'Failed to load preview';
    document.getElementById('preview-area').innerHTML =
      `<div class="preview-prompt"><div>Could not reach AniList API</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
  }
}

// ── Add custom ────────────────────────────────────
function clearNameError() {
  const inp = document.getElementById('catalog-name');
  const err = document.getElementById('catalog-name-error');
  inp.classList.remove('input-error');
  err.classList.remove('visible');
}

function addCustom() {
  const nameInput = document.getElementById('catalog-name');
  const name = nameInput.value.trim();
  if (!name) {
    nameInput.classList.add('input-error');
    const errEl = document.getElementById('catalog-name-error');
    errEl.classList.add('visible');
    clearTimeout(errEl._hideTimer);
    errEl._hideTimer = setTimeout(() => clearNameError(), 2500);
    nameInput.focus();
    return;
  }

  if (activePrototypePreview?.uiDraft) {
    const draft = cloneJson(activePrototypePreview.uiCatalogDraft || {});
    let cat;
    if (draft.type === 'ai') {
      cat = {
        id: draft.id || freshCatalogId('ai'),
        name,
        type: 'ai',
        model: draft.model || _orModel || 'meta-llama/llama-3.3-70b-instruct',
        aiMode: draft.aiMode || 'title_seed',
        seedMediaId: draft.seedMediaId,
        seedTitle: draft.seedTitle,
      };
      if (draft.smartOptions) cat.smartOptions = cloneJson(draft.smartOptions);
      const clientFilters = _buildClientFilters();
      if (Object.keys(clientFilters).length) cat.clientFilters = clientFilters;
    } else {
      cat = {
        id: draft.id || freshCatalogId('custom'),
        name,
        type: 'custom',
        filters: buildCurrentCustomFiltersFromForm(),
      };
      const selected = activePrototypePreview.uiSelectedTitle;
      if (selected?.id || selected?.title) {
        cat.searchSeed = { id: selected.id || undefined, title: selected.title || name };
      }
    }
    catalogs.push(cat);
    document.getElementById('catalog-name').value = '';
    clearNameError();
    activePrototypePreview = null;
    activeSource = null;
    _sourceMedia = null;
    _lastSuggestedName = '';
    _clearAdditionalFilters();
    renderFilterTags();
    updateNameInput();
    render();
    setPaneTab('catalogs');
    return;
  }

  if (activeSource?.type === 'derived') {
    const cat = {
      id: freshCatalogId('custom'),
      name,
      type: 'custom',
      baseCatalog: sanitizeCatalogSnapshot(activeSource.baseCatalog),
      includedMedia: cloneJson(activeSource.includedMedia || []),
    };
    const clientFilters = _buildClientFilters();
    if (Object.keys(clientFilters).length) cat.clientFilters = clientFilters;
    catalogs.push(cat);

    document.getElementById('catalog-name').value = '';
    clearNameError();
    activePrototypePreview = null;
    activeSource = null;
    _sourceMedia = null;
    _lastSuggestedName = '';
    _clearAdditionalFilters();
    renderFilterTags();
    updateNameInput();
    render();
    setPaneTab('catalogs');
    return;
  }

  if (activeSource) {
    // Save a source-backed catalog. Additional filters are optional; when present
    // they are stored for the configure UI to replay on top of the source.
    const clientFilters = _buildClientFilters();
    const idPrefix = activeSource.type === 'ai' ? 'ai' : 'watch';
    const id = freshCatalogId(idPrefix);
    const cat = { id, name, type: activeSource.type };
    const sourceName = getSourceBaseName(activeSource);
    if (sourceName && sourceName !== name) cat.sourceName = sourceName;
    if (activeSource.listStatus) cat.listStatus = activeSource.listStatus;
    if (activeSource.type === 'ai') {
      if (_orModel) cat.model = _orModel;
      if (activeSource.aiMode) cat.aiMode = activeSource.aiMode;
      if (activeSource.seedMediaId) cat.seedMediaId = activeSource.seedMediaId;
      if (activeSource.seedTitle) cat.seedTitle = activeSource.seedTitle;
      if (activeSource.smartOptions) cat.smartOptions = JSON.parse(JSON.stringify(activeSource.smartOptions));
    }
    if (Object.keys(clientFilters).length) cat.clientFilters = clientFilters;
    catalogs.push(cat);

    document.getElementById('catalog-name').value = '';
    clearNameError();
    activeSource = null;
    _sourceMedia = null;
    _lastSuggestedName = '';
    _clearAdditionalFilters();
    renderFilterTags();
    updateNameInput();
    render();
    setPaneTab('catalogs');
    return;
  }

  // Standard custom catalog from AniList filter query
  const filters = buildCurrentCustomFiltersFromForm();
  const cat = { id: freshCatalogId('custom'), name, type: 'custom', filters };
  if (activePrototypePreview?.uiSelectedTitle?.id || activePrototypePreview?.uiSelectedTitle?.title) {
    cat.searchSeed = {
      id: activePrototypePreview.uiSelectedTitle.id || undefined,
      title: activePrototypePreview.uiSelectedTitle.title || name,
    };
  }
  catalogs.push(cat);

  document.getElementById('catalog-name').value = '';
  clearNameError();
  activePrototypePreview = null;
  document.getElementById('f-sort').value = 'POPULARITY_DESC';
  document.getElementById('f-daterange').value = '';
  document.getElementById('f-score').value = 0;
  document.getElementById('score-val').textContent = 'Any';
  selectedGenres = []; selectedFormats = []; selectedStatuses = [];
  selectedYears  = []; selectedSeasons = [];
  syncFilterBtnLabels();
  if (activeFbFilter) renderFilterOpts(activeFbFilter);

  render();
  setPaneTab('catalogs');
}

// ── Remove ────────────────────────────────────────
function removeCatalog(id) {
  catalogs = catalogs.filter(c => c.id !== id);
  if (previewingId === id) {
    previewingId = null;
    if (activePrototypePreview?.id === id) {
      activePrototypePreview = null;
      renderDefaultPreviewPrompt();
      renderFilterTags();
    }
  }
  render();
}

// ── Preview catalog row ───────────────────────────
let previewingId = null;
async function previewCatalog(id) {
  if (dragMoved) return;
  const cat = catalogs.find(c => c.id === id);
  if (!cat) return;
  previewingId = id;

  if (isUiPrototype(cat)) {
    openPrototypePreview(cat, { selectedId: cat.id });
    return;
  }

  if (activePrototypePreview) clearPrototypePreview({ keepPreviewingId: true });

  if (cat.type === 'custom' && cat.baseCatalog) {
    activePrototypePreview = {
      id: cat.id,
      uiBaseCatalogSnapshot: sanitizeCatalogSnapshot(cat.baseCatalog),
      uiSelectedTitle: snapshotSearchItem((cat.includedMedia && cat.includedMedia[0]) || cat.searchSeed || {}),
    };
    activeSource = {
      id: cat.id,
      name: cat.name,
      sourceName: cat.baseCatalog?.name || cat.name,
      previewName: cat.name,
      type: 'derived',
      baseCatalog: sanitizeCatalogSnapshot(cat.baseCatalog),
      includedMedia: cloneJson(cat.includedMedia || []),
    };
    _sourceMedia = null;
    _lastSuggestedName = '';
    _clearAdditionalFilters();
    if (hasStoredClientFilters(cat)) {
      loadFiltersIntoForm(cat.clientFilters);
    } else {
      renderFilterTags();
    }
    updateNameInput();
    setPaneTab('preview');
    render();
    setPreviewLoading(cat.name);
    try {
      _sourceMedia = await fetchCatalogPreviewMedia({ ...cloneJson(cat), clientFilters: null });
      _applySourcePreview();
    } catch(e) {
      console.error('[preview] Error:', e);
      document.getElementById('preview-sub').textContent = 'Failed to load preview';
      document.getElementById('preview-area').innerHTML =
        `<div class="preview-prompt"><div>Could not load this catalog</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
    }
    return;
  }

  if (cat.type === 'watching' || cat.type === 'ai') {
    // Set as active source so the tag bar shows the source tag and filters work on top
    activeSource = {
      id:          cat.id,
      name:        cat.name,
      sourceName:  cat.sourceName || getSourceBaseName(cat),
      previewName: cat.name,
      listStatus:  cat.listStatus,
      type:        cat.type,
    };
    if (cat.type === 'ai') {
      if (cat.aiMode) activeSource.aiMode = cat.aiMode;
      if (cat.seedMediaId) activeSource.seedMediaId = cat.seedMediaId;
      if (cat.seedTitle) activeSource.seedTitle = cat.seedTitle;
      if (cat.smartOptions) activeSource.smartOptions = JSON.parse(JSON.stringify(cat.smartOptions));
      if (cat.aiMode === 'title_seed' && (cat.seedTitle || cat.seedMediaId)) {
        activePrototypePreview = {
          id: cat.id,
          uiSelectedTitle: snapshotSearchItem({ id: cat.seedMediaId, title: cat.seedTitle }),
        };
      }
    }
    _sourceMedia = null;
    _lastSuggestedName = '';
    _clearAdditionalFilters();
    if (hasStoredClientFilters(cat)) {
      loadFiltersIntoForm(cat.clientFilters);
    } else {
      renderFilterTags();
    }
    updateNameInput();
    setPaneTab('preview');
    render();
    fetchAndShowSource();
    return;
  }

  // Preset or custom — clear source tag and show plain preview
  activeSource = null;
  _sourceMedia = null;
  _lastSuggestedName = '';
  _clearAdditionalFilters();
  if (cat.searchSeed) {
    activePrototypePreview = {
      id: cat.id,
      uiSelectedTitle: snapshotSearchItem(cat.searchSeed),
    };
  }
  renderFilterTags();
  updateNameInput();
  setPaneTab('preview');
  render();
  if (cat.type === 'preset') {
    loadFiltersIntoForm(PRESET_FORM_DEFAULTS[id]);
  } else {
    loadFiltersIntoForm(cat.filters);
  }
  setPreviewLoading(cat.name);
  if (cat.type === 'preset') {
    await previewPresetWithCurrentFilters(cat);
    return;
  }
  try {
    const media = await fetchPreview(filtersToVars(cat.filters));
    renderPreview(media, `${cat.name} — ${media.length} titles`);
  } catch(e) {
    console.error('[preview] Error:', e);
    document.getElementById('preview-sub').textContent = 'Failed to load preview';
    document.getElementById('preview-area').innerHTML =
      `<div class="preview-prompt"><div>Could not reach AniList API</div><div class="preview-error-detail">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
  }
}

// ── Auto-preview (debounced) ──────────────────────
let autoPreviewTimer = null;
function setPendingPreview() {
  document.getElementById('preview-sub').textContent = 'Updating…';
}
function scheduleAutoPreview() {
  if (currentPane === 'catalogs') setPaneTab('preview');
  setPendingPreview();
  renderFilterTags();
  updateNameInput();
  clearTimeout(autoPreviewTimer);
  if (activeSource) {
    if (_sourceMedia !== null) {
      // Source is loaded — apply filters client-side, no server fetch needed
      autoPreviewTimer = setTimeout(_applySourcePreview, 200);
    }
    // If _sourceMedia is null the in-flight fetchAndShowSource will call _applySourcePreview when done
  } else {
    const previewCat = catalogs.find(c => c.id === previewingId);
    if (previewCat && previewCat.type === 'preset') {
      autoPreviewTimer = setTimeout(() => previewPresetWithCurrentFilters(previewCat), 400);
    } else if (activePrototypePreview?.uiDraft && activePrototypePreview.uiCatalogDraft?.type === 'custom') {
      autoPreviewTimer = setTimeout(previewActiveSearchDraft, 500);
    } else {
      autoPreviewTimer = setTimeout(previewCustom, 1000);
    }
  }
}

// ── Randomize toggle ──────────────────────────────
function toggleRandomize(id) {
  const cat = catalogs.find(c => c.id === id);
  if (cat) { cat.randomize = !cat.randomize; render(); }
}

const SHUFFLE_ICON = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/></svg>`;
const SHUFFLE_TOOLTIP = 'Randomize catalog content - reshuffle every 6 hours';

// ── Render ────────────────────────────────────────
function render() {
  ['anilist-popular-season','anilist-airing-week','anilist-trending','anilist-top-rated'].forEach(id => {
    const card = document.getElementById('preset-' + id);
    if (card) card.classList.toggle('added', catalogs.some(c => c.id === id));
  });
  ACCOUNT_PRESET_IDS.forEach(id => {
    const card = document.getElementById('preset-' + id);
    if (card) card.classList.toggle('added', catalogs.some(c => c.id === id));
  });
  const list = document.getElementById('catalog-list');
  const countBadge = document.getElementById('catalog-count-badge');
  if (countBadge) {
    countBadge.textContent = catalogs.length + ' Catalog' + (catalogs.length !== 1 ? 's' : '');
    countBadge.classList.toggle('hidden', catalogs.length === 0);
  }
  if (catalogs.length === 0) {
    list.innerHTML = '<div class="empty-state"><div class="empty-icon">&#127916;</div><div>No catalogs yet.<br>Use Quick Add or the builder.</div></div>';
  } else {
    list.innerHTML = catalogs.map((c, i) => {
      const smartState = c.type === 'ai' ? getSmartRequirementState() : null;
      const smartClasses = smartState
        ? `${smartState.needsAniList ? 'smart-auth-missing' : ''} ${smartState.needsOpenRouter ? 'smart-key-missing' : ''} ${smartState.note ? 'smart-has-note' : ''}`
        : '';
      const smartTitle = smartState?.note ? ` title="${escHtml(smartState.note)}"` : '';
      const smartNote = smartState?.note ? `<div class="smart-missing-note">${escHtml(smartState.note)}</div>` : '';
      return `
      <div class="catalog-item ${previewingId === c.id ? 'active-preview' : ''} ${smartClasses}" draggable="true" data-id="${c.id}" data-index="${i}" data-action="preview-catalog"${smartTitle}>
        <span class="drag-handle">&#8597;</span>
        <div class="catalog-num">${i + 1}</div>
        <div class="catalog-item-info">
          ${renamingId === c.id
            ? `<input class="catalog-rename-input" data-rename-id="${c.id}" value="${escHtml(c.name)}">`
            : `<div class="catalog-item-name">${escHtml(c.name)}</div>`
          }
          <div class="catalog-item-type"><span class="catalog-type-badge${catalogTypeBadgeClass(c)}">${catalogTypeBadgeLabel(c)}</span></div>
        </div>
        <div class="catalog-actions">
          <button class="edit-btn" type="button" data-action="start-rename" data-id="${c.id}">&#9998; Rename</button>
          <button class="shuffle-btn ${c.randomize ? 'active' : ''}" type="button" data-action="toggle-randomize" data-id="${c.id}" title="${SHUFFLE_TOOLTIP}" aria-pressed="${c.randomize ? 'true' : 'false'}">${SHUFFLE_ICON} ${c.randomize ? 'Randomized' : 'Randomize'}</button>
          <button class="remove-btn" type="button" data-action="remove-catalog" data-id="${c.id}">&#128465; Remove</button>
        </div>
        ${smartNote}
      </div>
    `;
    }).join('');
  }

  renderSearchUi();
  updatePrototypeInstallNote();
  updateUrl();
  scheduleFitCatalogsSidePane();
}

function filterSummary(f) {
  if (!f) return 'Custom catalog';
  const parts = [];
  if (f.genres && f.genres.length) parts.push(f.genres.slice(0,2).join(', '));
  if (f.season) parts.push(f.season.charAt(0) + f.season.slice(1).toLowerCase());
  if (f.year)   parts.push(f.year);
  if (f.format) parts.push(f.format);
  if (f.minScore) parts.push('Score ' + f.minScore + '+');
  return parts.length ? parts.join(' · ') : 'Custom catalog';
}

// ── Rename catalog ────────────────────────────────
let renamingId = null;

function startRenaming(id) {
  renamingId = id;
  render();
  const inp = document.querySelector(`[data-rename-id="${id}"]`);
  if (inp) { inp.focus(); inp.select(); }
}

function commitRename(id, value) {
  if (renamingId !== id) return;
  const name = value.trim();
  if (name) {
    const cat = catalogs.find(c => c.id === id);
    if (cat) cat.name = name;
  }
  renamingId = null;
  render();
}

function cancelRename() {
  renamingId = null;
  render();
}

// ── Drag to reorder ───────────────────────────────
let dragIdx = null;
let dragMoved = false;

function dragStart(e, i) {
  dragIdx = i;
  dragMoved = true;
  e.dataTransfer.effectAllowed = 'move';
  // Delay so the drag ghost captures the normal appearance first
  setTimeout(() => {
    const items = document.querySelectorAll('.catalog-item');
    if (items[i]) items[i].classList.add('dragging');
  }, 0);
}
function dragOver(e, i) {
  e.preventDefault();
  document.querySelectorAll('.catalog-item').forEach(el => el.classList.remove('drag-over', 'shift-up', 'shift-down'));
  e.currentTarget.classList.add('drag-over');
  document.querySelectorAll('.catalog-item').forEach((el, idx) => {
    if (dragIdx === null || idx === i) return;
    if (dragIdx < i && idx > dragIdx && idx <= i) el.classList.add('shift-up');
    if (dragIdx > i && idx >= i && idx < dragIdx) el.classList.add('shift-down');
  });
}
function dragLeave(e) { e.currentTarget.classList.remove('drag-over'); }
function drop(e, i) {
  e.preventDefault();
  document.querySelectorAll('.catalog-item').forEach(el => el.classList.remove('drag-over', 'dragging', 'shift-up', 'shift-down'));
  dragMoved = false;
  if (dragIdx === null || dragIdx === i) { dragIdx = null; return; }
  const moved = catalogs.splice(dragIdx, 1)[0];
  catalogs.splice(i, 0, moved);
  dragIdx = null;
  render();
}
document.addEventListener('dragend', () => {
  dragMoved = false;
  document.querySelectorAll('.catalog-item').forEach(el => el.classList.remove('dragging', 'drag-over', 'shift-up', 'shift-down'));
});

// ── Import config from manifest URL ──────────────
// ── Shareable recipes ─────────────────────────────
const RECIPE_VERSION = 1;
let recipeModalMode = 'browse';
let activeRecipePayload = null;
let shareRecipeDraft = null;
let recipeCatalogUniverse = [];
let recipePreviewCatalogId = '';
let recipePreviewToken = 0;

function publicRecipeCatalogs(sourceCatalogs = catalogs) {
  return sourceCatalogs
    .filter(cat => cat && !isUiPrototype(cat) && !catalogRequiresAuth(cat) && !ACCOUNT_PRESET_IDS.has(cat.id))
    .map(cat => {
      const out = sanitizeCatalogSnapshot(cat);
      if (out) return out;
      return { id: cat.id, name: cat.name, type: cat.type || (PRESET_IDS.has(cat.id) ? 'preset' : 'custom') };
    });
}

function compactCatalogForRecipe(cat) {
  return compactCatalogEntry(cat);
}

function expandRecipeCatalogEntry(entry) {
  const cat = expandCatalogEntry(entry);
  if (cat?.id) return cat;
  return { id: freshRecipeCustomId(), name: 'Custom Recipe Catalog', type: 'custom', filters: {} };
}

function buildRecipePayload({ name, description = '', catalogs: recipeCatalogs, posterBanners = isPosterLabEnabled(), recipePosterStyle = POSTER_STYLE_DEFAULT, tags = [] }) {
  const resolvedStyle = posterBanners ? normalizePosterStyle(recipePosterStyle) : 'off';
  return {
    v: RECIPE_VERSION,
    n: (name || 'AniList Catalog Recipe').trim(),
    d: (description || '').trim(),
    b: resolvedStyle !== 'off',
    ps: resolvedStyle !== 'off' ? resolvedStyle : undefined,
    g: tags.slice(0, 6),
    c: publicRecipeCatalogs(recipeCatalogs).map(compactCatalogForRecipe),
  };
}

function recipeCatalogsFromPayload(recipe) {
  if (!recipe || !Array.isArray(recipe.c)) return [];
  return recipe.c.map(expandRecipeCatalogEntry).filter(cat => cat && cat.id);
}

function recipeCatalogTypeLabel(cat) {
  if (PRESET_IDS.has(cat.id)) return 'Preset';
  if (cat.filters?.genres?.length) return cat.filters.genres.slice(0, 2).join(', ');
  if (cat.filters?.formats?.length) return cat.filters.formats.map(f => FORMAT_LABELS[f] || f).join(', ');
  return 'Custom';
}

function renderRecipeCatalogList(recipe) {
  const cats = recipeCatalogsFromPayload(recipe);
  if (!cats.length) return '<div class="recipe-empty">No public catalogs in this recipe.</div>';
  return `<div class="recipe-list">${cats.map(cat => `
    <div class="recipe-list-item">
      <div>
        <div class="recipe-list-name">${escHtml(cat.name)}</div>
        <div class="recipe-list-meta">${escHtml(recipeCatalogTypeLabel(cat))}${cat.randomize ? ' · Randomized' : ''}</div>
      </div>
      <span class="recipe-chip">${PRESET_IDS.has(cat.id) ? 'Preset' : 'Custom'}</span>
    </div>
  `).join('')}</div>`;
}

function renderRecipeChips(recipe, extra = []) {
  const cats = recipeCatalogsFromPayload(recipe);
  const chips = [
    `${cats.length} catalog${cats.length === 1 ? '' : 's'}`,
    recipe.b ? `Posters: ${posterStyleLabel(recipe.ps || POSTER_STYLE_DEFAULT)}` : 'Posters off',
    ...(Array.isArray(recipe.g) ? recipe.g : []),
    ...extra,
  ].filter(Boolean);
  return `<div class="recipe-chip-row">${chips.map(chip => `<span class="recipe-chip">${escHtml(chip)}</span>`).join('')}</div>`;
}

async function encodeJsonPayload(payload) {
  const json = JSON.stringify(payload);
  let bytes;
  if (typeof CompressionStream !== 'undefined') {
    const stream = new CompressionStream('gzip');
    const writer = stream.writable.getWriter();
    writer.write(new TextEncoder().encode(json));
    writer.close();
    const chunks = [];
    const reader = stream.readable.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
    }
    const totalLen = chunks.reduce((n, c) => n + c.length, 0);
    bytes = new Uint8Array(totalLen);
    let off = 0;
    for (const chunk of chunks) { bytes.set(chunk, off); off += chunk.length; }
  } else {
    bytes = new TextEncoder().encode(json);
  }
  let binary = '';
  bytes.forEach(b => { binary += String.fromCharCode(b); });
  return btoa(binary).replace(/=/g,'').replace(/\\+/g,'-').replace(/\\//g,'_');
}

async function decodeJsonPayload(token) {
  let b64 = token.replace(/-/g, '+').replace(/_/g, '/');
  const pad = (4 - b64.length % 4) % 4;
  b64 += '='.repeat(pad);
  let bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  if (bytes[0] === 0x1f && bytes[1] === 0x8b) {
    if (typeof DecompressionStream === 'undefined') throw new Error('This browser cannot decode compressed recipes.');
    const stream = new DecompressionStream('gzip');
    const writer = stream.writable.getWriter();
    writer.write(bytes);
    writer.close();
    const chunks = [];
    const reader = stream.readable.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
    }
    const totalLen = chunks.reduce((n, c) => n + c.length, 0);
    const decompressed = new Uint8Array(totalLen);
    let off = 0;
    for (const chunk of chunks) { decompressed.set(chunk, off); off += chunk.length; }
    bytes = decompressed;
  }
  return JSON.parse(new TextDecoder().decode(bytes));
}

function recipeLinkFromToken(token) {
  return `${BASE_URL}/configure?recipe=${encodeURIComponent(token)}`;
}

function getRecipeTokenFromText(raw) {
  if (!raw) return '';
  try {
    const url = new URL(raw, BASE_URL);
    return url.searchParams.get('recipe') || '';
  } catch (_) {}
  const match = raw.match(/[?&]recipe=([^&\\s]+)/i);
  if (match) return decodeURIComponent(match[1]);
  if (/^[A-Za-z0-9_-]{20,}$/.test(raw)) return raw;
  return '';
}

function validateRecipePayload(payload) {
  if (!payload || typeof payload !== 'object') throw new Error('Invalid recipe.');
  if (!Array.isArray(payload.c) || !payload.c.length) throw new Error('No public catalogs found in this recipe.');
  const recipeStyle = payload.b ? normalizePosterStyle(payload.ps || payload.posterStyle || POSTER_STYLE_DEFAULT) : 'off';
  return {
    v: payload.v || RECIPE_VERSION,
    n: String(payload.n || 'AniList Catalog Recipe').slice(0, 80),
    d: String(payload.d || '').slice(0, 240),
    b: recipeStyle !== 'off',
    ps: recipeStyle !== 'off' ? recipeStyle : undefined,
    g: Array.isArray(payload.g) ? payload.g.map(String).slice(0, 6) : [],
    c: payload.c,
  };
}

function freshRecipeCustomId() {
  return 'custom-' + Math.random().toString(36).slice(2, 10);
}

function getActiveRecipeDraft() {
  if (recipeModalMode === 'share') return shareRecipeDraft;
  if (recipeModalMode === 'preview') return activeRecipePayload;
  return null;
}

function getRecipeDraftCatalogs() {
  return recipeCatalogsFromPayload(getActiveRecipeDraft());
}

function setRecipeDraftCatalogs(nextCatalogs) {
  const draft = getActiveRecipeDraft();
  if (!draft) return;
  draft.c = (nextCatalogs || []).map(compactCatalogForRecipe);
}

function getRecipeAvailableCatalogs() {
  const selectedIds = new Set(getRecipeDraftCatalogs().map(cat => cat.id));
  return recipeCatalogUniverse.filter(cat => cat && cat.id && !selectedIds.has(cat.id));
}

function sortRecipeCatalogsByUniverse(items) {
  const order = new Map(recipeCatalogUniverse.map((cat, index) => [cat.id, index]));
  return (items || []).slice().sort((a, b) => {
    const aIdx = order.has(a.id) ? order.get(a.id) : Number.MAX_SAFE_INTEGER;
    const bIdx = order.has(b.id) ? order.get(b.id) : Number.MAX_SAFE_INTEGER;
    return aIdx - bIdx;
  });
}

function syncShareRecipeDraftFromInputs() {
  if (recipeModalMode !== 'share' || !shareRecipeDraft) return;
  const nameInput = document.getElementById('recipe-name-input');
  const descInput = document.getElementById('recipe-desc-input');
  const nextName = String(nameInput?.value || shareRecipeDraft.n || 'My AniList Catalog Recipe').slice(0, 80).trim();
  const nextDesc = String(descInput?.value || shareRecipeDraft.d || '').slice(0, 240);
  shareRecipeDraft.n = nextName || 'My AniList Catalog Recipe';
  shareRecipeDraft.d = nextDesc;
}

function syncRecipePreviewSelection() {
  const cats = getRecipeDraftCatalogs();
  if (!cats.length) {
    recipePreviewCatalogId = '';
    return null;
  }
  if (!cats.some(cat => cat.id === recipePreviewCatalogId)) {
    recipePreviewCatalogId = cats[0].id;
  }
  return cats.find(cat => cat.id === recipePreviewCatalogId) || cats[0];
}

function renderEditableRecipeCatalogSection({ title, description = '', catalogs: sectionCatalogs, emptyText, action, actionLabel, actionClass }) {
  const rows = sectionCatalogs || [];
  return `
    <div class="recipe-section">
      <div class="recipe-section-head">
        <div>
          <div class="recipe-section-title">${escHtml(title)}</div>
          ${description ? `<div class="recipe-section-sub">${escHtml(description)}</div>` : ''}
        </div>
      </div>
      ${rows.length ? `<div class="recipe-list">${rows.map(cat => `
        <div class="recipe-list-item">
          <div class="recipe-list-copy">
            <div class="recipe-list-name">${escHtml(cat.name)}</div>
            <div class="recipe-list-meta">${escHtml(recipeCatalogTypeLabel(cat))}${cat.randomize ? ' · Randomized' : ''}</div>
          </div>
          <div class="recipe-list-actions">
            <span class="recipe-chip">${PRESET_IDS.has(cat.id) ? 'Preset' : 'Custom'}</span>
            <button class="${escHtml(actionClass)}" type="button" data-action="${escHtml(action)}" data-id="${escHtml(cat.id)}">${escHtml(actionLabel)}</button>
          </div>
        </div>
      `).join('')}</div>` : `<div class="recipe-empty">${escHtml(emptyText)}</div>`}
    </div>`;
}

function renderRecipePreviewPanel() {
  const cats = getRecipeDraftCatalogs();
  const selected = syncRecipePreviewSelection();
  return `
    <div class="recipe-preview-panel">
      <div class="recipe-preview-toolbar">
        <div>
          <div class="recipe-section-title">Preview</div>
          <div class="recipe-section-sub">This uses the same live preview strip as the Smart Row builder.</div>
        </div>
        ${cats.length > 1 ? `
          <label class="recipe-label recipe-preview-select-wrap" for="recipe-preview-select">
            Preview Catalog
            <select class="smart-select recipe-preview-select" id="recipe-preview-select">
              ${cats.map(cat => `<option value="${escHtml(cat.id)}"${cat.id === recipePreviewCatalogId ? ' selected' : ''}>${escHtml(cat.name)}</option>`).join('')}
            </select>
          </label>
        ` : selected ? `<div class="recipe-preview-selected">${escHtml(selected.name)}</div>` : ''}
      </div>
      <div class="recipe-preview-feedback" id="recipe-preview-feedback"></div>
      <div class="smart-inline-preview visible recipe-inline-preview" id="recipe-inline-preview">
        <div class="smart-preview-empty">${cats.length ? 'Loading preview...' : 'Add a catalog to preview this recipe.'}</div>
      </div>
    </div>`;
}

function materializeRecipeCatalogs(recipe, mode) {
  const existingIds = new Set(mode === 'add' ? catalogs.map(c => c.id) : []);
  const seen = new Set();
  const result = [];
  for (const source of recipeCatalogsFromPayload(recipe)) {
    const cat = JSON.parse(JSON.stringify(source));
    if (PRESET_IDS.has(cat.id)) {
      if (mode === 'add' && existingIds.has(cat.id)) continue;
    } else if (!cat.id || existingIds.has(cat.id) || seen.has(cat.id)) {
      cat.id = freshRecipeCustomId();
    }
    seen.add(cat.id);
    existingIds.add(cat.id);
    result.push(cat);
  }
  return result;
}

function getBuiltinRecipes() {
  const currentSeason = getCurrentSeason();
  const currentYear = new Date().getFullYear();
  return [
    buildRecipePayload({
      name: 'Shounen Weekend',
      description: 'Fast-moving action, seasonal heat, and a custom adventure lane for easy weekend browsing.',
      tags: ['Action', 'Weekend', 'TV'],
      posterBanners: true,
      catalogs: [
        { id: 'anilist-trending', name: 'Trending Now', type: 'preset', randomize: true },
        { id: 'anilist-popular-season', name: 'Popular This Season', type: 'preset' },
        { id: 'custom-shounen-weekend', name: 'Action Adventure Picks', type: 'custom', filters: { sort: 'POPULARITY_DESC', genres: ['Action', 'Adventure', 'Fantasy'], formats: ['TV'], minScore: 70 } },
      ],
    }),
    buildRecipePayload({
      name: 'Cozy Slice of Life',
      description: 'Gentler catalogs for low-stress watching, school days, music, comedy, and soft drama.',
      tags: ['Cozy', 'Slice of Life', 'Comedy'],
      posterBanners: false,
      catalogs: [
        { id: 'custom-cozy-slice', name: 'Cozy Slice of Life', type: 'custom', filters: { sort: 'SCORE_DESC', genres: ['Slice of Life', 'Comedy'], formats: ['TV', 'OVA', 'ONA'], minScore: 70 } },
        { id: 'custom-soft-drama', name: 'Soft Drama & Music', type: 'custom', filters: { sort: 'POPULARITY_DESC', genres: ['Drama', 'Music'], minScore: 70 } },
      ],
    }),
    buildRecipePayload({
      name: 'High Score Movies',
      description: 'Movie-first discovery sorted by score, with a second lane for popular feature-length picks.',
      tags: ['Movies', 'Score 75+', 'Film Night'],
      posterBanners: true,
      catalogs: [
        { id: 'custom-high-score-movies', name: 'High Score Movies', type: 'custom', filters: { sort: 'SCORE_DESC', formats: ['MOVIE'], minScore: 75 } },
        { id: 'custom-popular-movies', name: 'Popular Anime Movies', type: 'custom', filters: { sort: 'POPULARITY_DESC', formats: ['MOVIE'], minScore: 65 } },
      ],
    }),
    buildRecipePayload({
      name: 'Current Season No Sequels',
      description: 'Current-season TV discovery that works nicely with the add-on season-one replacement behavior.',
      tags: ['Seasonal', 'TV', 'No Sequels'],
      posterBanners: true,
      catalogs: [
        { id: 'anilist-popular-season', name: 'Popular This Season', type: 'preset' },
        { id: 'custom-current-season-tv', name: 'Current Season TV', type: 'custom', filters: { sort: 'POPULARITY_DESC', season: currentSeason, year: currentYear, statuses: ['RELEASING'], formats: ['TV'] } },
      ],
    }),
    buildRecipePayload({
      name: 'Hidden Gems',
      description: 'A smaller, score-forward bundle for finished shows and OVAs outside the usual trending lanes.',
      tags: ['Hidden Gems', 'Finished', 'Score 75+'],
      posterBanners: false,
      catalogs: [
        { id: 'custom-hidden-gems-tv', name: 'Finished High Score TV', type: 'custom', filters: { sort: 'SCORE_DESC', statuses: ['FINISHED'], formats: ['TV'], minScore: 75 } },
        { id: 'custom-hidden-gems-ova', name: 'OVA & ONA Gems', type: 'custom', filters: { sort: 'SCORE_DESC', statuses: ['FINISHED'], formats: ['OVA', 'ONA'], minScore: 72 } },
      ],
    }),
  ];
}

function setRecipeModalOpen(open) {
  const overlay = document.getElementById('recipe-modal-overlay');
  if (!overlay) return;
  overlay.classList.toggle('open', !!open);
  if (open) setTimeout(() => overlay.querySelector('input, textarea, button')?.focus(), 0);
}

function closeRecipeModal() {
  setRecipeModalOpen(false);
  activeRecipePayload = null;
  shareRecipeDraft = null;
  recipeCatalogUniverse = [];
  recipePreviewCatalogId = '';
  recipePreviewToken += 1;
}

function removeCatalogFromRecipeDraft(catalogId) {
  if (recipeModalMode === 'share') syncShareRecipeDraftFromInputs();
  const nextCatalogs = getRecipeDraftCatalogs().filter(cat => cat.id !== catalogId);
  setRecipeDraftCatalogs(nextCatalogs);
  syncRecipePreviewSelection();
  renderRecipeModal();
}

function addCatalogToRecipeDraft(catalogId) {
  if (recipeModalMode === 'share') syncShareRecipeDraftFromInputs();
  const catalogToAdd = recipeCatalogUniverse.find(cat => cat.id === catalogId);
  if (!catalogToAdd) return;
  const nextCatalogs = getRecipeDraftCatalogs();
  if (nextCatalogs.some(cat => cat.id === catalogId)) return;
  nextCatalogs.push(cloneJson(catalogToAdd));
  setRecipeDraftCatalogs(sortRecipeCatalogsByUniverse(nextCatalogs));
  syncRecipePreviewSelection();
  renderRecipeModal();
}

function renderInlinePreviewInto(preview, media, catalog, { emptyMessage = 'No titles matched this preview.' } = {}) {
  if (!preview) return;
  preview.classList.add('visible');
  if (!media || !media.length) {
    preview.innerHTML = `<div class="smart-preview-empty">${escHtml(emptyMessage)}</div>`;
    return;
  }
  const cards = media.map(m => {
    const title = escHtml((m.title && (m.title.english || m.title.romaji || m.title.native)) || 'Untitled');
    const poster = escHtml((m.coverImage && (m.coverImage.extraLarge || m.coverImage.large || m.coverImage.medium)) || '');
    const href = m.id ? `https://anilist.co/anime/${m.id}` : '#';
    return `<a class="smart-preview-card" href="${escHtml(href)}" target="_blank" rel="noopener noreferrer">
      <div class="smart-preview-poster">${poster ? `<img src="${poster}" alt="${title}" loading="lazy">` : ''}</div>
      <div class="smart-preview-name">${title}</div>
    </a>`;
  }).join('');
  preview.innerHTML = `
    <div class="smart-preview-head">
      <div class="smart-preview-title">${escHtml(catalog?.name || 'Preview')}</div>
      <div class="smart-preview-count">${media.length} title${media.length === 1 ? '' : 's'}</div>
    </div>
    <div class="smart-preview-strip">${cards}</div>`;
}

function renderInlinePreviewStatusInto(preview, message) {
  if (!preview) return;
  preview.classList.add('visible');
  preview.innerHTML = `<div class="smart-preview-empty">${escHtml(message)}</div>`;
}

async function refreshRecipePreview() {
  const preview = document.getElementById('recipe-inline-preview');
  const feedback = document.getElementById('recipe-preview-feedback');
  const draft = getActiveRecipeDraft();
  if (!preview || !draft) return;
  const selected = syncRecipePreviewSelection();
  if (!selected) {
    renderInlinePreviewStatusInto(preview, 'Add a catalog to preview this recipe.');
    if (feedback) {
      feedback.textContent = '';
      feedback.className = 'recipe-preview-feedback';
    }
    return;
  }
  const token = ++recipePreviewToken;
  renderInlinePreviewStatusInto(preview, 'Loading preview...');
  if (feedback) {
    feedback.textContent = '';
    feedback.className = 'recipe-preview-feedback';
  }
  try {
    const media = await fetchCatalogPreviewMedia(selected);
    if (token != recipePreviewToken) return;
    renderInlinePreviewInto(preview, media, selected, { emptyMessage: 'No titles came back for this recipe catalog.' });
    if (feedback) {
      feedback.textContent = `${selected.name} preview ready with ${media.length} title${media.length === 1 ? '' : 's'}.`;
      feedback.className = 'recipe-preview-feedback ok';
    }
  } catch (e) {
    if (token != recipePreviewToken) return;
    renderInlinePreviewStatusInto(preview, 'Preview failed. Try another catalog.');
    if (feedback) {
      feedback.textContent = e instanceof Error ? e.message : String(e);
      feedback.className = 'recipe-preview-feedback err';
    }
  }
}

function renderRecipeModal() {
  const titleEl = document.getElementById('recipe-modal-title');
  const bodyEl = document.getElementById('recipe-modal-body');
  const footerEl = document.getElementById('recipe-modal-footer');
  if (!titleEl || !bodyEl || !footerEl) return;

  if (recipeModalMode === 'share') {
    const skipped = catalogs.length - publicRecipeCatalogs().length;
    titleEl.textContent = 'Share Recipe';
    if (!recipeCatalogUniverse.length) {
      bodyEl.innerHTML = '<div class="recipe-empty">No public catalogs to share. Recipes omit AniList account and AI catalogs so private auth-powered setup stays private.</div>';
      footerEl.innerHTML = '<button class="btn btn-ghost" data-action="close-recipe-modal">Close</button>';
      return;
    }
    const selectedCatalogs = getRecipeDraftCatalogs();
    const availableCatalogs = getRecipeAvailableCatalogs();
    bodyEl.innerHTML = `
      <div class="recipe-form-grid">
        <label class="recipe-label" for="recipe-name-input">Recipe Name</label>
        <input class="recipe-input" id="recipe-name-input" value="${escHtml(shareRecipeDraft.n)}" maxlength="80">
        <label class="recipe-label" for="recipe-desc-input">Description</label>
        <textarea class="recipe-textarea" id="recipe-desc-input" maxlength="240" placeholder="Optional note for whoever imports this recipe">${escHtml(shareRecipeDraft.d || '')}</textarea>
      </div>
      <div class="recipe-summary">
        ${renderRecipeChips(shareRecipeDraft, skipped ? [`${skipped} private omitted`] : [])}
      </div>
      ${renderEditableRecipeCatalogSection({
        title: 'In this recipe',
        description: 'These catalogs will be included in the recipe link. Removing one here does not touch Your Catalogs.',
        catalogs: selectedCatalogs,
        emptyText: 'This recipe draft does not include any catalogs yet.',
        action: 'remove-recipe-catalog',
        actionLabel: 'Remove',
        actionClass: 'btn btn-ghost btn-sm',
      })}
      ${availableCatalogs.length ? renderEditableRecipeCatalogSection({
        title: 'Available to add back',
        description: 'Removed catalogs stay here so you can put them back before copying the link.',
        catalogs: availableCatalogs,
        emptyText: '',
        action: 'add-recipe-catalog',
        actionLabel: 'Add back',
        actionClass: 'btn btn-primary btn-sm',
      }) : ''}
      ${renderRecipePreviewPanel()}
      <div class="recipe-feedback" id="recipe-feedback"></div>`;
    footerEl.innerHTML = `<button class="btn btn-ghost" data-action="close-recipe-modal">Cancel</button><button class="btn btn-primary" data-action="copy-recipe-link"${selectedCatalogs.length ? '' : ' disabled'}>Copy Recipe Link</button>`;
    refreshRecipePreview();
    return;
  }

  if (recipeModalMode === 'browse') {
    titleEl.textContent = 'Browse Recipes';
    const recipes = getBuiltinRecipes();
    bodyEl.innerHTML = `<div class="recipe-gallery">${recipes.map((recipe, idx) => `
      <div class="recipe-card">
        <div class="recipe-card-title">${escHtml(recipe.n)}</div>
        <div class="recipe-card-desc">${escHtml(recipe.d)}</div>
        ${renderRecipeChips(recipe)}
        <div class="recipe-card-actions">
          <button class="btn btn-ghost btn-sm btn-full" data-action="preview-builtin-recipe" data-index="${idx}">Preview</button>
          <button class="btn btn-primary btn-sm btn-full" data-action="add-builtin-recipe" data-index="${idx}">Add</button>
        </div>
      </div>
    `).join('')}</div>`;
    footerEl.innerHTML = '<button class="btn btn-ghost" data-action="close-recipe-modal">Close</button>';
    return;
  }

  const recipe = activeRecipePayload;
  const selectedCatalogs = getRecipeDraftCatalogs();
  const availableCatalogs = getRecipeAvailableCatalogs();
  titleEl.textContent = 'Recipe Preview';
  bodyEl.innerHTML = `
    <div class="recipe-summary">
      <div class="recipe-summary-title">${escHtml(recipe.n)}</div>
      ${recipe.d ? `<div class="recipe-summary-desc">${escHtml(recipe.d)}</div>` : ''}
      ${renderRecipeChips(recipe)}
    </div>
    ${renderEditableRecipeCatalogSection({
      title: 'In this recipe',
      description: 'Remove catalogs you do not want to add right now. They stay available to add back in this window.',
      catalogs: selectedCatalogs,
      emptyText: 'This recipe currently has no catalogs selected.',
      action: 'remove-recipe-catalog',
      actionLabel: 'Remove',
      actionClass: 'btn btn-ghost btn-sm',
    })}
    ${availableCatalogs.length ? renderEditableRecipeCatalogSection({
      title: 'Available to add back',
      description: 'These are the recipe catalogs you removed from the current draft.',
      catalogs: availableCatalogs,
      emptyText: '',
      action: 'add-recipe-catalog',
      actionLabel: 'Add back',
      actionClass: 'btn btn-primary btn-sm',
    }) : ''}
    ${renderRecipePreviewPanel()}
    <div class="recipe-mini-note">Add appends new catalogs and skips duplicate preset lanes. Replace swaps your current setup to this recipe.</div>`;
  footerEl.innerHTML = `<button class="btn btn-ghost" data-action="close-recipe-modal">Cancel</button><button class="btn btn-ghost" data-action="apply-recipe" data-mode="add"${selectedCatalogs.length ? '' : ' disabled'}>Add to current</button><button class="btn btn-primary" data-action="apply-recipe" data-mode="replace"${selectedCatalogs.length ? '' : ' disabled'}>Replace current</button>`;
  refreshRecipePreview();
}

function openShareRecipeModal() {
  recipeModalMode = 'share';
  activeRecipePayload = null;
  recipeCatalogUniverse = publicRecipeCatalogs();
  shareRecipeDraft = buildRecipePayload({
    name: 'My AniList Catalog Recipe',
    description: '',
    catalogs: recipeCatalogUniverse,
    posterBanners: isPosterLabEnabled(),
    recipePosterStyle: posterStyle,
  });
  recipePreviewCatalogId = recipeCatalogUniverse[0]?.id || '';
  renderRecipeModal();
  setRecipeModalOpen(true);
}

function openRecipeGallery() {
  recipeModalMode = 'browse';
  activeRecipePayload = null;
  shareRecipeDraft = null;
  recipeCatalogUniverse = [];
  recipePreviewCatalogId = '';
  renderRecipeModal();
  setRecipeModalOpen(true);
}

function openRecipePreview(recipe) {
  const validated = validateRecipePayload(recipe);
  activeRecipePayload = cloneJson(validated);
  recipeCatalogUniverse = cloneJson(recipeCatalogsFromPayload(validated));
  recipePreviewCatalogId = recipeCatalogUniverse[0]?.id || '';
  recipeModalMode = 'preview';
  renderRecipeModal();
  setRecipeModalOpen(true);
}

async function copyRecipeLink() {
  syncShareRecipeDraftFromInputs();
  const feedback = document.getElementById('recipe-feedback');
  const recipe = buildRecipePayload({
    name: shareRecipeDraft?.n || 'My AniList Catalog Recipe',
    description: shareRecipeDraft?.d || '',
    catalogs: getRecipeDraftCatalogs(),
    posterBanners: isPosterLabEnabled(),
    recipePosterStyle: posterStyle,
  });
  if (!recipe.c.length) {
    if (feedback) {
      feedback.textContent = 'Add at least one catalog to this recipe before copying the link.';
      feedback.className = 'recipe-feedback err';
    }
    return;
  }
  try {
    const token = await encodeJsonPayload(recipe);
    await navigator.clipboard.writeText(recipeLinkFromToken(token));
    if (feedback) { feedback.textContent = 'Recipe link copied.'; feedback.className = 'recipe-feedback ok'; }
  } catch (e) {
    if (feedback) { feedback.textContent = e instanceof Error ? e.message : String(e); feedback.className = 'recipe-feedback err'; }
  }
}

function applyRecipe(recipe, mode) {
  const validated = validateRecipePayload(recipe);
  const incoming = materializeRecipeCatalogs(validated, mode);
  if (!incoming.length) return;
  if (mode === 'replace') catalogs = incoming;
  else catalogs = catalogs.concat(incoming);
  posterStyle = validated.b ? normalizePosterStyle(validated.ps || POSTER_STYLE_DEFAULT) : 'off';
  syncPosterLabToggle();
  setPaneTab('catalogs');
  closeRecipeModal();
  render();
}

async function importRecipeToken(token) {
  const payload = validateRecipePayload(await decodeJsonPayload(token));
  openRecipePreview(payload);
}

async function openInitialRecipeIfPresent() {
  const token = _urlParams.get('recipe');
  if (!token) return;
  try {
    await importRecipeToken(token);
    const cleanUrl = new URL(window.location.href);
    cleanUrl.searchParams.delete('recipe');
    window.history.replaceState({}, '', cleanUrl.toString());
  } catch (e) {
    const fb = document.getElementById('import-feedback');
    if (fb) {
      fb.textContent = '✗ ' + (e instanceof Error ? e.message : String(e));
      fb.className = 'visible err';
    }
  }
}

async function importConfig() {
  const raw = document.getElementById('import-url').value.trim();
  const fb  = document.getElementById('import-feedback');
  fb.className = '';

  try {
    const recipeToken = getRecipeTokenFromText(raw);
    if (recipeToken) {
      await importRecipeToken(recipeToken);
      document.getElementById('import-url').value = '';
      fb.textContent = '✓ Recipe ready to preview';
      fb.className = 'visible ok';
      setTimeout(() => { fb.className = ''; }, 3000);
      return;
    }

    // Pull the path segment from any URL shaped like /{segment}/manifest.json
    // or /{segment}/poster-lab/manifest.json.
    // The segment may be "{config_token}" or "{config_token}~{session_key}".
    const match = raw.match(/\\/([A-Za-z0-9+=_~-]+)\\/(?:poster-lab\\/)?manifest\\.json/i);
    if (!match) throw new Error('No config token found — paste a full manifest URL');
    const importedPosterLab = /\\/poster-lab\\/manifest\\.json/i.test(raw);

    const [configPart, sessionPart] = match[1].split('~');

    // Restore standard base64 from URL-safe base64
    let b64 = configPart.replace(/-/g, '+').replace(/_/g, '/');
    const pad = (4 - b64.length % 4) % 4;
    b64 += '='.repeat(pad);

    // Decode bytes, then decompress if gzip magic bytes are present.
    let bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    if (bytes[0] === 0x1f && bytes[1] === 0x8b && typeof DecompressionStream !== 'undefined') {
      const stream = new DecompressionStream('gzip');
      const writer = stream.writable.getWriter();
      writer.write(bytes);
      writer.close();
      const chunks = [];
      const reader = stream.readable.getReader();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
      }
      const totalLen = chunks.reduce((n, c) => n + c.length, 0);
      const decompressed = new Uint8Array(totalLen);
      let off = 0;
      for (const chunk of chunks) { decompressed.set(chunk, off); off += chunk.length; }
      bytes = decompressed;
    }
    const parsed = JSON.parse(new TextDecoder().decode(bytes));

    let config;
    if (parsed && Array.isArray(parsed.c)) {
      // Compact format: expand back to full catalog objects
      config = { catalogs: parsed.c.map(expandCatalogEntry).filter(cat => cat && cat.id) };
      if (parsed.ps) config.posterStyle = normalizePosterStyle(parsed.ps);
    } else {
      config = parsed;
    }

    if (!config || !Array.isArray(config.catalogs)) throw new Error('Invalid configuration data');
    if (!config.catalogs.length) throw new Error('No catalogs found in this config');

    catalogs = config.catalogs;
    posterStyle = importedPosterLab ? normalizePosterStyle(config.posterStyle || config.poster_style || POSTER_STYLE_DEFAULT) : 'off';
    syncPosterLabToggle();
    // Restore the auth key from the imported URL if present.
    // If the key was revoked or the auth DB was lost, the user will need to reconnect.
    if (sessionPart && sessionPart !== _sessionKey) {
      _sessionKey = sessionPart;
      fetchMe(); // validate against /api/me and render auth UI
    }
    document.getElementById('import-url').value = '';
    render();

    const n = catalogs.length;
    fb.textContent = '✓ Imported ' + n + ' catalog' + (n !== 1 ? 's' : '');
    fb.className = 'visible ok';
    setTimeout(() => { fb.className = ''; }, 3000);
  } catch(e) {
    fb.textContent = '✗ ' + e.message;
    fb.className = 'visible err';
  }
}

// ── URL generation ────────────────────────────────
let _currentManifestUrl = '';
let _qrInstance = null;

async function updateUrl() {
  const compact = supportedCatalogs().map(compactCatalogEntry);
  // The auth key is NOT embedded in the payload — it travels as a path suffix.
  const payload = { c: compact };
  if (isPosterLabEnabled() && normalizePosterStyle(posterStyle) !== POSTER_STYLE_DEFAULT) {
    payload.ps = normalizePosterStyle(posterStyle);
  }
  const json = JSON.stringify(payload);

  let configToken;
  if (typeof CompressionStream !== 'undefined') {
    // Gzip-compress the JSON before base64url-encoding for shorter URLs.
    const stream = new CompressionStream('gzip');
    const writer = stream.writable.getWriter();
    writer.write(new TextEncoder().encode(json));
    writer.close();
    const chunks = [];
    const reader = stream.readable.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
    }
    const totalLen = chunks.reduce((n, c) => n + c.length, 0);
    const bytes = new Uint8Array(totalLen);
    let off = 0;
    for (const chunk of chunks) { bytes.set(chunk, off); off += chunk.length; }
    let binary = '';
    bytes.forEach(b => { binary += String.fromCharCode(b); });
    configToken = btoa(binary).replace(/=/g,'').replace(/\\+/g,'-').replace(/\\//g,'_');
  } else {
    // Fallback for browsers without CompressionStream (rare).
    let binary = '';
    new TextEncoder().encode(json).forEach(b => { binary += String.fromCharCode(b); });
    configToken = btoa(binary).replace(/=/g,'').replace(/\\+/g,'-').replace(/\\//g,'_');
  }

  // Append the auth key with '~' separator when authenticated.
  // '~' is unreserved in RFC 3986 and never appears in base64url output.
  const segment = _sessionKey ? `${configToken}~${_sessionKey}` : configToken;
  const manifestPath = isPosterLabEnabled() ? 'poster-lab/manifest.json' : 'manifest.json';
  const url = `${BASE_URL}/${segment}/${manifestPath}`;
  _currentManifestUrl = url;
  document.getElementById('url-display').textContent = url;
  const tw = document.getElementById('token-warning');
  if (tw) tw.classList.toggle('show', !!_sessionKey);
  updateQrCode(url);
}

function updateQrCode(url) {
  const wrap = document.getElementById('qr-canvas-wrap');
  if (!wrap) return;
  wrap.innerHTML = '';
  if (typeof QRCode === 'undefined' || !url || url === '—') return;

  const qr = new QRCode(wrap, {
    text: url,
    width: 180,
    height: 180,
    colorDark: '#ffffff',
    colorLight: '#1c1c1e',
    correctLevel: QRCode.CorrectLevel.M,
  });
}

function fitCatalogsSidePane() {
  const sideCol = document.querySelector('.catalogs-side-col');
  if (!sideCol) return;
  sideCol.classList.remove('compact');
  sideCol.style.removeProperty('--install-qr-size');
  if (window.innerWidth <= 768) return;
  if (currentPane !== 'catalogs') return;

  const fits = () => sideCol.scrollHeight <= sideCol.clientHeight + 1;
  if (fits()) return;

  sideCol.classList.add('compact');
  let size = 148;
  sideCol.style.setProperty('--install-qr-size', size + 'px');
  while (size > 104 && !fits()) {
    size -= 8;
    sideCol.style.setProperty('--install-qr-size', size + 'px');
  }
}

function scheduleFitCatalogsSidePane() {
  requestAnimationFrame(() => fitCatalogsSidePane());
}

function openInStremio() {
  openManifestUrlInStremio(_currentManifestUrl);
}

function openManifestUrlInStremio(url) {
  if (!url) return;
  const stremioUrl = url.replace(/^https?:\\/\\//, 'stremio://');
  window.location.href = stremioUrl;
}

async function copyUrl() {
  const url = _currentManifestUrl || document.getElementById('url-display').textContent;
  await navigator.clipboard.writeText(url);
  const btn = document.getElementById('copy-url-btn');
  btn.textContent = 'Copied';
  btn.disabled = true;
  setTimeout(() => { btn.textContent = 'Copy URL'; btn.disabled = false; }, 2000);
}

// ── Init ──────────────────────────────────────────
function bindStaticUiEvents() {
  const scoreInput = document.getElementById('f-score');
  if (scoreInput) {
    scoreInput.addEventListener('input', e => {
      const score = parseInt(e.target.value, 10) || 0;
      document.getElementById('score-val').textContent = score > 0 ? score + '+' : 'Any';
      scheduleAutoPreview();
    });
  }

  const adultInput = document.getElementById('f-adult');
  if (adultInput) adultInput.addEventListener('change', onAdultChange);

  const nameInput = document.getElementById('catalog-name');
  if (nameInput) {
    nameInput.addEventListener('input', () => {
      if (nameInput.value.trim()) clearNameError();
    });
    nameInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        addCustom();
      }
    });
  }

  const searchInput = document.getElementById('header-search-input');
  if (searchInput) {
    searchInput.addEventListener('focus', () => {
      searchOpen = true;
      renderSearchDropdown();
    });
    searchInput.addEventListener('input', e => {
      scheduleSearchLookup(e.target.value);
    });
    searchInput.addEventListener('keydown', handleSearchKeydown);
  }

  const importInput = document.getElementById('import-url');
  if (importInput) {
    importInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        importConfig();
      }
    });
  }

  const catalogList = document.getElementById('catalog-list');
  if (catalogList) {
    catalogList.addEventListener('dragstart', e => {
      const item = e.target.closest('.catalog-item');
      if (!item) return;
      dragStart(e, parseInt(item.dataset.index, 10));
    });
    catalogList.addEventListener('dragover', e => {
      const item = e.target.closest('.catalog-item');
      if (!item) return;
      dragOver(e, parseInt(item.dataset.index, 10));
    });
    catalogList.addEventListener('dragleave', e => {
      const item = e.target.closest('.catalog-item');
      if (!item || item.contains(e.relatedTarget)) return;
      dragLeave({ currentTarget: item });
    });
    catalogList.addEventListener('drop', e => {
      const item = e.target.closest('.catalog-item');
      if (!item) return;
      drop(e, parseInt(item.dataset.index, 10));
    });
  }

  document.addEventListener('wheel', e => {
    const strip = e.target.closest?.('.smart-preview-strip');
    if (!strip) return;
    const maxScroll = strip.scrollWidth - strip.clientWidth;
    if (maxScroll <= 0) return;
    const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    if (!delta) return;
    const next = Math.max(0, Math.min(maxScroll, strip.scrollLeft + delta));
    if (next === strip.scrollLeft) return;
    e.preventDefault();
    strip.scrollLeft = next;
  }, { passive: false });

  window.addEventListener('resize', scheduleFitCatalogsSidePane);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && document.getElementById('search-modal-overlay')?.classList.contains('open')) {
      e.preventDefault();
      closeSearchCatalogModal();
      return;
    }
    if (e.key === 'Escape' && document.getElementById('recipe-modal-overlay')?.classList.contains('open')) {
      e.preventDefault();
      closeRecipeModal();
      return;
    }
    if (e.key === 'Escape' && document.getElementById('smart-modal-overlay')?.classList.contains('open')) {
      e.preventDefault();
      closeSmartBuilder();
      return;
    }
    const renameInput = e.target.closest('.catalog-rename-input');
    if (!renameInput) return;
    if (e.key === 'Enter') {
      e.preventDefault();
      renameInput.blur();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      cancelRename();
    }
  });

  document.addEventListener('focusout', e => {
    const renameInput = e.target.closest('.catalog-rename-input');
    if (!renameInput) return;
    commitRename(renameInput.dataset.renameId, renameInput.value);
  });

  document.addEventListener('click', e => {
    if (!e.target.closest?.('#header-search') && searchOpen) {
      closeSearchDropdown();
    }
    if (e.target?.id === 'ai-modal-overlay') {
      closeAiModal();
      return;
    }
    if (e.target?.id === 'search-modal-overlay') {
      closeSearchCatalogModal();
      return;
    }
    if (e.target?.id === 'recipe-modal-overlay') {
      closeRecipeModal();
      return;
    }
    if (e.target?.id === 'smart-modal-overlay') {
      closeSmartBuilder();
      return;
    }

    const genreBadge = e.target.closest('.genre-badge[data-genre]');
    if (genreBadge) {
      e.preventDefault();
      e.stopPropagation();
      applyGenreFilter(genreBadge.dataset.genre);
      return;
    }

    const actionEl = e.target.closest('[data-action]');
    if (!actionEl) return;

    switch (actionEl.dataset.action) {
      case 'save-config-before-login':
        saveConfigBeforeLogin();
        return;
      case 'disconnect':
        e.preventDefault();
        disconnect();
        return;
      case 'set-active-filter':
        e.preventDefault();
        setActiveFilter(actionEl.dataset.filter);
        return;
      case 'toggle-year-menu':
        e.preventDefault();
        toggleYearMenu();
        return;
      case 'set-year-value':
        e.preventDefault();
        setYearValue(actionEl.dataset.value);
        return;
      case 'add-custom':
        e.preventDefault();
        addCustom();
        return;
      case 'set-pane-tab':
        e.preventDefault();
        setPaneTab(actionEl.dataset.pane);
        return;
      case 'toggle-sort-menu':
        e.preventDefault();
        toggleSortMenu();
        return;
      case 'set-sort-value':
        e.preventDefault();
        setSortValue(actionEl.dataset.value);
        return;
      case 'set-view':
        e.preventDefault();
        setView(actionEl.dataset.view);
        return;
      case 'set-poster-style':
        e.preventDefault();
        setPosterStyle(actionEl.dataset.style);
        return;
      case 'set-search-mode':
        e.preventDefault();
        if (actionEl.dataset.mode === 'smart' && getResolvedSearchMode() !== 'smart') return;
        searchMode = actionEl.dataset.mode === 'smart' ? 'smart' : 'metadata';
        renderSearchUi();
        return;
      case 'search-result-preview':
        e.preventDefault();
        previewSearchResult(getSearchResultById(actionEl.dataset.resultId));
        return;
      case 'search-result-add':
        e.preventDefault();
        openSearchCatalogModal(getSearchResultById(actionEl.dataset.resultId));
        return;
      case 'add-preset':
        e.preventDefault();
        addPreset(actionEl.dataset.id, actionEl.dataset.name);
        return;
      case 'add-account-preset':
        e.preventDefault();
        addAccountPreset(actionEl.dataset.id, actionEl.dataset.name, actionEl.dataset.status);
        return;
      case 'open-ai-modal':
        e.preventDefault();
        e.stopPropagation();
        openAiModal();
        return;
      case 'open-smart-builder':
        e.preventDefault();
        openSmartBuilder();
        return;
      case 'close-smart-builder':
        e.preventDefault();
        closeSmartBuilder();
        return;
      case 'smart-template':
        e.preventDefault();
        setSmartTemplate(actionEl.dataset.mode);
        return;
      case 'smart-preview':
        e.preventDefault();
        previewSmartRow();
        return;
      case 'smart-save':
        e.preventDefault();
        saveSmartRow();
        return;
      case 'open-stremio':
        e.preventDefault();
        openInStremio();
        return;
      case 'copy-url':
        e.preventDefault();
        copyUrl();
        return;
      case 'open-search-add-modal-from-preview':
        e.preventDefault();
        if (activePrototypePreview) openSearchCatalogModal(activePrototypePreview);
        return;
      case 'dismiss-search-prototype-preview':
        e.preventDefault();
        dismissPrototypePreview();
        return;
      case 'close-search-modal':
        e.preventDefault();
        closeSearchCatalogModal();
        return;
      case 'search-modal-create-copy':
        e.preventDefault();
        applySearchDraftToCatalog(actionEl.dataset.targetId, 'copy');
        return;
      case 'search-modal-overwrite':
        e.preventDefault();
        applySearchDraftToCatalog(actionEl.dataset.targetId, 'overwrite');
        return;
      case 'open-share-recipe':
        e.preventDefault();
        openShareRecipeModal();
        return;
      case 'browse-recipes':
        e.preventDefault();
        openRecipeGallery();
        return;
      case 'close-recipe-modal':
        e.preventDefault();
        closeRecipeModal();
        return;
      case 'remove-recipe-catalog':
        e.preventDefault();
        removeCatalogFromRecipeDraft(actionEl.dataset.id);
        return;
      case 'add-recipe-catalog':
        e.preventDefault();
        addCatalogToRecipeDraft(actionEl.dataset.id);
        return;
      case 'copy-recipe-link':
        e.preventDefault();
        copyRecipeLink();
        return;
      case 'preview-builtin-recipe':
        e.preventDefault();
        openRecipePreview(getBuiltinRecipes()[parseInt(actionEl.dataset.index, 10)]);
        return;
      case 'add-builtin-recipe':
        e.preventDefault();
        applyRecipe(getBuiltinRecipes()[parseInt(actionEl.dataset.index, 10)], 'add');
        return;
      case 'apply-recipe':
        e.preventDefault();
        if (activeRecipePayload) applyRecipe(activeRecipePayload, actionEl.dataset.mode === 'replace' ? 'replace' : 'add');
        return;
      case 'import-config':
        e.preventDefault();
        importConfig();
        return;
      case 'remove-filter':
        e.preventDefault();
        e.stopPropagation();
        removeFilter(actionEl.dataset.key);
        return;
      case 'clear-all-filters':
        e.preventDefault();
        clearAllFilters();
        return;
      case 'preview-catalog':
        if (e.target.closest('.catalog-actions') || e.target.closest('.catalog-rename-input') || e.target.closest('.drag-handle')) return;
        previewCatalog(actionEl.dataset.id);
        return;
      case 'start-rename':
        e.preventDefault();
        e.stopPropagation();
        startRenaming(actionEl.dataset.id);
        return;
      case 'toggle-randomize':
        e.preventDefault();
        e.stopPropagation();
        toggleRandomize(actionEl.dataset.id);
        return;
      case 'remove-catalog':
        e.preventDefault();
        e.stopPropagation();
        removeCatalog(actionEl.dataset.id);
        return;
      case 'close-ai-modal':
        e.preventDefault();
        closeAiModal();
        return;
      case 'test-or-key':
        e.preventDefault();
        testOrKey();
        return;
      case 'save-ai-modal':
        e.preventDefault();
        saveOrKeyFromModal();
        return;
      default:
        return;
    }
  });

  document.addEventListener('change', e => {
    if (e.target?.id === 'ai-model-select') handleAiModelChange();
    if (e.target?.id === 'smart-seed-mode') setSmartTemplate(e.target.value);
    if (e.target?.id === 'recipe-preview-select') {
      recipePreviewCatalogId = e.target.value;
      refreshRecipePreview();
    }
    if (e.target?.matches?.('[data-smart-format], #smart-min-score, #smart-popularity')) {
      resetSmartBuilderPreview();
    }
  });

  document.addEventListener('input', e => {
    if (e.target?.id === 'recipe-name-input' || e.target?.id === 'recipe-desc-input') {
      syncShareRecipeDraftFromInputs();
    }
    if (e.target?.id === 'smart-row-name') {
      e.target.dataset.autoname = '0';
      if (smartBuilderPreviewCatalog) {
        const name = e.target.value.trim() || defaultSmartRowName(smartBuilderPreviewCatalog.aiMode, smartBuilderPreviewCatalog.seedTitle || '');
        smartBuilderPreviewCatalog.name = name;
        renderSmartInlinePreview(smartBuilderPreviewMedia, smartBuilderPreviewCatalog);
        updateSmartSaveState();
      }
    }
    if (e.target?.id === 'smart-seed-title') {
      const rowName = document.getElementById('smart-row-name');
      if (rowName && rowName.dataset.autoname === '1') rowName.value = defaultSmartRowName(smartBuilderMode, e.target.value.trim());
      resetSmartBuilderPreview();
    }
  });
}

if (!catalogs.length) {
  catalogs = [
    { id: 'anilist-popular-season', name: 'Popular This Season', type: 'preset' },
    { id: 'anilist-airing-week',    name: 'Airing This Week',    type: 'preset' },
    { id: 'anilist-trending',       name: 'Trending Now',        type: 'preset' },
    { id: 'anilist-top-rated',      name: 'Top Rated All Time',  type: 'preset' },
  ];
}

// Show auth error banner if redirected back with an OAuth error
const _authError = _urlParams.get('error');
if (_authError) {
  const banner = document.getElementById('error-banner');
  if (banner) {
    const errorMessages = {
      auth_failed: 'Failed to authenticate with AniList. Please try again.',
      auth_invalid_client: 'AniList rejected this app configuration. Check your AniList client ID, client secret, and redirect URI.',
    };
    banner.textContent = errorMessages[_authError] || errorMessages.auth_failed;
    banner.classList.add('visible');
  }
  _sessionKey = null;
  _hasOrKey = false;
  // Clean error param from URL without reloading
  const cleanUrl = new URL(window.location.href);
  cleanUrl.searchParams.delete('error');
  window.history.replaceState({}, '', cleanUrl.toString());
}

// Bootstrap auth UI — validates token against /api/me if present
bindStaticUiEvents();
syncPosterLabToggle();
fetchMe();

render();
setActiveFilter('genres');
renderFilterTags();
window.addEventListener('DOMContentLoaded', openInitialRecipeIfPresent);
</script>

<!-- Recipe Modal -->
<div class="recipe-modal-overlay" id="recipe-modal-overlay">
  <div class="recipe-modal">
    <div class="recipe-modal-header">
      <div class="recipe-modal-title" id="recipe-modal-title">Recipes</div>
      <button class="recipe-modal-close" data-action="close-recipe-modal">&#10005;</button>
    </div>
    <div class="recipe-modal-body" id="recipe-modal-body"></div>
    <div class="recipe-modal-footer" id="recipe-modal-footer"></div>
  </div>
</div>

<!-- Smart Row Builder Modal -->
<div class="smart-modal-overlay" id="smart-modal-overlay">
  <div class="smart-modal" role="dialog" aria-modal="true" aria-labelledby="smart-modal-title">
    <div class="smart-modal-header">
      <div class="smart-modal-title" id="smart-modal-title">Build Smart Row</div>
      <button class="smart-modal-close" data-action="close-smart-builder">&#10005;</button>
    </div>
    <div class="smart-modal-body" id="smart-modal-body"></div>
    <div class="smart-modal-footer" id="smart-modal-footer"></div>
  </div>
</div>

<!-- AI Settings Modal -->
<div class="ai-modal-overlay" id="ai-modal-overlay">
  <div class="ai-modal">
    <div class="ai-modal-header">
      <div class="ai-modal-title">OpenRouter Settings</div>
      <button class="ai-modal-close" data-action="close-ai-modal">&#10005;</button>
    </div>
    <div class="ai-modal-body">
      <div class="ai-modal-section">
        <label class="ai-modal-label">Model</label>
        <select id="ai-model-select" class="ai-modal-select">
          <option value="meta-llama/llama-3.3-70b-instruct">Llama 3.3 70B Instruct (Default &mdash; fast &amp; cheap)</option>
          <option value="google/gemini-flash-1.5">Gemini Flash 1.5 (Fast)</option>
          <option value="openai/gpt-4o-mini">GPT-4o Mini (Accurate)</option>
          <option value="anthropic/claude-haiku-4-5-20251001">Claude Haiku 4.5 (Fast)</option>
          <option value="custom">Custom model&hellip;</option>
        </select>
        <input type="text" id="ai-model-custom" class="ai-modal-input" placeholder="e.g. mistralai/mixtral-8x7b-instruct">
      </div>
      <div class="ai-modal-section">
        <label class="ai-modal-label">OpenRouter API Key</label>
        <div class="ai-key-row">
          <input type="password" id="ai-key-input" class="ai-modal-input" placeholder="sk-or-v1-…" autocomplete="off">
          <button class="ai-test-btn" id="ai-test-btn" data-action="test-or-key">Test</button>
        </div>
        <div class="ai-key-feedback" id="ai-key-feedback"></div>
        <div class="ai-key-hint">Get a free key at openrouter.ai/keys &mdash; key is encrypted and stored server-side only</div>
      </div>
    </div>
    <div class="ai-modal-footer">
      <button class="ai-modal-cancel" data-action="close-ai-modal">Cancel</button>
      <button class="ai-modal-save" id="ai-modal-save-btn" data-action="save-ai-modal">Save</button>
    </div>
  </div>
</div>
<div class="search-modal-overlay" id="search-modal-overlay">
  <div class="search-modal" role="dialog" aria-modal="true" aria-labelledby="search-modal-title">
    <div class="search-modal-header">
      <div>
        <div class="search-modal-title" id="search-modal-title">Add Search Draft</div>
        <div class="search-modal-sub" id="search-modal-sub"></div>
      </div>
      <button class="search-modal-close" data-action="close-search-modal">&#10005;</button>
    </div>
    <div class="search-modal-body" id="search-modal-body"></div>
    <div class="search-modal-footer" id="search-modal-footer">
      <button class="btn btn-ghost btn-sm" data-action="close-search-modal">Close</button>
    </div>
  </div>
</div>
</body>
</html>"""
