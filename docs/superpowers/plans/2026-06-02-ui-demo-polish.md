# UI Demo Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the existing React UI better for AI demo and presentation.

**Architecture:** Keep the current `App.jsx` state-driven layout. Add a play-mode AI analysis panel fed from existing API response fields and client-side elapsed time. Use existing CSS only, no new libraries.

**Tech Stack:** React 18, Vite, CSS.

---

### Task 1: Play Mode AI Analysis

**Files:**
- Modify: `frontend/src/App.jsx`

- [ ] Add state for backend status, AI elapsed time, and last AI move.
- [ ] Populate these fields in `requestAiMove()`.
- [ ] Reset these fields when starting a new game or switching modes.
- [ ] Render an AI analysis panel in play mode.

### Task 2: UI Polish

**Files:**
- Modify: `frontend/src/App.css`

- [ ] Tighten page layout and panel spacing.
- [ ] Add styles for AI analysis rows and status pills.
- [ ] Improve board sizing on desktop and mobile.

### Task 3: Verification

Run:

```powershell
cd frontend
npm.cmd run build
```

Expected: build succeeds.
