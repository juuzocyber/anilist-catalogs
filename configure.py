CONFIGURE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AniList Catalogs — Configure</title>
<style>
  :root {
    --bg:       #000000;
    --surface:  #0a0a0a;
    --card:     #1c1c1e;
    --card2:    #2c2c2e;
    --fill:     rgba(120,120,128,0.20);
    --fill2:    rgba(120,120,128,0.12);
    --sep:      rgba(84,84,88,0.55);
    --text:     #ffffff;
    --text2:    rgba(235,235,245,0.60);
    --text3:    rgba(235,235,245,0.25);
    --radius:   12px;
    --radius-lg:18px;
    --pill:     50px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }

  /* ── Layout ─────────────────────────────────── */
  .app { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

  header {
    border-bottom: 0.5px solid var(--sep);
    padding: 16px 28px;
    display: flex;
    align-items: center;
    background: rgba(0,0,0,0.72);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 10;
  }
  .brand { display: flex; align-items: center; gap: 10px; }
  header img { width: 24px; height: 24px; border-radius: 6px; }
  header h1 { font-size: 15px; font-weight: 400; letter-spacing: 0.01em; }
  .header-sub {
    font-size: 12px;
    color: var(--text3);
    margin-left: 8px;
    padding-left: 8px;
    border-left: 0.5px solid var(--sep);
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
    padding: 28px 20px 0;
    border-right: 0.5px solid var(--sep);
    overflow-y: auto;
    background: linear-gradient(180deg, #0e0e10 0%, #020202 100%);
    display: flex; flex-direction: column;
  }
  .left-panel-content { flex: 1; }
  .left-panel-footer {
    position: sticky; bottom: 0;
    border-top: 0.5px solid var(--sep);
    padding: 14px 0;
    background: #020202;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
  }
  .left-panel-footer .pane-footer-icons { display: flex; align-items: center; gap: 14px; }
  .left-panel-footer .pane-footer-text { font-size: 10px; color: var(--text3); }

  /* ── Mid panel — preview ─────────────────────── */
  .mid-panel {
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: #000000;
  }
  #preview-pane { overflow-y: auto; flex: 1; }

  /* ── Filter bar ──────────────────────────────── */
  .filter-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 12px 28px;
    border-bottom: 0.5px solid var(--sep);
    flex-shrink: 0;
  }
  /* Filter pill buttons (same style as genres btn) */
  .fb-filter-btn {
    display: flex; align-items: center; justify-content: center; gap: 5px;
    background: var(--fill2); border: 0.5px solid transparent;
    border-radius: 20px; color: var(--text2); cursor: pointer;
    padding: 0 10px; font-size: 12px; font-family: inherit;
    height: 32px; flex: 1; min-width: 0;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
  }
  .fb-filter-btn:hover { background: var(--fill); border-color: var(--sep); color: var(--text); }
  .fb-filter-btn.active { border-color: rgba(255,255,255,0.2); color: var(--text); background: var(--card2); }
  .fb-filter-btn.active .fb-chevron { transform: rotate(180deg); }
  .fb-filter-btn.has-value { color: var(--text); border-color: var(--sep); }
  /* Option pills inside the shared filter opts panel */
  .filter-opts-pills { display: flex; flex-wrap: wrap; gap: 6px; }
  .filter-opt-pill {
    padding: 4px 11px; border-radius: var(--pill);
    border: 0.5px solid var(--sep); background: var(--fill2);
    color: var(--text2); font-size: 12px; font-family: inherit;
    cursor: pointer; transition: background 0.15s, color 0.15s, border-color 0.15s;
  }
  .filter-opt-pill:hover { background: var(--fill); color: var(--text); border-color: rgba(255,255,255,0.12); }
  .filter-opt-pill.selected { background: #ffffff; border-color: #ffffff; color: #000000; font-weight: 500; }
  .filter-opt-pill.disabled { opacity: 0.35; cursor: default; }
  /* Name input + Add button inline in filter bar */
  .fb-name-input {
    height: 32px; border-radius: 20px; padding: 0 14px;
    font-size: 12px; background: var(--fill2);
    border: 0.5px solid var(--sep); color: var(--text);
    font-family: inherit; min-width: 0; width: 100%;
  }
  .fb-name-input::placeholder { color: var(--text3); }
  .fb-name-input:focus { outline: none; background: var(--card2); border-color: rgba(255,255,255,0.25); }
  .btn-fb { height: 32px; padding: 0 16px; border-radius: 20px; font-size: 12px; }
  .fb-add-btn {
    height: 32px; padding: 0 16px; border-radius: 20px; font-size: 12px;
    font-family: inherit; font-weight: 500; cursor: pointer; flex-shrink: 0;
    background: var(--card2); border: 0.5px solid rgba(255,255,255,0.12);
    color: var(--text);
    transition: background 0.15s, border-color 0.15s, color 0.15s;
  }
  .fb-add-btn:hover { background: var(--fill); border-color: rgba(255,255,255,0.22); color: #fff; }
  .fb-chevron { transition: transform 0.15s ease; font-size: 9px; opacity: 0.5; }
  .fb-sep { width: 0.5px; height: 18px; background: var(--sep); flex-shrink: 0; margin: 0 2px; }
  .fb-adult-toggle {
    display: flex; align-items: center; gap: 5px;
    background: var(--fill2); border: 0.5px solid transparent;
    border-radius: 20px; color: var(--text2); cursor: pointer;
    padding: 0 10px; font-size: 12px; font-family: inherit;
    height: 32px; flex-shrink: 0; user-select: none;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
  }
  .fb-adult-toggle:hover { background: var(--fill); border-color: var(--sep); color: var(--text); }
  .fb-adult-toggle.active { background: rgba(232,93,4,0.12); border-color: rgba(232,93,4,0.45); color: #e85d04; }
  .fb-adult-toggle input[type=checkbox] { width: 12px; height: 12px; accent-color: #e85d04; cursor: pointer; margin: 0; }
  /* Inline score slider in filter bar */
  .fb-slider-wrap {
    display: flex; align-items: center; gap: 8px;
    background: var(--fill2); border: 0.5px solid transparent;
    border-radius: 20px; padding: 0 14px; height: 32px;
    flex: 1.5; min-width: 0;
    transition: background 0.15s, border-color 0.15s;
  }
  .fb-slider-wrap:hover { background: var(--fill); border-color: var(--sep); }
  .fb-slider-label { font-size: 12px; color: var(--text3); white-space: nowrap; }
  .fb-slider-wrap input[type=range] {
    flex: 1; min-width: 40px; height: 3px; margin: 0;
    -webkit-appearance: none; border-radius: 2px;
    background: rgba(255,255,255,0.15); outline: none;
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
    padding: 12px 28px 14px; border-bottom: 0.5px solid var(--sep);
    flex-shrink: 0; max-height: 150px; overflow-y: auto;
  }

  .fb-name-wrap { position: relative; flex: 1.5; min-width: 0; display: flex; }
  .fb-name-wrap .fb-name-input { flex: 1; }
  #catalog-name-error {
    display: none; position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%);
    font-size: 11px; color: #fff; background: #e85d04; border-radius: 6px;
    padding: 4px 10px; white-space: nowrap; pointer-events: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4); z-index: 20;
  }
  #catalog-name-error::after {
    content: ''; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%);
    border: 5px solid transparent; border-bottom-color: #e85d04;
  }

  /* ── Pane tab bar (Preview / Catalogs switch) ─── */
  .pane-tabbar {
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px; padding: 10px 28px 8px; flex-shrink: 0; flex-wrap: wrap;
    border-bottom: 0.5px solid var(--sep);
  }
  .pane-tabs {
    display: flex; background: var(--fill2); border-radius: 20px;
    padding: 3px; gap: 2px; flex-shrink: 0;
  }
  .pane-tab {
    padding: 4px 14px; border-radius: 17px; border: none; cursor: pointer;
    font-size: 12px; font-family: inherit; font-weight: 500;
    color: var(--text3); background: transparent;
    transition: background 0.15s, color 0.15s;
  }
  .pane-tab:hover { color: var(--text2); }
  .pane-tab.active { background: var(--card); color: var(--text); box-shadow: 0 1px 3px rgba(0,0,0,0.3); }
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
  .filter-tags { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; min-height: 22px; flex-shrink: 0; }
  .filter-tag {
    display: inline-flex; align-items: center; gap: 3px;
    padding: 3px 10px; border-radius: var(--pill);
    background: var(--fill); color: var(--text2);
    font-size: 12px; font-weight: 500; cursor: default;
    transition: background 0.15s, color 0.15s; user-select: none;
  }
  .filter-tag:hover { background: var(--card2); color: var(--text); }
  .filter-tag-x {
    display: none; cursor: pointer; margin-left: 2px;
    color: var(--text3); font-size: 14px; line-height: 1; font-weight: 400;
  }
  .filter-tag:hover .filter-tag-x { display: inline; }
  .filter-tag-x:hover { color: var(--text); }
  .filter-tag-clear {
    display: none; background: none;
    border: 0.5px solid var(--sep); border-radius: var(--pill);
    color: var(--text3); font-size: 11px; font-family: inherit;
    padding: 3px 10px; cursor: pointer; gap: 5px;
    transition: color 0.15s, border-color 0.15s;
  }
  .filter-tags:hover .filter-tag-clear { display: inline-flex; align-items: center; }
  .filter-tag-clear:hover { color: var(--text2); border-color: var(--text3); }

  /* ── Pane tabbar layout ──────────────────────── */
  .pane-tabbar-left { display: flex; align-items: center; gap: 12px; min-width: 0; flex: 1; }
  .filter-tags-wrap { display: flex; align-items: center; gap: 6px; min-width: 0; }
  .tags-icon { color: var(--text3); flex-shrink: 0; }

  /* ── Sort dropdown ───────────────────────────── */
  .sort-dropdown { position: relative; flex-shrink: 0; }
  .sort-btn {
    display: flex; align-items: center; gap: 5px;
    background: none; border: none; cursor: pointer;
    font-size: 11px; color: var(--text3); padding: 4px 8px;
    border-radius: 7px; font-family: inherit;
    transition: background 0.15s, color 0.15s;
  }
  .sort-btn:hover { background: var(--fill); color: var(--text2); }
  .sort-btn.open  { background: var(--fill); color: var(--text2); }
  .sort-btn-label { font-weight: 500; color: var(--text2); }
  .sort-btn-chevron { font-size: 8px; opacity: 0.5; transition: transform 0.15s; }
  .sort-btn.open .sort-btn-chevron { transform: rotate(180deg); }
  .sort-menu {
    display: none; position: absolute; right: 0; top: calc(100% + 6px);
    background: var(--card); border-radius: 10px;
    border: 0.5px solid var(--sep);
    box-shadow: 0 8px 28px rgba(0,0,0,0.55);
    min-width: 160px; z-index: 100; overflow: hidden;
  }
  .sort-menu-item {
    display: block; width: 100%;
    padding: 9px 16px; text-align: left;
    background: none; border: none; border-bottom: 0.5px solid var(--sep);
    cursor: pointer; font-size: 13px; color: var(--text2); font-family: inherit;
    transition: background 0.1s, color 0.1s;
  }
  .sort-menu-item:last-child { border-bottom: none; }
  .sort-menu-item:hover { background: var(--fill); color: var(--text); }
  .sort-menu-item.active { color: var(--text); font-weight: 500; }

  /* ── View controls ───────────────────────────── */
  .view-controls { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
  .view-sep { color: var(--sep); font-size: 14px; }
  .view-toggle { display: flex; gap: 2px; }
  .view-btn {
    background: none; border: none; cursor: pointer;
    color: var(--text3); padding: 5px; border-radius: 7px;
    display: flex; align-items: center;
    transition: background 0.15s, color 0.15s;
  }
  .view-btn:hover { background: var(--fill); color: var(--text2); }
  .view-btn.active { background: var(--fill); color: var(--text); }

  /* ── List view ───────────────────────────────── */
  .preview-list { display: flex; flex-direction: column; }
  .list-item {
    display: grid;
    grid-template-columns: 44px 1fr 90px 120px 140px;
    gap: 20px; align-items: center;
    padding: 10px 4px;
    border-bottom: 0.5px solid var(--sep);
    text-decoration: none; color: inherit;
    border-radius: 8px;
    transition: background 0.15s;
  }
  .list-item:last-child { border-bottom: none; }
  .list-item:hover { background: rgba(255,255,255,0.03); }
  .list-thumb {
    width: 44px; height: 62px; border-radius: 6px;
    overflow: hidden; background: var(--card); flex-shrink: 0;
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
    display: inline-block; padding: 2px 7px; border-radius: 4px;
    font-size: 10px; font-weight: 500; line-height: 1.4;
  }
  .list-score { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }
  .list-score-pct { font-size: 13px; font-weight: 600; color: var(--text); display: flex; align-items: center; gap: 4px; }
  .list-al-icon { width: 11px; height: 11px; border-radius: 2px; opacity: 0.7; }
  .list-stat { font-size: 11px; color: var(--text3); }
  .list-meta-col { display: flex; flex-direction: column; gap: 3px; }
  .list-meta-primary { font-size: 12px; color: var(--text2); }
  .list-meta-secondary { font-size: 11px; color: var(--text3); }

  /* ── Detail card view ───────────────────────── */
  .detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 12px;
    padding: 20px 28px 28px;
  }
  .detail-card {
    display: flex; border-radius: var(--radius);
    overflow: hidden; background: var(--card);
    color: inherit; cursor: pointer;
    transition: background 0.15s;
    height: 230px;
  }
  .detail-card:hover { background: var(--card2); }
  .detail-poster {
    flex: 0 0 35%; position: relative; overflow: hidden; background: var(--fill2);
  }
  .detail-poster img { width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; }
  .detail-poster-overlay {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 32px 9px 8px;
    background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.72) 40%, rgba(0,0,0,0.88) 100%);
    pointer-events: none;
  }
  .detail-overlay-inner {
    background: rgba(0,0,0,0.35);
    border-radius: 5px;
    padding: 4px 7px 5px;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
  }
  .detail-overlay-title {
    font-size: 11px; font-weight: 700; color: #fff;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    line-height: 1.3; letter-spacing: -0.1px;
  }
  .detail-overlay-studio {
    font-size: 10px; font-weight: 500; margin-top: 1px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .detail-body {
    flex: 1; min-width: 0; padding: 11px 12px 10px;
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
    padding: 2px 9px 2px 7px;
  }
  .detail-score-icon { width: 13px; height: 13px; border-radius: 3px; object-fit: cover; flex-shrink: 0; }
  .detail-meta { font-size: 11px; color: var(--text3); flex-shrink: 0; }
  .detail-desc {
    font-size: 11px; color: var(--text2); line-height: 1.55;
    flex: 1; overflow-y: auto; min-height: 0;
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
    border-radius: var(--radius);
    border: 0.5px dashed var(--sep);
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
    grid-template-columns: repeat(auto-fill, minmax(175px, 1fr));
    gap: 18px;
    padding: 20px 28px 28px;
  }
  .poster { display: flex; flex-direction: column; gap: 7px; width: 175px; flex-shrink: 0; text-decoration: none; color: inherit; cursor: pointer; }
  .poster-img {
    border-radius: 10px;
    overflow: hidden;
    aspect-ratio: 2/3;
    background: var(--card);
    position: relative;
  }
  .poster-img img {
    width: 100%; height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.22s ease;
  }
  .poster:hover .poster-img img { transform: scale(1.04); }
  .poster-genres {
    position: absolute;
    top: 0; left: 0; right: 0;
    padding: 8px 6px 20px;
    display: flex; flex-wrap: wrap; gap: 3px;
    background: linear-gradient(180deg, rgba(0,0,0,0.78) 0%, transparent 100%);
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
  }
  .poster:hover .poster-genres { opacity: 1; }
  .poster-genres .genre-badge { font-size: 9px; padding: 2px 6px; }
  .poster-meta {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 7px 8px;
    background: rgba(0,0,0,0.57);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
  }
  .poster:hover .poster-meta { opacity: 1; }
  .poster-meta-row { font-size: 10px; color: rgba(255,255,255,0.92); font-weight: 500; }
  .poster-meta-sub { font-size: 10px; color: rgba(255,255,255,0.55); margin-top: 2px; }
  .poster-title {
    font-size: 12px;
    color: var(--text2);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .poster-score {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    color: var(--text3);
    margin-top: -3px;
  }
  .poster-anilist-logo { width: 13px; height: 13px; border-radius: 3px; flex-shrink: 0; }

  /* ── Section headings ────────────────────────── */
  .section-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 10px;
    padding-left: 2px;
  }
  section { margin-bottom: 32px; }

  /* ── Preset list — Apple grouped rows ────────── */
  .presets-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .preset-card {
    background: var(--card);
    border: 0.5px solid var(--sep);
    border-radius: var(--radius);
    padding: 13px 14px;
    cursor: pointer;
    transition: background 0.15s ease;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .preset-card:hover  { background: var(--card2); }
  .preset-card:active { background: var(--fill); }
  .preset-info { flex: 1; min-width: 0; }
  .preset-name { font-weight: 500; font-size: 13px; letter-spacing: -0.1px; }
  .preset-desc { font-size: 11px; color: var(--text2); margin-top: 2px; }
  .preset-badge {
    font-size: 10px;
    font-weight: 500;
    padding: 2px 9px;
    border-radius: var(--pill);
    background: rgba(255,255,255,0.12);
    color: var(--text);
    flex-shrink: 0;
    display: none;
  }
  .preset-card.added .preset-badge { display: block; }
  .preset-chevron {
    color: var(--text3);
    font-size: 16px;
    flex-shrink: 0;
    line-height: 1;
    transition: color 0.15s;
  }
  .preset-card:hover .preset-chevron { color: var(--text2); }

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
    padding: 16px 24px 24px;
    display: flex; flex-direction: column; gap: 10px;
  }
  .catalogs-side-col {
    flex: 0 0 320px; border-left: 0.5px solid var(--sep);
    padding: 16px 20px; display: flex; flex-direction: column; gap: 0;
    overflow-y: auto; background: var(--bg);
  }
  .catalogs-side-col .divider { margin: 12px 0; }

  /* ── Buttons ─────────────────────────────────── */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 9px 16px;
    border-radius: 10px;
    border: none;
    font-size: 13px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: opacity 0.15s, transform 0.1s ease;
    white-space: nowrap;
    letter-spacing: -0.1px;
    -webkit-font-smoothing: antialiased;
  }
  .btn:hover  { opacity: 0.78; }
  .btn:active { transform: scale(0.97); opacity: 1; }
  .btn-primary { background: #ffffff; color: #000000; }
  .btn-ghost   { background: var(--fill); color: var(--text); }
  .btn-danger  { background: var(--fill2); color: var(--text2); }
  .btn-sm  { padding: 7px 13px; font-size: 12px; }
  .btn-full { width: 100%; }

  /* ── Panel headings ──────────────────────────── */
  .panel-title { font-size: 13px; font-weight: 600; color: var(--text); letter-spacing: -0.1px; }
  .panel-sub   { font-size: 12px; color: var(--text2); margin-top: 2px; }

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
    background: var(--card);
    border: 0.5px solid var(--sep);
    border-radius: var(--radius);
    padding: 14px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: background 0.15s ease, transform 0.12s ease, box-shadow 0.12s ease;
    position: relative;
    cursor: pointer;
  }
  .catalog-item:hover { background: var(--card2); }
  .catalog-item.active-preview {
    background: var(--card2);
    box-shadow: inset 2px 0 0 rgba(255,255,255,0.25);
  }
  .catalog-item.dragging { opacity: 0.35; }
  .catalog-item .drag-handle { color: var(--text3); cursor: grab; font-size: 13px; flex-shrink: 0; line-height: 1; }
  .catalog-item .drag-handle:active { cursor: grabbing; }
  .catalog-item-info { flex: 1; min-width: 0; }
  .catalog-item-name { font-size: 13px; font-weight: 500; letter-spacing: -0.1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .catalog-item-type { font-size: 11px; color: var(--text3); margin-top: 1px; }
  .catalog-rename-input {
    font-size: 13px; font-weight: 500; letter-spacing: -0.1px;
    background: var(--fill2); border: 0.5px solid rgba(235,235,245,0.35);
    border-radius: 6px; color: var(--text);
    padding: 2px 7px; width: 100%; outline: none;
  }
  .catalog-rename-input:focus { border-color: rgba(235,235,245,0.6); }
  .catalog-type-badge {
    font-size: 10px; font-weight: 600;
    padding: 2px 8px;
    border-radius: var(--pill);
    flex-shrink: 0;
    background: rgba(235,235,245,0.07); color: var(--text3);
    letter-spacing: 0.01em;
    border: 0.5px solid var(--sep);
  }
  .catalog-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
  .remove-btn, .shuffle-btn, .edit-btn {
    display: flex; align-items: center; gap: 5px;
    padding: 5px 11px; border-radius: 7px; border: none;
    font-size: 11px; font-weight: 500; font-family: inherit;
    cursor: pointer; flex-shrink: 0;
    transition: background 0.15s, color 0.15s, opacity 0.15s;
  }
  .edit-btn   { background: var(--fill); color: var(--text2); }
  .shuffle-btn { background: var(--fill); color: var(--text2); }
  .remove-btn { background: rgba(220,38,38,0.15); color: #f87171; }
  .edit-btn:hover   { background: var(--card2); color: var(--text); }
  .shuffle-btn:hover { background: var(--card2); color: var(--text); }
  .shuffle-btn.active { background: var(--fill); color: var(--text); }
  .remove-btn:hover { background: rgba(220,38,38,0.28); color: #fca5a5; }
  .catalog-num {
    flex-shrink: 0; width: 28px; height: 28px;
    border-radius: 8px; background: var(--fill2);
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 600; color: var(--text3);
  }
  .catalog-count-badge {
    font-size: 11px; font-weight: 500; color: var(--text2);
    background: var(--fill2); border-radius: var(--pill);
    padding: 2px 10px; flex-shrink: 0;
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
    padding: 28px;
    background: var(--card);
    border-radius: var(--radius);
  }
  .empty-icon { font-size: 28px; opacity: 0.35; }

  /* ── URL output ──────────────────────────────── */
  .btn-stremio {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; padding: 10px 16px; border-radius: 10px; border: none;
    background: var(--fill); color: var(--text);
    font-size: 13px; font-weight: 600; font-family: inherit;
    cursor: pointer; letter-spacing: -0.1px;
    transition: opacity 0.15s, transform 0.1s, background 0.15s;
    -webkit-font-smoothing: antialiased;
  }
  .btn-stremio:hover  { background: var(--card2); }
  .btn-stremio:active { transform: scale(0.97); }
  .url-alt-label { font-size: 11px; color: var(--text3); margin: 12px 0 8px; line-height: 1.6; }
  .qr-localhost-notice { font-size: 11px; color: var(--text3); text-align: center; line-height: 1.5; margin-top: 4px; }
  .url-box { background: var(--card); border-radius: var(--radius); padding: 14px; }
  .url-box-row { display: flex; align-items: flex-start; gap: 8px; }
  .url-text {
    font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
    font-size: 11px; color: var(--text2);
    word-break: break-all; line-height: 1.65;
    max-height: 72px; overflow-y: auto;
    margin-bottom: 10px; cursor: text; user-select: all;
    scrollbar-width: thin; scrollbar-color: var(--sep) transparent;
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
  .copy-row { display: flex; gap: 8px; }
  .copy-feedback { font-size: 11px; color: var(--text3); margin-top: 4px; display: none; }
  .copy-feedback.show { display: block; }
  .qr-section { margin-top: 0; }
  .qr-wrap {
    background: var(--card); border-radius: var(--radius); padding: 12px;
    display: flex; flex-direction: column; align-items: center; gap: 8px;
  }
  #qr-canvas-wrap canvas { border-radius: 6px; display: block; }
  .qr-sub { font-size: 11px; color: var(--text3); text-align: center; line-height: 1.5; }
  .important-note {
    padding: 10px 12px;
    border: 0.5px solid var(--sep); border-radius: var(--radius);
    font-size: 11px; color: var(--text3); line-height: 1.6;
    background: var(--fill2);
  }
  .important-note strong { color: var(--text2); }

  /* ── Divider ─────────────────────────────────── */
  .divider { border: none; border-top: 0.5px solid var(--sep); margin: 24px 0; }

  /* ── Drag-over lift ─────────────────────────── */
  .catalog-item.drag-over {
    transform: translateY(-3px) scale(1.015);
    background: var(--card2) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.45);
    z-index: 1;
    border-radius: var(--radius) !important;
  }

  /* ── Auth header section ─────────────────────────── */
  .header-auth { margin-left: auto; display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
  .btn-connect {
    display: flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 20px; border: 0.5px solid var(--sep);
    background: var(--fill2); color: var(--text2);
    font-size: 12px; font-weight: 500; font-family: inherit;
    cursor: pointer; text-decoration: none;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
  }
  .btn-connect:hover { background: var(--fill); color: var(--text); border-color: rgba(255,255,255,0.15); }
  .auth-connected { display: flex; align-items: center; gap: 8px; }
  .auth-avatar { width: 26px; height: 26px; border-radius: 50%; border: 1.5px solid var(--sep); object-fit: cover; flex-shrink: 0; }
  .auth-name { font-size: 12px; color: var(--text2); font-weight: 500; }
  .btn-disconnect {
    padding: 4px 10px; border-radius: 20px; border: 0.5px solid var(--sep);
    background: none; color: var(--text3); font-size: 11px; font-family: inherit;
    cursor: pointer; transition: color 0.15s, border-color 0.15s;
  }
  .btn-disconnect:hover { color: #f87171; border-color: rgba(248,113,113,0.4); }

  /* ── Error / auth banners ────────────────────────── */
  .error-banner {
    display: none; padding: 10px 28px; flex-shrink: 0;
    background: rgba(220,38,38,0.12); border-bottom: 0.5px solid rgba(220,38,38,0.35);
    font-size: 12px; color: #f87171; font-weight: 500;
  }
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
  .preset-card.account-locked { opacity: 0.4; cursor: not-allowed; pointer-events: none; }
  .account-badge {
    font-size: 10px; font-weight: 600; padding: 2px 8px;
    border-radius: var(--pill); flex-shrink: 0;
    background: rgba(235,235,245,0.07); color: var(--text3);
    letter-spacing: 0.01em;
    border: 0.5px solid var(--sep);
  }

  /* ── AI Recommendations pill ─────────────────────── */
  .preset-card.ai-no-key { border: 0.5px solid rgba(220,38,38,0.45) !important; }
  .preset-card.ai-no-key:hover { border-color: rgba(220,38,38,0.7) !important; }
  .ai-gear-btn {
    display: none; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 50%; flex-shrink: 0;
    border: none; background: var(--fill); color: var(--text3);
    cursor: pointer; font-size: 12px; line-height: 1;
    transition: background 0.15s, color 0.15s;
  }
  .preset-card:not(.account-locked):hover .ai-gear-btn { display: flex; }
  .ai-gear-btn:hover { background: var(--card2); color: var(--text); }
  .ai-connected-tag {
    font-size: 10px; font-weight: 600; padding: 2px 7px;
    border-radius: var(--pill); flex-shrink: 0;
    background: rgba(34,197,94,0.10); color: #22c55e;
    letter-spacing: 0.01em; border: 0.5px solid rgba(34,197,94,0.3);
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
  .ai-modal-save:hover { opacity: 0.85; }
  .ai-modal-save:disabled { opacity: 0.4; cursor: not-allowed; }

  @media (max-width: 1024px) {
    main { grid-template-columns: 326px 1fr; }
  }
  @media (max-width: 768px) {
    main { grid-template-columns: 1fr; }
    .mid-panel { border-top: 0.5px solid var(--sep); }
    header { padding: 14px 20px; }
    .header-sub { display: none; }
  }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
</head>
<body>
<div class="app">
  <header>
    <div class="brand">
      <img src="https://anilist.co/img/icons/android-chrome-512x512.png" alt="AniList">
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
        <div class="presets-grid">
          <div class="preset-card" id="preset-anilist-popular-season" onclick="addPreset('anilist-popular-season','Popular This Season')">
            <div class="preset-info">
              <div class="preset-name">Popular This Season</div>
              <div class="preset-desc">Top anime airing right now</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card" id="preset-anilist-airing-week" onclick="addPreset('anilist-airing-week','Airing This Week')">
            <div class="preset-info">
              <div class="preset-name">Airing This Week</div>
              <div class="preset-desc">New episodes this week</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card" id="preset-anilist-trending" onclick="addPreset('anilist-trending','Trending Now')">
            <div class="preset-info">
              <div class="preset-name">Trending Now</div>
              <div class="preset-desc">What everyone's watching</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card" id="preset-anilist-top-rated" onclick="addPreset('anilist-top-rated','Top Rated All Time')">
            <div class="preset-info">
              <div class="preset-name">Top Rated All Time</div>
              <div class="preset-desc">Highest scored anime ever</div>
            </div>
            <span class="account-badge">Preset</span><div class="preset-badge">Added</div>
            <span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-ai-recommendations" onclick="addAiCatalog()">
            <div class="preset-info">
              <div class="preset-name">AI Recommendations</div>
              <div class="preset-desc">Personalised picks powered by AI</div>
            </div>
            <span class="account-badge" style="background:rgba(139,92,246,0.12);color:#a78bfa;border-color:rgba(139,92,246,0.3)">AI</span>
            <div class="preset-badge">Added</div>
            <button class="ai-gear-btn" id="ai-gear-btn" onclick="event.stopPropagation();openAiModal()" title="Configure AI settings">&#9881;</button>
            <span class="ai-connected-tag" id="ai-connected-tag" style="display:none">Connected</span>
            <span class="preset-chevron">&#8250;</span>
          </div>
        </div>
      </section>

      <hr class="divider">

      <section>
        <div class="section-title">AniList Profile Catalogs</div>
        <div class="presets-grid" id="account-presets-grid">
          <div class="preset-card account-locked" id="preset-anilist-watching-current" onclick="addAccountPreset('anilist-watching-current','Currently Watching','CURRENT')">
            <div class="preset-info"><div class="preset-name">Currently Watching</div><div class="preset-desc">Anime you're actively watching</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-planning" onclick="addAccountPreset('anilist-watching-planning','Plan to Watch','PLANNING')">
            <div class="preset-info"><div class="preset-name">Plan to Watch</div><div class="preset-desc">Your watch list</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-completed" onclick="addAccountPreset('anilist-watching-completed','Completed','COMPLETED')">
            <div class="preset-info"><div class="preset-name">Completed</div><div class="preset-desc">Anime you've finished</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-paused" onclick="addAccountPreset('anilist-watching-paused','Paused','PAUSED')">
            <div class="preset-info"><div class="preset-name">Paused</div><div class="preset-desc">On hold</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-dropped" onclick="addAccountPreset('anilist-watching-dropped','Dropped','DROPPED')">
            <div class="preset-info"><div class="preset-name">Dropped</div><div class="preset-desc">Anime you've stopped watching</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-watching-repeating" onclick="addAccountPreset('anilist-watching-repeating','Rewatching','REPEATING')">
            <div class="preset-info"><div class="preset-name">Rewatching</div><div class="preset-desc">Currently rewatching</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
          <div class="preset-card account-locked" id="preset-anilist-favourites" onclick="addAccountPreset('anilist-favourites','My Favourites','FAVOURITES')">
            <div class="preset-info"><div class="preset-name">My Favourites</div><div class="preset-desc">Your starred anime</div></div>
            <span class="account-badge">Account</span><div class="preset-badge">Added</div><span class="preset-chevron">&#8250;</span>
          </div>
        </div>
      </section>
      </div><!-- end .left-panel-content -->
      <div class="left-panel-footer">
        <div class="pane-footer-icons">
          <a class="pane-footer-icon" href="https://github.com/juuzocyber/anilist-catalogs" target="_blank" rel="noopener" title="GitHub">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
          </a>
          <a class="pane-footer-icon" href="#" title="Buy me a coffee">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.89 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z"/></svg>
          </a>
        </div>
        <div class="pane-footer-text">Version: v1.1.2 &mdash; Developed by juuzo</div>
      </div>
    </div>

    <!-- MID: Filters + Preview + Catalogs -->
    <div class="mid-panel">

      <!-- Filter bar -->
      <div class="filter-bar">
        <button class="fb-filter-btn" id="btn-genres" onclick="setActiveFilter('genres')">
          <span id="lbl-genres">Genres</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-year" style="display:none">
          <option value="">Year</option>
          __YEAR_OPTIONS__
        </select>
        <button class="fb-filter-btn" id="btn-year" onclick="setActiveFilter('year')">
          <span id="lbl-year">Year</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-season" style="display:none">
          <option value="">Season</option>
          <option value="CURRENT">Current Season</option>
          <option value="WINTER">Winter</option>
          <option value="SPRING">Spring</option>
          <option value="SUMMER">Summer</option>
          <option value="FALL">Fall</option>
        </select>
        <button class="fb-filter-btn" id="btn-season" onclick="setActiveFilter('season')">
          <span id="lbl-season">Season</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-format" style="display:none">
          <option value="">Format</option>
          <option value="TV">TV Series</option>
          <option value="TV_SHORT">TV Short</option>
          <option value="MOVIE">Movie</option>
          <option value="OVA">OVA</option>
          <option value="ONA">ONA</option>
          <option value="SPECIAL">Special</option>
        </select>
        <button class="fb-filter-btn" id="btn-format" onclick="setActiveFilter('format')">
          <span id="lbl-format">Format</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-status" style="display:none">
          <option value="">Status</option>
          <option value="RELEASING">Airing</option>
          <option value="FINISHED">Finished</option>
          <option value="NOT_YET_RELEASED">Upcoming</option>
        </select>
        <button class="fb-filter-btn" id="btn-status" onclick="setActiveFilter('status')">
          <span id="lbl-status">Status</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <select id="f-sort" style="display:none">
          <option value="POPULARITY_DESC">Popularity</option>
          <option value="TRENDING_DESC">Trending</option>
          <option value="SCORE_DESC">Score</option>
          <option value="START_DATE_DESC">Newest</option>
          <option value="FAVOURITES_DESC">Favourites</option>
        </select>
        <div class="fb-sep"></div>
        <div class="fb-slider-wrap">
          <span class="fb-slider-label">Score</span>
          <input type="range" id="f-score" min="0" max="90" step="10" value="0"
                 oninput="document.getElementById('score-val').textContent = this.value > 0 ? this.value + '+' : 'Any'; scheduleAutoPreview()">
          <span class="fb-slider-val" id="score-val">Any</span>
        </div>
        <select id="f-daterange" style="display:none">
          <option value="">Date Range</option>
          <option value="this-week">This Week</option>
          <option value="this-month">This Month</option>
          <option value="last-month">Last Month</option>
          <option value="this-year">This Year</option>
          <option value="last-year">Last Year</option>
        </select>
        <button class="fb-filter-btn" id="btn-daterange" onclick="setActiveFilter('daterange')">
          <span id="lbl-daterange">Date Range</span>
          <span class="fb-chevron">&#9660;</span>
        </button>
        <label class="fb-adult-toggle" id="adult-toggle">
          <input type="checkbox" id="f-adult" onchange="onAdultChange()">
          Adult
        </label>
        <div class="fb-sep"></div>
        <div class="fb-name-wrap" id="catalog-name-wrap">
          <input class="fb-name-input" type="text" id="catalog-name" placeholder="Catalog name" oninput="clearNameError()">
          <div id="catalog-name-error">Name required</div>
        </div>
        <button class="fb-add-btn" id="catalog-add-btn" onclick="addCustom()">Add</button>
      </div>

      <!-- Always-visible options panel -->
      <div class="options-panel" id="options-panel">
        <div class="filter-opts-pills" id="filter-opts-pills"></div>
      </div>

      <!-- Pane tab bar: Preview / Catalogs switch -->
      <div class="pane-tabbar">
        <div class="pane-tabbar-left">
          <div class="pane-tabs">
            <button class="pane-tab active" id="tab-preview" onclick="setPaneTab('preview')">Preview</button>
            <button class="pane-tab" id="tab-catalogs" onclick="setPaneTab('catalogs')">Your Catalogs</button>
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
              <button class="sort-btn" id="sort-btn" onclick="toggleSortMenu()">
                <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor" style="opacity:0.5"><path d="M3 2v8M3 10l-2-2M3 10l2-2M9 10V2M9 2L7 4M9 2l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/></svg>
                <span class="sort-btn-label" id="sort-btn-label">Popularity</span>
                <span class="sort-btn-chevron">&#9660;</span>
              </button>
              <div class="sort-menu" id="sort-menu">
                <button class="sort-menu-item active" data-value="POPULARITY_DESC" onclick="setSortValue('POPULARITY_DESC')">Popularity</button>
                <button class="sort-menu-item" data-value="TRENDING_DESC" onclick="setSortValue('TRENDING_DESC')">Trending</button>
                <button class="sort-menu-item" data-value="SCORE_DESC" onclick="setSortValue('SCORE_DESC')">Average Score</button>
                <button class="sort-menu-item" data-value="START_DATE_DESC" onclick="setSortValue('START_DATE_DESC')">Newest</button>
                <button class="sort-menu-item" data-value="FAVOURITES_DESC" onclick="setSortValue('FAVOURITES_DESC')">Favorites</button>
              </div>
            </div>
            <span class="view-sep">|</span>
            <div class="view-toggle">
              <button class="view-btn active" id="view-btn-grid" onclick="setView('grid')" title="Grid view">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><rect x="0" y="0" width="6" height="6" rx="1.5"/><rect x="8" y="0" width="6" height="6" rx="1.5"/><rect x="0" y="8" width="6" height="6" rx="1.5"/><rect x="8" y="8" width="6" height="6" rx="1.5"/></svg>
              </button>
              <button class="view-btn" id="view-btn-detail" onclick="setView('detail')" title="Detail view">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor"><rect x="0" y="0" width="5" height="6" rx="1"/><rect x="7" y="0" width="7" height="2" rx="0.75"/><rect x="7" y="3" width="5" height="1.5" rx="0.5"/><rect x="7" y="5" width="6" height="1" rx="0.5"/><rect x="0" y="8" width="5" height="6" rx="1"/><rect x="7" y="8" width="7" height="2" rx="0.75"/><rect x="7" y="11" width="5" height="1.5" rx="0.5"/><rect x="7" y="13" width="6" height="1" rx="0.5"/></svg>
              </button>
              <button class="view-btn" id="view-btn-list" onclick="setView('list')" title="List view">
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
      <div id="catalogs-pane" style="display:none">
        <div class="catalogs-list-col">
          <div style="display:flex;align-items:center;justify-content:space-between;min-height:20px">
            <div class="panel-sub-inline">Drag to reorder &middot; click to preview</div>
            <span class="catalog-count-badge" id="catalog-count-badge" style="display:none"></span>
          </div>
          <div class="catalog-list" id="catalog-list"></div>
        </div>
        <div class="catalogs-side-col">
          <div class="section-title">Install AniList Catalogs</div>
          <button class="btn-stremio" onclick="openInStremio()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/></svg>
            Add to Stremio
          </button>
          <div style="text-align:center;font-size:11px;color:var(--text3);margin:10px 0">OR</div>
          <div class="url-box">
            <div class="url-text" id="url-display">—</div>
            <div class="copy-row">
              <button class="btn btn-ghost btn-sm btn-full" onclick="copyUrl()">Copy URL</button>
              <div class="url-warn-icon" id="token-warning">
                &#9888;
                <div class="url-warn-tooltip">This URL contains a session key for your AniList account. Keep it private and do not share it. If it expires, just reconnect AniList.</div>
              </div>
              <div class="copy-feedback" id="copy-feedback">&#10003; Copied</div>
            </div>
          </div>

          <div style="text-align:center;font-size:11px;color:var(--text3);margin:10px 0">OR</div>
          <div class="qr-section" style="margin-top:0">
            <div class="qr-wrap">
              <div class="qr-sub">Scan this QR code with your mobile device</div>
              <div id="qr-canvas-wrap"></div>
              <div class="qr-sub">The QR code contains the Stremio URL for your addon. Scan it with your smartphone to install in the Stremio mobile app.</div>
            </div>
          </div>

          <div style="margin-top:auto">
            <hr class="divider" style="margin:12px 0">
            <div class="section-title">Import Config</div>
            <div style="display:flex;gap:8px;">
              <input type="text" id="import-url" placeholder="Paste manifest URL…" style="flex:1;font-size:12px;padding:7px 10px">
              <button class="btn btn-ghost btn-sm" onclick="importConfig()">Import</button>
            </div>
            <div id="import-feedback" style="font-size:11px;margin-top:8px;display:none;line-height:1.5"></div>
          </div>
        </div>
      </div>

    </div>

  </main>
</div>

<script>
const GENRES = ["Action","Adventure","Comedy","Drama","Ecchi","Fantasy","Horror","Mahou Shoujo","Mecha","Music","Mystery","Psychological","Romance","Sci-Fi","Slice of Life","Sports","Supernatural","Thriller"];
const BASE_URL = window.location.origin;

const GENRE_COLORS = {
  'Action':'#e85d04','Adventure':'#f48c06','Comedy':'#a7c957','Drama':'#4895ef',
  'Ecchi':'#f72585','Fantasy':'#7b2fbe','Horror':'#9b2226','Mahou Shoujo':'#f48fb1',
  'Mecha':'#4361ee','Music':'#c77dff','Mystery':'#0077b6','Psychological':'#bc6c25',
  'Romance':'#e63946','Sci-Fi':'#48cae4','Slice of Life':'#52b788',
  'Sports':'#2dc653','Supernatural':'#9d4edd','Thriller':'#d62828',
};
const STUDIO_COLORS = {
  'MAPPA':'#e85d04','Ufotable':'#7b2fbe','Kyoto Animation':'#4895ef',
  'Wit Studio':'#52b788','MADHOUSE':'#48cae4','Bones':'#f48c06',
  'Toei Animation':'#e63946','A-1 Pictures':'#4361ee','CloverWorks':'#c77dff',
  'David Production':'#f4c430','Trigger':'#e84393','J.C.Staff':'#0077b6',
  'Shaft':'#9d4edd','Production I.G':'#3d8f4a','P.A. Works':'#bc6c25',
  'Doga Kobo':'#a7c957','Studio KAI':'#48cae4','White Fox':'#52b788',
  'Brains Base':'#f48c06','Sunrise':'#e85d04',
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
// Session key: a short 12-char token handed back by the OAuth callback.
// The actual encrypted AniList token lives server-side; only this key travels
// in the manifest URL (as "{config_token}~{session_key}").
let _sessionKey = _urlParams.get('s') || null;
// OpenRouter state — populated from /api/me response on load.
let _hasOrKey = false;
let _orModel  = 'meta-llama/llama-3.3-70b-instruct';
// Clean the ?s= handoff param from the configure page URL immediately — it
// doesn't belong in the browser history and the key is now held in memory.
if (_sessionKey) {
  const _cleanUrl = new URL(window.location.href);
  _cleanUrl.searchParams.delete('s');
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
    el.innerHTML =
      '<div class="auth-connected">' +
      (user.avatar ? '<img class="auth-avatar" src="' + escHtml(user.avatar) + '" alt="">' : '') +
      '<span class="auth-name">' + escHtml(user.name) + '</span>' +
      '<button class="btn-disconnect" onclick="disconnect()">Disconnect</button>' +
      '</div>';
  } else {
    el.innerHTML =
      '<a class="btn-connect" href="/oauth/login" onclick="saveConfigBeforeLogin()">' +
      '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" style="opacity:0.7"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>' +
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
      card.style.pointerEvents = locked ? 'none' : '';
    }
  });
  // AI pill: locked when not authenticated, red outline when authenticated but no OR key
  const aiCard = document.getElementById('preset-anilist-ai-recommendations');
  if (aiCard) {
    aiCard.classList.toggle('account-locked', locked);
    aiCard.style.pointerEvents = locked ? 'none' : '';
    aiCard.classList.toggle('ai-no-key', !locked && !_hasOrKey);
    const connTag = document.getElementById('ai-connected-tag');
    if (connTag) connTag.style.display = (!locked && _hasOrKey) ? '' : 'none';
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
    fetch('/oauth/logout?s=' + encodeURIComponent(_sessionKey)).catch(() => {});
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
  wrap.style.display   = hideForSource ? 'none' : '';
  addBtn.style.display = hideForSource ? 'none' : '';

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

// Fetch source content from the server and then apply client-side filters.
async function fetchAndShowSource() {
  if (!activeSource) return;
  const captured = activeSource;

  if (activeSource.type === 'watching') {
    if (!_sessionKey) {
      document.getElementById('preview-sub').textContent = activeSource.name;
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#128274;</div><div>Account catalog<br><span style="font-size:11px;color:var(--text3)">Connect your AniList account to preview this list</span></div></div>';
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
        `<div class="preview-prompt"><div>Could not load account catalog</div><div style="font-size:11px;color:var(--text3);margin-top:6px">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
    }
    return;
  }

  if (activeSource.type === 'ai') {
    if (!_sessionKey) {
      document.getElementById('preview-sub').textContent = activeSource.name;
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#128274;</div><div>Account catalog<br><span style="font-size:11px;color:var(--text3)">Connect your AniList account to use AI recommendations</span></div></div>';
      return;
    }
    if (!_hasOrKey) {
      document.getElementById('preview-sub').textContent = activeSource.name;
      document.getElementById('preview-area').innerHTML =
        '<div class="preview-prompt"><div class="preview-prompt-icon">&#9881;</div><div>OpenRouter key required<br><span style="font-size:11px;color:var(--text3)">Click the gear icon on the AI pill to add your key</span></div></div>';
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
        `<div class="preview-prompt"><div>Could not load AI recommendations</div><div style="font-size:11px;color:var(--text3);margin-top:6px">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
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
      customInput.style.display = 'none';
    } else {
      select.value = 'custom';
      customInput.style.display = 'block';
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
    customInput.style.display = 'block';
    customInput.focus();
  } else {
    customInput.style.display = 'none';
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
    Page(page:1,perPage:24){
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

function scoreColor(s) {
  if (s >= 80) return '#2d6a4f';
  if (s >= 70) return '#52b788';
  if (s >= 60) return '#f48c06';
  return '#e63946';
}

function renderGridView(media) {
  return '<div class="preview-grid">' + media.map(m => {
    const title  = escHtml(m.title.english || m.title.romaji || '');
    const score  = m.averageScore ? (m.averageScore / 10).toFixed(1) : '';
    const scoreCol = m.averageScore ? scoreColor(m.averageScore) : 'var(--text3)';
    const genres = (m.genres || []).slice(0, 3).map(g => {
      const c = GENRE_COLORS[g] || '#888';
      return `<span class="genre-badge" style="background:${c}bb;color:#fff;border:0.5px solid ${c}dd;cursor:pointer" onclick="event.preventDefault();event.stopPropagation();applyGenreFilter('${escHtml(g)}')">${escHtml(g)}</span>`;
    }).join('');
    const fmt    = FORMAT_LABELS[m.format] || m.format || '';
    const eps    = m.episodes ? m.episodes + ' ep' + (m.episodes !== 1 ? 's' : '') : '';
    const metaTop = [fmt, eps].filter(Boolean).join(' · ');
    let metaSub = '';
    if (m.nextAiringEpisode) {
      const t = m.nextAiringEpisode.timeUntilAiring;
      const d = Math.floor(t / 86400), h = Math.floor(t / 3600);
      metaSub = `Ep ${m.nextAiringEpisode.episode} in ${d > 0 ? d + 'd' : h + 'h'}`;
    }
    return `<a class="poster" href="https://anilist.co/anime/${m.id}" target="_blank" rel="noopener">
      <div class="poster-img">
        <img src="${escHtml(m.coverImage.large)}" alt="${title}" loading="lazy">
        <div class="poster-genres">${genres}</div>
        <div class="poster-meta">
          ${metaTop ? `<div class="poster-meta-row">${escHtml(metaTop)}</div>` : ''}
          ${metaSub ? `<div class="poster-meta-sub">${escHtml(metaSub)}</div>` : ''}
        </div>
      </div>
      <div class="poster-title">${title}</div>
      <div class="poster-score">
        ${score ? `<img class="poster-anilist-logo" src="https://anilist.co/img/icons/android-chrome-512x512.png" alt=""><span style="color:${scoreCol}">${score}</span>` : ''}
      </div>
    </a>`;
  }).join('') + '</div>';
}

function renderListView(media) {
  function airingText(nae) {
    if (!nae) return '';
    const t = nae.timeUntilAiring;
    const d = Math.floor(t / 86400), h = Math.floor(t / 3600);
    return `Ep ${nae.episode} in ${d > 0 ? d + 'd' : h + 'h'}`;
  }
  return '<div class="preview-list">' + media.map(m => {
    const title   = escHtml(m.title.english || m.title.romaji || '');
    const score   = m.averageScore ? m.averageScore + '%' : '\u2014';
    const scoreCol = m.averageScore ? scoreColor(m.averageScore) : 'var(--text3)';
    const users   = m.popularity ? (m.popularity >= 1000 ? (m.popularity / 1000).toFixed(0) + 'K' : m.popularity) + ' users' : '';
    const format  = escHtml(FORMAT_LABELS[m.format] || m.format || '');
    const eps     = m.episodes ? m.episodes + ' ep' + (m.episodes !== 1 ? 's' : '') : '';
    const period  = [SEASON_LABELS[m.season], m.seasonYear].filter(Boolean).map(escHtml).join(' ');
    const airing  = escHtml(airingText(m.nextAiringEpisode));
    const statusL = escHtml(STATUS_LABELS[m.status] || m.status || '');
    const genres  = (m.genres || []).slice(0, 3).map(g => {
      const c = GENRE_COLORS[g] || '#888';
      return `<span class="genre-badge" style="background:${c}28;color:${c};border:0.5px solid ${c}55;cursor:pointer" onclick="event.preventDefault();event.stopPropagation();applyGenreFilter('${escHtml(g)}')">${escHtml(g)}</span>`;
    }).join('');
    return `<a class="list-item" href="https://anilist.co/anime/${m.id}" target="_blank" rel="noopener">
      <div class="list-thumb"><img src="${escHtml(m.coverImage.large)}" alt="${title}" loading="lazy"></div>
      <div class="list-main">
        <div class="list-title">${title}</div>
        <div class="list-genres">${genres}</div>
      </div>
      <div class="list-score">
        <div class="list-score-pct"><img class="list-al-icon" src="https://anilist.co/img/icons/android-chrome-512x512.png" alt=""><span style="color:${scoreCol}">${score}</span></div>
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
    const title   = escHtml(m.title.english || m.title.romaji || '');
    const score   = m.averageScore || 0;
    const fmt     = FORMAT_LABELS[m.format] || m.format || '';
    const eps     = m.episodes ? m.episodes + (m.episodes !== 1 ? ' episodes' : ' episode') : '';
    const meta    = [fmt, eps].filter(Boolean).join(' \u00b7 ');
    const period  = [SEASON_LABELS[m.season], m.seasonYear].filter(Boolean).join(' ');
    const airing  = airingStr(m.nextAiringEpisode);
    const studio  = ((m.studios && m.studios.nodes && m.studios.nodes[0]) || {}).name || '';
    const studioColor = STUDIO_COLORS[studio] || 'rgba(235,235,245,0.55)';
    const desc    = m.description ? escHtml(m.description.replace(/<[^>]*>/g, '').replace(/\\n/g, ' ')) : '';
    const themeColor = STUDIO_COLORS[studio] || null;
    const genres  = (m.genres || []).slice(0, 3).map(g => {
      const c = themeColor || GENRE_COLORS[g] || '#888';
      const lighter = themeColor ? (GENRE_COLORS[g] || c) : c;
      return `<span class="genre-badge" style="background:${lighter}22;color:${lighter}cc;border:0.5px solid ${lighter}44;cursor:pointer" onclick="event.stopPropagation();applyGenreFilter('${escHtml(g)}')">${escHtml(g)}</span>`;
    }).join('');
    const sc = scoreColor(score);
    const scoreBadge = score ? `<div class="detail-score-badge" style="background:${sc}"><img class="detail-score-icon" src="https://anilist.co/img/icons/android-chrome-512x512.png" alt="AL">${score}%</div>` : '';
    const headerLeft = airing
      ? `<div class="detail-airing-label">Ep ${airing.ep} airing in</div><div class="detail-airing-time">${escHtml(airing.time)}</div>`
      : `<div class="detail-period">${escHtml(period)}</div>`;
    return `<div class="detail-card" onclick="window.open('https://anilist.co/anime/${m.id}','_blank')">
      <div class="detail-poster">
        <img src="${escHtml(m.coverImage.large)}" alt="${title}" loading="lazy">
        <div class="detail-poster-overlay">
          <div class="detail-overlay-inner">
            <div class="detail-overlay-title">${title}</div>
            ${studio ? `<div class="detail-overlay-studio" style="color:${studioColor}">${escHtml(studio)}</div>` : ''}
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
    </div>`;
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
  const isOpen = menu.style.display === 'block';
  if (isOpen) { closeSortMenu(); } else {
    menu.style.display = 'block';
    document.getElementById('sort-btn').classList.add('open');
  }
}
function closeSortMenu() {
  const menu = document.getElementById('sort-menu');
  if (menu) menu.style.display = 'none';
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
  document.getElementById('preview-pane').style.display = tab === 'preview' ? '' : 'none';
  document.getElementById('catalogs-pane').style.display = tab === 'catalogs' ? 'flex' : 'none';
  document.getElementById('preview-tab-extras').style.display = tab === 'preview' ? '' : 'none';
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
    `<span class="filter-tag" onclick="event.stopPropagation()">${escHtml(t.label)}<span class="filter-tag-x" onclick="removeFilter('${escHtml(t.key)}')">&#10005;</span></span>`
  ).join('') + (tags.length ? '<button class="filter-tag-clear" onclick="clearAllFilters()">Clear All &#10005;</button>' : '');
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
      `<div class="preview-prompt"><div>Could not reach AniList API</div><div style="font-size:11px;color:var(--text3);margin-top:6px">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
  }
}

// ── Add custom ────────────────────────────────────
function clearNameError() {
  const inp = document.getElementById('catalog-name');
  const err = document.getElementById('catalog-name-error');
  inp.style.borderColor = '';
  err.style.display = 'none';
}

function addCustom() {
  const nameInput = document.getElementById('catalog-name');
  const name = nameInput.value.trim();
  if (!name) {
    nameInput.style.borderColor = '#e85d04';
    const errEl = document.getElementById('catalog-name-error');
    errEl.style.display = 'block';
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
  try {
    const media = cat.type === 'preset'
      ? cat.id === 'anilist-airing-week'
        ? await fetchAiringWeekPreview()
        : await fetchPreview(PRESET_VARS[cat.id]())
      : await fetchPreview(filtersToVars(cat.filters));
    renderPreview(media, `${cat.name} \u2014 ${media.length} titles`);
  } catch(e) {
    console.error('[preview] Error:', e);
    document.getElementById('preview-sub').textContent = 'Failed to load preview';
    document.getElementById('preview-area').innerHTML =
      `<div class="preview-prompt"><div>Could not reach AniList API</div><div style="font-size:11px;color:var(--text3);margin-top:6px">${escHtml(e instanceof Error ? e.message : String(e))}</div></div>`;
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
    autoPreviewTimer = setTimeout(previewCustom, 1000);
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
    countBadge.style.display = catalogs.length > 0 ? '' : 'none';
  }
  if (catalogs.length === 0) {
    list.innerHTML = '<div class="empty-state"><div class="empty-icon">&#127916;</div><div>No catalogs yet.<br>Use Quick Add or the builder.</div></div>';
  } else {
    list.innerHTML = catalogs.map((c, i) => `
      <div class="catalog-item ${previewingId === c.id ? 'active-preview' : ''}" draggable="true" data-id="${c.id}"
           ondragstart="dragStart(event,${i})" ondragover="dragOver(event,${i})"
           ondrop="drop(event,${i})" ondragleave="dragLeave(event)"
           onclick="previewCatalog('${c.id}')">
        <span class="drag-handle" onclick="event.stopPropagation()">&#8597;</span>
        <div class="catalog-num">${i + 1}</div>
        <div class="catalog-item-info">
          ${renamingId === c.id
            ? `<input class="catalog-rename-input" data-rename-id="${c.id}" value="${escHtml(c.name)}"
                 onclick="event.stopPropagation()"
                 onblur="commitRename('${c.id}', this.value)"
                 onkeydown="if(event.key==='Enter'){this.blur();}if(event.key==='Escape'){cancelRename();}">`
            : `<div class="catalog-item-name">${escHtml(c.name)}</div>`
          }
          <div class="catalog-item-type"><span class="catalog-type-badge">${c.type === 'watching' ? 'Account' : c.type === 'ai' ? 'AI' : c.type === 'custom' ? 'Custom' : 'Preset'}</span></div>
        </div>
        <div class="catalog-actions" onclick="event.stopPropagation()">
          <button class="edit-btn" onclick="startRenaming('${c.id}')">&#9998; Rename</button>
          <button class="shuffle-btn ${c.randomize ? 'active' : ''}" onclick="toggleRandomize('${c.id}')">${SHUFFLE_ICON} Randomize</button>
          <button class="remove-btn" onclick="removeCatalog('${c.id}')">&#128465; Remove</button>
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
  document.querySelectorAll('.catalog-item').forEach(el => el.classList.remove('drag-over'));
  e.currentTarget.classList.add('drag-over');
}
function dragLeave(e) { e.currentTarget.classList.remove('drag-over'); }
function drop(e, i) {
  e.preventDefault();
  document.querySelectorAll('.catalog-item').forEach(el => el.classList.remove('drag-over', 'dragging'));
  dragMoved = false;
  if (dragIdx === null || dragIdx === i) { dragIdx = null; return; }
  const moved = catalogs.splice(dragIdx, 1)[0];
  catalogs.splice(i, 0, moved);
  dragIdx = null;
  render();
}
document.addEventListener('dragend', () => {
  dragMoved = false;
  document.querySelectorAll('.catalog-item.dragging').forEach(el => el.classList.remove('dragging'));
});

// ── Import config from manifest URL ──────────────
async function importConfig() {
  const raw = document.getElementById('import-url').value.trim();
  const fb  = document.getElementById('import-feedback');
  fb.style.display = 'none';

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
    fb.style.color = 'var(--text2)';
    fb.textContent = '\u2713 Imported ' + n + ' catalog' + (n !== 1 ? 's' : '');
    fb.style.display = 'block';
    setTimeout(() => { fb.style.display = 'none'; }, 3000);
  } catch(e) {
    fb.style.color = '#e85d04';
    fb.textContent = '\u2717 ' + e.message;
    fb.style.display = 'block';
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

  // qrcodejs creates a canvas immediately and an img shortly after
  wrap.querySelectorAll('canvas, img').forEach(el => { el.style.borderRadius = '6px'; });
  const observer = new MutationObserver(() => {
    wrap.querySelectorAll('canvas, img').forEach(el => { el.style.borderRadius = '6px'; });
  });
  observer.observe(wrap, { childList: true });
  setTimeout(() => observer.disconnect(), 500);

}

function openInStremio() {
  if (!_currentManifestUrl) return;
  const stremioUrl = _currentManifestUrl.replace(/^https?:\\/\\//, 'stremio://');
  window.location.href = stremioUrl;
}

async function copyUrl() {
  const url = _currentManifestUrl || document.getElementById('url-display').textContent;
  await navigator.clipboard.writeText(url);
  const fb = document.getElementById('copy-feedback');
  fb.classList.add('show');
  setTimeout(() => fb.classList.remove('show'), 2000);
}

// ── Init ──────────────────────────────────────────
catalogs = [
  { id: 'anilist-popular-season', name: 'Popular This Season', type: 'preset' },
  { id: 'anilist-airing-week',    name: 'Airing This Week',    type: 'preset' },
  { id: 'anilist-trending',       name: 'Trending Now',        type: 'preset' },
  { id: 'anilist-top-rated',      name: 'Top Rated All Time',  type: 'preset' },
];

// Show auth error banner if redirected back with ?error=auth_failed
if (_urlParams.get('error') === 'auth_failed') {
  const banner = document.getElementById('error-banner');
  if (banner) {
    banner.textContent = 'Failed to authenticate with AniList. Please try again.';
    banner.style.display = 'block';
  }
  // Clean error param from URL without reloading
  const cleanUrl = new URL(window.location.href);
  cleanUrl.searchParams.delete('error');
  window.history.replaceState({}, '', cleanUrl.toString());
}

// Bootstrap auth UI — validates token against /api/me if present
fetchMe();

render();
setActiveFilter('genres');
renderFilterTags();
</script>

<!-- AI Settings Modal -->
<div class="ai-modal-overlay" id="ai-modal-overlay" onclick="if(event.target===this)closeAiModal()">
  <div class="ai-modal">
    <div class="ai-modal-header">
      <div class="ai-modal-title">AI Recommendations Settings</div>
      <button class="ai-modal-close" onclick="closeAiModal()">&#10005;</button>
    </div>
    <div class="ai-modal-body">
      <div class="ai-modal-section">
        <label class="ai-modal-label">Model</label>
        <select id="ai-model-select" class="ai-modal-select" onchange="handleAiModelChange()">
          <option value="meta-llama/llama-3.3-70b-instruct">Llama 3.3 70B Instruct (Default &mdash; fast &amp; cheap)</option>
          <option value="google/gemini-flash-1.5">Gemini Flash 1.5 (Fast)</option>
          <option value="openai/gpt-4o-mini">GPT-4o Mini (Accurate)</option>
          <option value="anthropic/claude-haiku-4-5-20251001">Claude Haiku 4.5 (Fast)</option>
          <option value="custom">Custom model&hellip;</option>
        </select>
        <input type="text" id="ai-model-custom" class="ai-modal-input" placeholder="e.g. mistralai/mixtral-8x7b-instruct" style="display:none;margin-top:6px">
      </div>
      <div class="ai-modal-section">
        <label class="ai-modal-label">OpenRouter API Key</label>
        <div class="ai-key-row">
          <input type="password" id="ai-key-input" class="ai-modal-input" placeholder="sk-or-v1-\u2026" autocomplete="off">
          <button class="ai-test-btn" id="ai-test-btn" onclick="testOrKey()">Test</button>
        </div>
        <div class="ai-key-feedback" id="ai-key-feedback"></div>
        <div class="ai-key-hint">Get a free key at openrouter.ai/keys &mdash; key is encrypted and stored server-side only</div>
      </div>
    </div>
    <div class="ai-modal-footer">
      <button class="ai-modal-cancel" onclick="closeAiModal()">Cancel</button>
      <button class="ai-modal-save" id="ai-modal-save-btn" onclick="saveOrKeyFromModal()">Save</button>
    </div>
  </div>
</div>
</body>
</html>"""
