CONFIGURE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AniList Catalogs — Configure</title>
<style nonce="__CSP_NONCE__">
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
  body {
    font-family: 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', sans-serif;
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
    background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.025));
    border: 1px solid transparent;
    border-radius: 15px; color: var(--text2); cursor: pointer;
    padding: 0 16px; font-size: 12px; font-family: inherit;
    height: 38px; flex: 1; min-width: 0;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.045);
    transition: background 0.18s, border-color 0.18s, color 0.18s, transform 0.18s, box-shadow 0.18s;
  }
  .fb-filter-btn:hover {
    background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border-color: var(--sep-strong); color: var(--text); transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }
  .fb-filter-btn.active {
    border-color: rgba(255,255,255,0.24); color: var(--text);
    background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.035));
    box-shadow: none;
  }
  .fb-filter-btn.active .fb-chevron { transform: rotate(180deg); }
  .fb-filter-btn.has-value { color: var(--text); border-color: var(--sep-strong); }
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
    background: linear-gradient(180deg, #f8f8f8, #dcdcdc);
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
    height: 38px; padding: 0 18px; border-radius: 15px; font-size: 12px;
    font-family: inherit; font-weight: 700; cursor: pointer; flex-shrink: 0;
    background: linear-gradient(180deg, #fcfcfc, #dddddd);
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
    border-radius: 15px; color: var(--text2); cursor: pointer;
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
    border-radius: 15px; padding: 0 14px; height: 38px;
    flex: 1.5; min-width: 0;
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

  .fb-name-wrap { position: relative; flex: 1.5; min-width: 0; display: flex; }
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
    background: linear-gradient(180deg, rgba(255,255,255,0.14), rgba(255,255,255,0.05));
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
    padding: 5px 12px; border-radius: var(--pill);
    background: rgba(255,255,255,0.05); color: var(--text2);
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 12px; font-weight: 500; cursor: default;
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
    font-size: 11px; color: var(--text3); padding: 8px 12px;
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
    padding: 4px 6px 4px 12px;
    border-radius: var(--pill);
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
  }
  .view-sep { color: var(--sep); font-size: 14px; }
  .view-toggle {
    display: flex; gap: 3px;
    padding: 5px;
    border-radius: var(--pill);
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
  }
  .view-btn {
    background: none; border: none; cursor: pointer;
    color: var(--text3); padding: 8px; border-radius: 12px;
    display: flex; align-items: center;
    transition: background 0.15s, color 0.15s, transform 0.15s;
  }
  .view-btn:hover { background: rgba(255,255,255,0.07); color: var(--text2); transform: translateY(-1px); }
  .view-btn.active {
    background: linear-gradient(180deg, rgba(255,255,255,0.14), rgba(255,255,255,0.05));
    color: var(--text);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  }

  /* ── List view ───────────────────────────────── */
  .preview-list { display: flex; flex-direction: column; }
  .list-item {
    display: grid;
    grid-template-columns: 44px 1fr 90px 120px 140px;
    gap: 20px; align-items: center;
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    text-decoration: none; color: inherit;
    border-radius: 12px;
    transition: background 0.15s, transform 0.15s, border-color 0.15s;
    border: 1px solid transparent;
  }
  .list-item:last-child { border-bottom: none; }
  .list-item:hover { background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.07); transform: translateY(-1px); }
  .list-thumb {
    width: 44px; height: 62px; border-radius: 8px;
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
    display: flex; border-radius: 16px;
    overflow: hidden; background: linear-gradient(180deg, rgba(27,27,30,0.98), rgba(18,18,20,0.98));
    color: inherit; cursor: pointer;
    text-decoration: none;
    transition: background 0.18s, transform 0.18s, box-shadow 0.18s, border-color 0.18s;
    height: 270px;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: var(--shadow-sm);
    --studio-color: #ffffff;
    --studio-banner: rgba(255,255,255,0.18);
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
    background: var(--studio-banner);
    padding: 7px 14px;
    border-radius: 0;
    backdrop-filter: blur(3px) saturate(122%);
    -webkit-backdrop-filter: blur(3px) saturate(122%);
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
  .detail-card:hover .detail-overlay-title { color: var(--studio-color); }
  .detail-overlay-studio {
    font-size: 11px; font-weight: 600; margin-top: 4px;
    color: var(--studio-color);
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
    display: flex; align-items: center; gap: 6px; padding-top: 6px; flex-shrink: 0;
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
  #preview-area { padding: 0 0 4px; }
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
  .preview-list { padding: 0 28px; }
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
    --studio-banner: rgba(255,255,255,0.18);
  }
  .poster:hover { transform: translateY(-4px); }
  .poster-img {
    border-radius: 14px;
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
  .poster:hover .poster-img img { transform: scale(1.05); }
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
  .theme-orange { --studio-color:#e85d04; --studio-banner:rgba(232,93,4,0.18); --studio-banner-border:rgba(232,93,4,0.12); }
  .theme-gold { --studio-color:#f48c06; --studio-banner:rgba(244,140,6,0.18); --studio-banner-border:rgba(244,140,6,0.12); }
  .theme-lime { --studio-color:#a7c957; --studio-banner:rgba(167,201,87,0.18); --studio-banner-border:rgba(167,201,87,0.12); }
  .theme-blue { --studio-color:#4895ef; --studio-banner:rgba(72,149,239,0.18); --studio-banner-border:rgba(72,149,239,0.12); }
  .theme-pink { --studio-color:#f72585; --studio-banner:rgba(247,37,133,0.18); --studio-banner-border:rgba(247,37,133,0.12); }
  .theme-purple { --studio-color:#7b2fbe; --studio-banner:rgba(123,47,190,0.18); --studio-banner-border:rgba(123,47,190,0.12); }
  .theme-red { --studio-color:#e63946; --studio-banner:rgba(230,57,70,0.18); --studio-banner-border:rgba(230,57,70,0.12); }
  .theme-cyan { --studio-color:#48cae4; --studio-banner:rgba(72,202,228,0.18); --studio-banner-border:rgba(72,202,228,0.12); }
  .theme-green { --studio-color:#52b788; --studio-banner:rgba(82,183,136,0.18); --studio-banner-border:rgba(82,183,136,0.12); }
  .theme-violet { --studio-color:#9d4edd; --studio-banner:rgba(157,78,221,0.18); --studio-banner-border:rgba(157,78,221,0.12); }
  .theme-sky { --studio-color:#0077b6; --studio-banner:rgba(0,119,182,0.18); --studio-banner-border:rgba(0,119,182,0.12); }
  .theme-amber { --studio-color:#f4c430; --studio-banner:rgba(244,196,48,0.18); --studio-banner-border:rgba(244,196,48,0.12); }
  .theme-coral { --studio-color:#ff7a59; --studio-banner:rgba(255,122,89,0.18); --studio-banner-border:rgba(255,122,89,0.12); }
  .theme-mint { --studio-color:#26c485; --studio-banner:rgba(38,196,133,0.18); --studio-banner-border:rgba(38,196,133,0.12); }
  .theme-rose { --studio-color:#ff5d8f; --studio-banner:rgba(255,93,143,0.18); --studio-banner-border:rgba(255,93,143,0.12); }
  .theme-ocean { --studio-color:#118ab2; --studio-banner:rgba(17,138,178,0.18); --studio-banner-border:rgba(17,138,178,0.12); }
  .theme-indigo { --studio-color:#3a86ff; --studio-banner:rgba(58,134,255,0.18); --studio-banner-border:rgba(58,134,255,0.12); }
  .theme-magenta { --studio-color:#ff006e; --studio-banner:rgba(255,0,110,0.18); --studio-banner-border:rgba(255,0,110,0.12); }
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
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.14);
  }
  .poster-meta {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 10px 14px;
    background: var(--studio-banner);
    backdrop-filter: blur(3px) saturate(122%);
    -webkit-backdrop-filter: blur(3px) saturate(122%);
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
  .poster:hover .poster-title { color: var(--studio-color); }
  .preset-name.ai-title {
    display: inline-flex;
    align-items: center;
    gap: 7px;
  }
  .ai-star-icon {
    width: 14px;
    height: 14px;
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
  .score-high { color: #2d6a4f; }
  .score-mid { color: #52b788; }
  .score-low { color: #f48c06; }
  .score-poor { color: #e63946; }
  .score-none { color: var(--text3); }
  .detail-score-badge.detail-score-high { background: #2d6a4f; }
  .detail-score-badge.detail-score-mid { background: #52b788; }
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
  .ai-connected-hidden { display: none; }
  .select-hidden { display: none; }
  .catalogs-hidden { display: none !important; }
  .catalog-meta-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 20px;
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
    background: linear-gradient(180deg, rgba(29,29,32,0.98), rgba(20,20,22,0.98));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
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
    background: linear-gradient(135deg, rgba(255,255,255,0.06), transparent 42%);
    opacity: 0;
    transition: opacity 0.18s ease;
    pointer-events: none;
  }
  .preset-card:hover  {
    background: linear-gradient(180deg, rgba(36,37,41,0.98), rgba(24,24,27,0.98));
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    border-color: rgba(255,255,255,0.11);
  }
  .preset-card:hover::before { opacity: 1; }
  .preset-card:active { background: rgba(255,255,255,0.06); }
  .preset-info { flex: 1; min-width: 0; }
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
  .preset-card.added .preset-badge { display: block; }
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
    overflow-y: hidden; background: linear-gradient(180deg, rgba(14,14,16,0.96), rgba(8,8,9,0.98));
  }
  .catalogs-side-col .divider { margin: 6px 0; }
  .side-module {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 10px;
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
  .import-row input { flex: 1; font-size: 12px; padding: 8px 11px; border-radius: 12px; }
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

  /* ── Buttons ─────────────────────────────────── */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 10px 16px;
    border-radius: 14px;
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
  .btn-primary { background: linear-gradient(180deg, #ffffff, #dfdfdf); color: #000000; box-shadow: none; }
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
  .mid-panel::-webkit-scrollbar { width: 3px; }
  .left-panel::-webkit-scrollbar-track,
  .mid-panel::-webkit-scrollbar-track { background: transparent; }
  .left-panel::-webkit-scrollbar-thumb,
  .mid-panel::-webkit-scrollbar-thumb {
    background: rgba(84,84,88,0.28);
    border-radius: 2px;
  }
  .left-panel::-webkit-scrollbar-thumb:hover,
  .mid-panel::-webkit-scrollbar-thumb:hover { background: rgba(84,84,88,0.50); }
  .catalog-item {
    background: linear-gradient(180deg, rgba(28,28,31,0.98), rgba(18,18,20,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
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
  .catalog-item:hover { background: linear-gradient(180deg, rgba(35,36,40,0.98), rgba(22,22,25,0.98)); border-color: rgba(255,255,255,0.12); box-shadow: var(--shadow-md); }
  .catalog-item.active-preview {
    background: linear-gradient(180deg, rgba(37,38,42,0.98), rgba(23,24,27,0.98));
    border-color: rgba(255,255,255,0.14);
    box-shadow: inset 3px 0 0 rgba(255,255,255,0.22), var(--shadow-md);
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
  .shuffle-btn.active { background: rgba(255,255,255,0.12); color: var(--text); }
  .remove-btn:hover { background: rgba(220,38,38,0.24); color: #fecaca; transform: translateY(-1px); }
  .catalog-num {
    flex-shrink: 0; width: 34px; height: 34px;
    border-radius: 12px; background: rgba(255,255,255,0.1);
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
    background: linear-gradient(180deg, rgba(26,26,29,0.96), rgba(17,17,19,0.96));
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
  }
  .empty-icon { font-size: 28px; opacity: 0.35; }

  /* ── URL output ──────────────────────────────── */
  .btn-stremio {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; padding: 9px 12px; border-radius: 16px; border: 1px solid transparent;
    background: linear-gradient(180deg, #ffffff, #dfdfdf); color: #0a0a0a;
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
    background: linear-gradient(180deg, rgba(26,26,29,0.98), rgba(18,18,20,0.98));
    border-radius: 14px;
    padding: 11px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shadow-sm);
  }
  .url-box-row { display: flex; align-items: flex-start; gap: 8px; }
  .url-text {
    font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
    font-size: 10px; color: var(--text2);
    word-break: break-all; line-height: 1.65;
    max-height: 68px; overflow-y: auto;
    margin-bottom: 8px; cursor: text; user-select: all;
    scrollbar-width: thin; scrollbar-color: var(--sep) transparent;
    padding: 8px 10px;
    border-radius: 14px;
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
    background: linear-gradient(180deg, rgba(26,26,29,0.98), rgba(18,18,20,0.98)); border-radius: 14px; padding: 10px;
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--shadow-sm);
  }
  #qr-canvas-wrap canvas,
  #qr-canvas-wrap img { border-radius: 12px; display: block; max-width: 100%; height: auto; }
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
    transform: translateX(8px) translateY(-3px) scale(1.01);
    background: var(--card2) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.45);
    z-index: 1;
    border-radius: var(--radius) !important;
  }
  .catalog-item.shift-down { transform: translateY(10px); }
  .catalog-item.shift-up { transform: translateY(-10px); }

  /* ── Auth header section ─────────────────────────── */
  .header-auth { margin-left: auto; display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
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

  /* ── AI Recommendations pill ─────────────────────── */
  .preset-card.ai-no-key { border: 0.5px solid rgba(220,38,38,0.45) !important; }
  .preset-card.ai-no-key:hover { border-color: rgba(220,38,38,0.7) !important; }
  .ai-gear-btn {
    display: none; align-items: center; justify-content: center;
    width: 26px; height: 26px; border-radius: 50%; flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.05); color: var(--text3);
    cursor: pointer; font-size: 12px; line-height: 1;
    transition: background 0.15s, color 0.15s;
  }
  .preset-card:not(.account-locked):hover .ai-gear-btn { display: flex; }
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
  .ai-modal-save:hover { opacity: 0.85; }
  .ai-modal-save:disabled { opacity: 0.4; cursor: not-allowed; }

  @media (max-width: 1024px) {
    main { grid-template-columns: 326px 1fr; }
    .catalogs-side-col { flex-basis: 316px; }
    .preview-grid { grid-template-columns: repeat(auto-fill, minmax(188px, 1fr)); }
    .poster { width: 188px; }
    .detail-grid { grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); }
  }
  @media (max-width: 768px) {
    main { grid-template-columns: 1fr; }
    .mid-panel { border-top: 1px solid var(--sep); }
    header { padding: 14px 20px; }
    .header-sub { display: none; }
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
    }
    .detail-grid { grid-template-columns: 1fr; }
    .detail-card { height: auto; min-height: 270px; }
    .preview-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px; }
    .poster { width: 100%; }
    .list-item { grid-template-columns: 44px 1fr; gap: 14px; }
    .list-score, .list-meta-col { display: none; }
    .pane-tab-extras { justify-content: flex-start; }
    .view-controls { width: 100%; justify-content: space-between; }
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
          <div class="preset-card account-locked" id="preset-anilist-ai-recommendations" data-action="add-ai">
            <div class="preset-info">
              <div class="preset-name ai-title"><svg class="ai-star-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.2 3.2c.52 2.92 1.5 4.03 2.6 4.83.82.6 1.74.95 4.9 1.6-2.93.52-4.05 1.5-4.85 2.6-.6.82-.95 1.74-1.6 4.9-.52-2.93-1.5-4.05-2.6-4.85-.82-.6-1.74-.95-4.9-1.6 2.93-.52 4.05-1.5 4.85-2.6.6-.82.95-1.74 1.6-4.9Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M18.2 3.4c.24 1.35.7 1.86 1.2 2.23.38.27.8.44 2.26.74-1.35.24-1.87.7-2.24 1.2-.27.38-.44.8-.74 2.26-.24-1.35-.7-1.87-1.2-2.24-.38-.27-.8-.44-2.26-.74 1.35-.24 1.87-.7 2.24-1.2.27-.38.44-.8.74-2.26Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M17.2 14.2c.3 1.68.87 2.33 1.5 2.78.46.34.97.54 2.82.92-1.68.3-2.34.87-2.79 1.5-.34.46-.54.97-.92 2.82-.3-1.68-.87-2.34-1.5-2.79-.46-.34-.97-.54-2.82-.92 1.68-.3 2.34-.87 2.79-1.5.34-.46.54-.97.92-2.82Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>AI Recommendations</div>
              <div class="preset-desc">Personalised picks powered by AI</div>
            </div>
            <span class="account-badge ai-badge">AI</span>
            <div class="preset-badge">Added</div>
            <button class="ai-gear-btn" id="ai-gear-btn" data-action="open-ai-modal" title="Configure AI settings">&#9881;</button>
            <span class="ai-connected-tag ai-connected-hidden" id="ai-connected-tag">Connected</span>
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
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-planning" data-action="add-account-preset" data-id="anilist-watching-planning" data-name="Plan to Watch" data-status="PLANNING">
            <div class="preset-info"><div class="preset-name">Plan to Watch</div><div class="preset-desc">Your watch list</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-completed" data-action="add-account-preset" data-id="anilist-watching-completed" data-name="Completed" data-status="COMPLETED">
            <div class="preset-info"><div class="preset-name">Completed</div><div class="preset-desc">Anime you've finished</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-paused" data-action="add-account-preset" data-id="anilist-watching-paused" data-name="Paused" data-status="PAUSED">
            <div class="preset-info"><div class="preset-name">Paused</div><div class="preset-desc">On hold</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-dropped" data-action="add-account-preset" data-id="anilist-watching-dropped" data-name="Dropped" data-status="DROPPED">
            <div class="preset-info"><div class="preset-name">Dropped</div><div class="preset-desc">Anime you've stopped watching</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-repeating" data-action="add-account-preset" data-id="anilist-watching-repeating" data-name="Rewatching" data-status="REPEATING">
            <div class="preset-info"><div class="preset-name">Rewatching</div><div class="preset-desc">Currently rewatching</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-favourites" data-action="add-account-preset" data-id="anilist-favourites" data-name="My Favourites" data-status="FAVOURITES">
            <div class="preset-info"><div class="preset-name">My Favourites</div><div class="preset-desc">Your starred anime</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
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
        <div class="pane-footer-text">Version: v1.3.0 &mdash; Developed by juuzo</div>
      </div>
    </div>

    <!-- MID: Filters + Preview + Catalogs -->
    <div class="mid-panel">

      <!-- Filter bar -->
      <div class="filter-bar">
        <button class="fb-filter-btn" id="btn-genres" data-action="set-active-filter" data-filter="genres">
          <span id="lbl-genres">Genres</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-year" class="select-hidden">
          <option value="">Year</option>
          __YEAR_OPTIONS__
        </select>
        <button class="fb-filter-btn" id="btn-year" data-action="set-active-filter" data-filter="year">
          <span id="lbl-year">Year</span>
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
          </div>
          <div class="side-or">OR</div>
          <div class="side-module">
            <div class="url-box">
              <div class="url-text" id="url-display">—</div>
              <div class="copy-row">
                <button class="btn btn-ghost btn-sm btn-full" id="copy-url-btn" data-action="copy-url">Copy URL</button>
                <div class="url-warn-icon" id="token-warning">
                  &#9888;
                  <div class="url-warn-tooltip">This URL contains a session key for your AniList account. Keep it private and do not share it. If it expires, just reconnect AniList.</div>
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
                <input type="text" id="import-url" placeholder="Paste manifest URL…">
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

// ── Auth state ────────────────────────────────────
const _urlParams = new URLSearchParams(window.location.search);
const _hashParams = new URLSearchParams(window.location.hash.startsWith('#') ? window.location.hash.slice(1) : '');
// Session key: a short 12-char token handed back by the OAuth callback.
// The actual encrypted AniList token lives server-side; only this key travels
// in the manifest URL (as "{config_token}~{session_key}").
let _sessionKey = _hashParams.get('s') || _urlParams.get('s') || null;
// OpenRouter state — populated from /api/me response on load.
let _hasOrKey = false;
let _orModel  = 'meta-llama/llama-3.3-70b-instruct';
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
// restored on return (identified by the presence of the ?s= session key).
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
  // AI pill: locked when not authenticated, red outline when authenticated but no OR key
  const aiCard = document.getElementById('preset-anilist-ai-recommendations');
  if (aiCard) {
    aiCard.classList.toggle('account-locked', locked);
    aiCard.classList.toggle('pointer-disabled', locked);
    aiCard.classList.toggle('ai-no-key', !locked && !_hasOrKey);
    const connTag = document.getElementById('ai-connected-tag');
    setHidden(connTag, locked || !_hasOrKey);
  }
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

// Returns true if any additional filter (genre/format/status/year/season/score)
// is active on top of the current source tag.
function hasActiveAdditionalFilters() {
  const score = parseInt(document.getElementById('f-score').value);
  return selectedGenres.length > 0 || selectedFormats.length > 0 ||
         selectedStatuses.length > 0 || selectedYears.length > 0 ||
         selectedSeasons.length > 0 || score > 0;
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
  const parts = [activeSource.name];
  selectedGenres.forEach(g  => parts.push(g));
  selectedFormats.forEach(f  => parts.push(FORMAT_LABELS[f] || f));
  selectedYears.forEach(y    => parts.push(y));
  selectedSeasons.forEach(s  => parts.push(s === 'CURRENT' ? 'Current Season' : (SEASON_LABELS[s] || s)));
  selectedStatuses.forEach(s => parts.push(STATUS_LABELS[s] || s));
  const score = parseInt(document.getElementById('f-score').value);
  if (score > 0) parts.push(score + '+ Score');
  return parts.join(' \u00b7 ');
}

// Build a clientFilters object from the current DOM filter state.
function _buildClientFilters() {
  const f = {};
  const sort  = document.getElementById('f-sort').value;
  const score = parseInt(document.getElementById('f-score').value);
  if (sort && sort !== 'POPULARITY_DESC') f.sort = sort;
  if (selectedGenres.length)   f.genres   = [...selectedGenres];
  if (selectedFormats.length)  f.formats  = [...selectedFormats];
  if (selectedStatuses.length) f.statuses = [...selectedStatuses];
  if (selectedYears.length)    f.years    = [...selectedYears];
  if (selectedSeasons.length)  f.seasons  = [...selectedSeasons];
  if (score > 0)               f.minScore = score;
  return f;
}

// Update the name-input + Add-button visibility based on source/filter state.
// Shows when: no source (standard custom flow), OR source + additional filters.
// Hides when: source only, no additional filters (catalog added directly).
function updateNameInput() {
  const wrap   = document.getElementById('catalog-name-wrap');
  const addBtn = document.getElementById('catalog-add-btn');
  if (!wrap || !addBtn) return;

  const hasFilters = hasActiveAdditionalFilters();
  const hideForSource = activeSource && !hasFilters;
  wrap.classList.toggle('hidden', hideForSource);
  addBtn.classList.toggle('hidden', hideForSource);

  if (activeSource && hasFilters) {
    const inp       = document.getElementById('catalog-name');
    const suggested = _buildSuggestedName();
    if (!inp.value.trim() || inp.value === _lastSuggestedName) {
      inp.value = suggested;
      _lastSuggestedName = suggested;
    }
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
  const subtitle = count < total
    ? `${activeSource.name} \u2014 ${count} of ${total} titles`
    : `${activeSource.name} \u2014 ${count} titles`;
  renderPreview(filtered, subtitle);
}

async function previewPresetWithCurrentFilters(cat) {
  setPreviewLoading(cat.name);
  try {
    if (cat.id === 'anilist-airing-week') {
      const media = await fetchAiringWeekPreview();
      const filtered = _filterSourceMedia(media);
      const subtitle = filtered.length < media.length
        ? `${cat.name} \u2014 ${filtered.length} of ${media.length} titles`
        : `${cat.name} \u2014 ${filtered.length} titles`;
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

    const media = await fetchPreview(variables);
    renderPreview(media, `${cat.name} \u2014 ${media.length} titles`);
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
      document.getElementById('preview-sub').textContent = activeSource.name;
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#128274;</div><div>Account catalog<br><span class="preview-error-detail">Connect your AniList account to preview this list</span></div></div>';
      return;
    }
    setPreviewLoading(activeSource.name);
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
      document.getElementById('preview-sub').textContent = activeSource.name;
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#128274;</div><div>Account catalog<br><span class="preview-error-detail">Connect your AniList account to use AI recommendations</span></div></div>';
      return;
    }
    if (!_hasOrKey) {
      document.getElementById('preview-sub').textContent = activeSource.name;
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#9881;</div><div>OpenRouter key required<br><span class="preview-error-detail">Click the gear icon on the AI pill to add your key</span></div></div>';
      return;
    }
    setPreviewLoading('AI is thinking\u2026 (this may take a moment)');
    try {
      const res = await fetch('/api/preview-ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session: _sessionKey }),
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
  if (!_sessionKey) return;
  const alreadyAdded = !!catalogs.find(c => c.id === id);
  // Set this as the active source (shows tag in filter bar + enables filtering on top)
  activeSource = { id, name, listStatus, type: 'watching' };
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

function addAiCatalog() {
  if (!_sessionKey) return;
  if (!_hasOrKey) { openAiModal(); return; }
  const alreadyAdded = !!catalogs.find(c => c.id === 'anilist-ai-recommendations');
  activeSource = { id: 'anilist-ai-recommendations', name: 'AI Recommendations', type: 'ai' };
  _sourceMedia = null;
  _lastSuggestedName = '';
  _clearAdditionalFilters();
  if (!alreadyAdded) {
    catalogs.push({ id: 'anilist-ai-recommendations', name: 'AI Recommendations', type: 'ai', model: _orModel });
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
  if (!_sessionKey) return;
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
  if (btn) { btn.disabled = true; btn.textContent = 'Testing\u2026'; }
  if (fb) { fb.textContent = ''; fb.className = 'ai-key-feedback'; }
  try {
    const res = await fetch('/api/test-openrouter-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: keyInput.value.trim() }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data.valid) {
      if (fb) { fb.textContent = '\u2713 Key is valid.'; fb.className = 'ai-key-feedback ok'; }
    } else {
      if (fb) { fb.textContent = '\u2717 ' + (data.detail || 'Invalid key.'); fb.className = 'ai-key-feedback err'; }
    }
  } catch(e) {
    if (fb) { fb.textContent = '\u2717 Network error.'; fb.className = 'ai-key-feedback err'; }
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
  if (saveBtn) { saveBtn.disabled = true; saveBtn.textContent = 'Saving\u2026'; }
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
      render();
      closeAiModal();
      // If model changed and AI catalog is already added, trigger a fresh fetch
      if (modelChanged && catalogs.find(c => c.id === 'anilist-ai-recommendations')) {
        _sourceMedia = null;
        activeSource = { id: 'anilist-ai-recommendations', name: 'AI Recommendations', type: 'ai' };
        renderFilterTags();
        updateNameInput();
        setPaneTab('preview');
        fetchAndShowSource();
      }
    } else {
      if (fb) { fb.textContent = '\u2717 ' + (data.detail || 'Failed to save.'); fb.className = 'ai-key-feedback err'; }
    }
  } catch(e) {
    if (fb) { fb.textContent = '\u2717 Network error.'; fb.className = 'ai-key-feedback err'; }
  } finally {
    if (saveBtn) { saveBtn.disabled = false; saveBtn.textContent = 'Save'; }
  }
}

// ── Filter bar helpers ────────────────────────────

// ── Inline filter panel helpers ────────────────────
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

function setActiveFilter(id) {
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

  const multiIds = ['year', 'season', 'format', 'status'];
  const arr = id === 'year'     ? selectedYears
            : id === 'season'   ? selectedSeasons
            : id === 'format'   ? selectedFormats
            : id === 'status'   ? selectedStatuses
            : null;

  const opts = id === 'year'
    ? [...document.getElementById('f-year').options].map(o => ({ value: o.value, label: o.value ? o.text : 'Any' }))
    : FILTER_OPTS[id];

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
  query($sort:[MediaSort],$format_in:[MediaFormat],$season:MediaSeason,$seasonYear:Int,$status_in:[MediaStatus],$genre_in:[String],$averageScore_greater:Int,$startDate_greater:FuzzyDateInt,$startDate_lesser:FuzzyDateInt,$isAdult:Boolean){
    Page(page:1,perPage:50){
      media(type:ANIME,isAdult:$isAdult,sort:$sort,format_in:$format_in,season:$season,seasonYear:$seasonYear,status_in:$status_in,genre_in:$genre_in,averageScore_greater:$averageScore_greater,startDate_greater:$startDate_greater,startDate_lesser:$startDate_lesser){
        id title{romaji english} coverImage{large} averageScore popularity
        genres format episodes status season seasonYear description(asHtml:false)
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
          id title{romaji english} coverImage{large} averageScore isAdult popularity
          genres format episodes status season seasonYear description(asHtml:false)
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

function setPreviewLoading(subtitle) {
  document.getElementById('preview-sub').textContent = subtitle || 'Loading\u2026';
  document.getElementById('preview-area').innerHTML = '<div class="preview-loading"><div class="spinner"></div></div>';
}

function renderPreview(media, subtitle) {
  _lastMedia = media; _lastSubtitle = subtitle;
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
        <img src="${escHtml(m.coverImage.large)}" alt="${title}" loading="lazy">
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
    const score   = m.averageScore ? m.averageScore + '%' : '\u2014';
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
      <div class="list-thumb"><img src="${escHtml(m.coverImage.large)}" alt="${title}" loading="lazy"></div>
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
    const meta    = [fmt, eps].filter(Boolean).join(' \u00b7 ');
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
        <img src="${escHtml(m.coverImage.large)}" alt="${title}" loading="lazy">
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
});

// ── Pane tab switch (Preview / Catalogs) ──────────
let currentPane = 'preview';
function setPaneTab(tab) {
  currentPane = tab;
  document.getElementById('tab-preview').classList.toggle('active', tab === 'preview');
  document.getElementById('tab-catalogs').classList.toggle('active', tab === 'catalogs');
  document.getElementById('preview-pane').classList.toggle('pane-hidden', tab !== 'preview');
  document.getElementById('catalogs-pane').classList.toggle('catalogs-hidden', tab !== 'catalogs');
  document.getElementById('preview-tab-extras').classList.toggle('pane-hidden', tab !== 'preview');
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
  renderSortBtn();
  syncFilterBtnLabels();

  const tags = [];
  // Source tag always appears first when an account/AI source is active
  if (activeSource) tags.push({ key: 'source', label: activeSource.name.toLowerCase() });
  selectedFormats.forEach(f  => tags.push({ key: 'format:'  + f, label: FORMAT_LABELS[f]  || f }));
  selectedSeasons.forEach(s  => tags.push({ key: 'season:'  + s, label: s === 'CURRENT' ? 'Current Season' : (SEASON_LABELS[s] || s) }));
  selectedYears.forEach(y    => tags.push({ key: 'year:'    + y, label: y }));
  selectedStatuses.forEach(s => tags.push({ key: 'status:'  + s, label: STATUS_LABELS[s] || s }));
  if (score > 0) tags.push({ key: 'score', label: score + '+ score' });
  if (includeAdult) tags.push({ key: 'adult', label: 'Adult' });
  selectedGenres.forEach(g   => tags.push({ key: 'genre:'   + g, label: g }));

  const container = document.getElementById('filter-tags');
  container.innerHTML = tags.map(t =>
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
  if      (key === 'score')            { document.getElementById('f-score').value = 0; document.getElementById('score-val').textContent = 'Any'; }
  else if (key === 'adult')            { includeAdult = false; document.getElementById('f-adult').checked = false; document.getElementById('adult-toggle').classList.remove('active'); }
  else if (key.startsWith('genre:'))   { toggleMultiVal(selectedGenres,  key.slice(6)); }
  else if (key.startsWith('format:'))  { toggleMultiVal(selectedFormats, key.slice(7)); }
  else if (key.startsWith('status:'))  { toggleMultiVal(selectedStatuses,key.slice(7)); }
  else if (key.startsWith('year:'))    { toggleMultiVal(selectedYears,   key.slice(5)); }
  else if (key.startsWith('season:'))  { toggleMultiVal(selectedSeasons, key.slice(7)); }
  document.getElementById('f-daterange').value = '';
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
  if (filters.sort)                                 v.sort             = [filters.sort];
  if (filters.formats  && filters.formats.length)   v.format_in        = filters.formats;
  else if (filters.format)                          v.format_in        = [filters.format];
  if (filters.statuses && filters.statuses.length)  v.status_in        = filters.statuses;
  else if (filters.status)                          v.status_in        = [filters.status];
  if (filters.season)                               v.season           = filters.season;
  if (filters.year)                                 v.seasonYear       = filters.year;
  if (filters.minScore)                             v.averageScore_greater = filters.minScore;
  if (filters.genres && filters.genres.length)      v.genre_in         = filters.genres;
  return v;
}

// ── Preset form defaults ──────────────────────────
const PRESET_FORM_DEFAULTS = {
  'anilist-popular-season': { sort: 'POPULARITY_DESC', formats: [], seasons: ['CURRENT'], statuses: ['RELEASING'], score: 0, genres: [] },
  'anilist-airing-week':    { sort: 'TRENDING_DESC',   formats: [], seasons: [],          daterange: 'this-week', statuses: ['RELEASING'], score: 0, genres: [] },
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
  selectedYears   = f.year     ? [String(f.year)] : [];
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

// Quick Date Range presets — auto-fill the existing filter fields.
// No special query logic; "This Week" = status:RELEASING, month-based = season+year.
// The "Airing This Week" PRESET (not this filter) uses the airingSchedules query.
function onDateRangeChange(el) {
  const now = new Date();
  const y = now.getFullYear();
  const m = now.getMonth() + 1;
  switch (el.value) {
    case 'this-week':
      selectedStatuses = ['RELEASING'];
      selectedYears = []; selectedSeasons = [];
      break;
    case 'this-month':
      selectedYears   = [String(y)];
      selectedSeasons = [m <= 3 ? 'WINTER' : m <= 6 ? 'SPRING' : m <= 9 ? 'SUMMER' : 'FALL'];
      break;
    case 'last-month': {
      const lm = m === 1 ? 12 : m - 1;
      const ly = m === 1 ? y - 1 : y;
      selectedYears   = [String(ly)];
      selectedSeasons = [lm <= 3 ? 'WINTER' : lm <= 6 ? 'SPRING' : lm <= 9 ? 'SUMMER' : 'FALL'];
      break;
    }
    case 'this-year':
      selectedYears   = [String(y)];
      selectedSeasons = [];
      break;
    case 'last-year':
      selectedYears   = [String(y - 1)];
      selectedSeasons = [];
      break;
    default:
      break;
  }
  syncFilterBtnLabels();
  if (activeFbFilter) renderFilterOpts(activeFbFilter);
  scheduleAutoPreview();
}

// ── Preset add / preview ──────────────────────────
async function addPreset(id, name) {
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
async function previewCustom() {
  const sort  = document.getElementById('f-sort').value;
  const score = parseInt(document.getElementById('f-score').value);
  const year   = selectedYears.length  === 1 ? selectedYears[0]  : '';
  const season = selectedSeasons.length === 1 ? selectedSeasons[0] : '';

  const sv = resolveSeasonVars(season, year);
  const variables = { sort: [sort] };
  if (!includeAdult) variables.isAdult = false;
  if (selectedFormats.length)  variables.format_in  = [...selectedFormats];
  if (selectedStatuses.length) variables.status_in  = [...selectedStatuses];
  if (sv.season)               variables.season     = sv.season;
  if (sv.seasonYear)           variables.seasonYear = sv.seasonYear;
  if (score > 0)               variables.averageScore_greater = score;
  if (selectedGenres.length)   variables.genre_in   = [...selectedGenres];

  setPreviewLoading('Loading\u2026');
  try {
    const media = await fetchPreview(variables);
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

  if (activeSource && hasActiveAdditionalFilters()) {
    // Save a filtered watching/AI catalog — the source type and listStatus are stored,
    // plus client-side filters so the configure UI preview re-applies them.
    const clientFilters = _buildClientFilters();
    const id = 'watch-' + Math.random().toString(36).slice(2, 10);
    const cat = { id, name, type: 'watching' };
    if (activeSource.listStatus) cat.listStatus = activeSource.listStatus;
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
  const filters = {};
  const sort  = document.getElementById('f-sort').value;
  const score = parseInt(document.getElementById('f-score').value);
  const year   = selectedYears.length  === 1 ? selectedYears[0]  : '';
  const season = selectedSeasons.length === 1 ? selectedSeasons[0] : '';

  const sv = resolveSeasonVars(season, year);
  if (sort)                    filters.sort     = sort;
  if (selectedFormats.length)  filters.formats  = [...selectedFormats];
  if (selectedStatuses.length) filters.statuses = [...selectedStatuses];
  if (sv.season)               filters.season   = sv.season;
  if (sv.seasonYear)           filters.year     = sv.seasonYear;
  if (score > 0)               filters.minScore = score;
  if (selectedGenres.length)   filters.genres   = [...selectedGenres];

  const id = 'custom-' + Math.random().toString(36).slice(2, 10);
  catalogs.push({ id, name, type: 'custom', filters });

  document.getElementById('catalog-name').value = '';
  clearNameError();
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
  render();
}

// ── Preview catalog row ───────────────────────────
let previewingId = null;
async function previewCatalog(id) {
  if (dragMoved) return;
  const cat = catalogs.find(c => c.id === id);
  if (!cat) return;
  previewingId = id;

  if (cat.type === 'watching' || cat.type === 'ai') {
    // Set as active source so the tag bar shows the source tag and filters work on top
    activeSource = {
      id:          cat.id,
      name:        cat.name,
      listStatus:  cat.listStatus,
      type:        cat.type,
    };
    _sourceMedia = null;
    _lastSuggestedName = '';
    _clearAdditionalFilters();
    renderFilterTags();
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
    renderPreview(media, `${cat.name} \u2014 ${media.length} titles`);
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
  document.getElementById('preview-sub').textContent = 'Updating\u2026';
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
  const aiCard = document.getElementById('preset-anilist-ai-recommendations');
  if (aiCard) aiCard.classList.toggle('added', catalogs.some(c => c.id === 'anilist-ai-recommendations'));

  const list = document.getElementById('catalog-list');
  const countBadge = document.getElementById('catalog-count-badge');
  if (countBadge) {
    countBadge.textContent = catalogs.length + ' Catalog' + (catalogs.length !== 1 ? 's' : '');
    countBadge.classList.toggle('hidden', catalogs.length === 0);
  }
  if (catalogs.length === 0) {
    list.innerHTML = '<div class="empty-state"><div class="empty-icon">&#127916;</div><div>No catalogs yet.<br>Use Quick Add or the builder.</div></div>';
  } else {
    list.innerHTML = catalogs.map((c, i) => `
      <div class="catalog-item ${previewingId === c.id ? 'active-preview' : ''}" draggable="true" data-id="${c.id}" data-index="${i}" data-action="preview-catalog">
        <span class="drag-handle">&#8597;</span>
        <div class="catalog-num">${i + 1}</div>
        <div class="catalog-item-info">
          ${renamingId === c.id
            ? `<input class="catalog-rename-input" data-rename-id="${c.id}" value="${escHtml(c.name)}">`
            : `<div class="catalog-item-name">${escHtml(c.name)}</div>`
          }
          <div class="catalog-item-type"><span class="catalog-type-badge">${c.type === 'watching' ? 'Account' : c.type === 'ai' ? 'AI' : c.type === 'custom' ? 'Custom' : 'Preset'}</span></div>
        </div>
        <div class="catalog-actions">
          <button class="edit-btn" type="button" data-action="start-rename" data-id="${c.id}">&#9998; Rename</button>
          <button class="shuffle-btn ${c.randomize ? 'active' : ''}" type="button" data-action="toggle-randomize" data-id="${c.id}">${SHUFFLE_ICON} Randomize</button>
          <button class="remove-btn" type="button" data-action="remove-catalog" data-id="${c.id}">&#128465; Remove</button>
        </div>
      </div>
    `).join('');
  }

  updateUrl();
}

function filterSummary(f) {
  if (!f) return 'Custom catalog';
  const parts = [];
  if (f.genres && f.genres.length) parts.push(f.genres.slice(0,2).join(', '));
  if (f.season) parts.push(f.season.charAt(0) + f.season.slice(1).toLowerCase());
  if (f.year)   parts.push(f.year);
  if (f.format) parts.push(f.format);
  if (f.minScore) parts.push('Score ' + f.minScore + '+');
  return parts.length ? parts.join(' \u00b7 ') : 'Custom catalog';
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
async function importConfig() {
  const raw = document.getElementById('import-url').value.trim();
  const fb  = document.getElementById('import-feedback');
  fb.className = '';

  try {
    // Pull the path segment from any URL shaped like /{segment}/manifest.json.
    // The segment may be "{config_token}" or "{config_token}~{session_key}".
    const match = raw.match(/\\/([A-Za-z0-9+/=_~-]+)\\/manifest\\.json/i);
    if (!match) throw new Error('No config token found — paste a full manifest URL');

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
      config = { catalogs: parsed.c.map(entry => {
        const id = entry.i || '';
        if (PRESET_IDS.has(id)) {
          const cat = { id, name: entry.n || PRESET_DEFAULT_NAMES[id], type: 'preset' };
          if (entry.r) cat.randomize = true;
          return cat;
        } else if (entry.w) {
          const cat = { id, name: entry.n || id, type: 'watching' };
          if (entry.s) cat.listStatus = entry.s;
          if (entry.r) cat.randomize = true;
          if (entry.cf && Object.keys(entry.cf).length) cat.clientFilters = entry.cf;
          return cat;
        } else if (entry.a) {
          const cat = { id, name: entry.n || 'AI Recommendations', type: 'ai',
                        model: entry.m || 'meta-llama/llama-3.3-70b-instruct' };
          if (entry.r) cat.randomize = true;
          return cat;
        } else {
          const cat = { id, name: entry.n || id, type: 'custom', filters: entry.f || {} };
          if (entry.r) cat.randomize = true;
          return cat;
        }
      })};
    } else {
      config = parsed;
    }

    if (!config || !Array.isArray(config.catalogs)) throw new Error('Invalid configuration data');
    if (!config.catalogs.length) throw new Error('No catalogs found in this config');

    catalogs = config.catalogs;
    // Restore session key from the imported URL if present.
    // Session keys expire after 24 hours — if stale the user will need to reconnect.
    if (sessionPart && sessionPart !== _sessionKey) {
      _sessionKey = sessionPart;
      fetchMe(); // validate against /api/me and render auth UI
    }
    document.getElementById('import-url').value = '';
    render();

    const n = catalogs.length;
    fb.textContent = '\u2713 Imported ' + n + ' catalog' + (n !== 1 ? 's' : '');
    fb.className = 'visible ok';
    setTimeout(() => { fb.className = ''; }, 3000);
  } catch(e) {
    fb.textContent = '\u2717 ' + e.message;
    fb.className = 'visible err';
  }
}

// ── URL generation ────────────────────────────────
let _currentManifestUrl = '';
let _qrInstance = null;

async function updateUrl() {
  const compact = catalogs.map(cat => {
    if (PRESET_IDS.has(cat.id)) {
      const entry = { i: cat.id };
      if (cat.name && cat.name !== PRESET_DEFAULT_NAMES[cat.id]) entry.n = cat.name;
      if (cat.randomize) entry.r = true;
      return entry;
    } else if (cat.type === 'watching') {
      const entry = { i: cat.id, n: cat.name, w: true };
      if (cat.listStatus) entry.s = cat.listStatus;
      if (cat.randomize) entry.r = true;
      if (cat.clientFilters && Object.keys(cat.clientFilters).length) entry.cf = cat.clientFilters;
      return entry;
    } else if (cat.type === 'ai') {
      const entry = { i: cat.id, n: cat.name, a: true };
      const defaultModel = 'meta-llama/llama-3.3-70b-instruct';
      if (cat.model && cat.model !== defaultModel) entry.m = cat.model;
      if (cat.randomize) entry.r = true;
      return entry;
    } else {
      const entry = { i: cat.id, n: cat.name, f: cat.filters || {} };
      if (cat.randomize) entry.r = true;
      return entry;
    }
  });
  // Session key is NOT embedded in the payload — it travels as a path suffix.
  const payload = { c: compact };
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

  // Append session key with '~' separator when authenticated.
  // '~' is unreserved in RFC 3986 and never appears in base64url output.
  const segment = _sessionKey ? `${configToken}~${_sessionKey}` : configToken;
  const url = `${BASE_URL}/${segment}/manifest.json`;
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

function openInStremio() {
  if (!_currentManifestUrl) return;
  const stremioUrl = _currentManifestUrl.replace(/^https?:\\/\\//, 'stremio://');
  window.location.href = stremioUrl;
}

async function copyUrl() {
  const url = _currentManifestUrl || document.getElementById('url-display').textContent;
  await navigator.clipboard.writeText(url);
  const btn = document.getElementById('copy-url-btn');
  btn.textContent = '✓ Copied';
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

  document.addEventListener('keydown', e => {
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
    if (e.target?.id === 'ai-modal-overlay') {
      closeAiModal();
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
      case 'add-preset':
        e.preventDefault();
        addPreset(actionEl.dataset.id, actionEl.dataset.name);
        return;
      case 'add-account-preset':
        e.preventDefault();
        addAccountPreset(actionEl.dataset.id, actionEl.dataset.name, actionEl.dataset.status);
        return;
      case 'add-ai':
        e.preventDefault();
        addAiCatalog();
        return;
      case 'open-ai-modal':
        e.preventDefault();
        e.stopPropagation();
        openAiModal();
        return;
      case 'open-stremio':
        e.preventDefault();
        openInStremio();
        return;
      case 'copy-url':
        e.preventDefault();
        copyUrl();
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
fetchMe();

render();
setActiveFilter('genres');
renderFilterTags();
</script>

<!-- AI Settings Modal -->
<div class="ai-modal-overlay" id="ai-modal-overlay">
  <div class="ai-modal">
    <div class="ai-modal-header">
      <div class="ai-modal-title">AI Recommendations Settings</div>
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
          <input type="password" id="ai-key-input" class="ai-modal-input" placeholder="sk-or-v1-\u2026" autocomplete="off">
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
</body>
</html>"""
