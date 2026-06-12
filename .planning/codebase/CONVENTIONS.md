# Coding Conventions

**Analysis Date:** 2026-06-05

## Naming Patterns

**Files:**
- Snake_case/spaced naming conventions for top-level files (e.g. `blockchain_degree_attestation_website.html`).

**Functions:**
- camelCase for JavaScript logic functions: `showPage`, `simHash`, `showToast`, `initSeed`, `mineBlock`, `generateHash`, `issueDegree`, `verifyDegree`, `renderDashboard`, `renderExplorer`, `renderAudit`.
- short/abbreviated camelCase utility functions: `rndHex`, `rndGas`, `now`, `shortHash`, `animCount`.

**Variables/Constants:**
- UPPER_CASE for configuration constants: `UNIS`, `EMPLOYERS`, `CONTRACTS`, `PARTICIPANTS`, `SEED`, `SEED_VER`.
- camelCase for standard variables and properties inside state and loops: `hashInput`, `isRevoked`, `matched`, `v-employer`.
- Global state storage named with single capital letter: `S`.

**HTML Elements / DOM Identifiers:**
- Prefixing form controls with `f-` (e.g. `f-university`, `f-name`, `f-sid`, `f-degree`, `f-date`, `f-gpa`, `f-notes`).
- Prefixing verification controls with `v-` (e.g. `v-employer`, `v-hash`).
- Prefixing pages with `p-` (e.g. `p-home`, `p-dashboard`, `p-issue`, `p-verify`, `p-explorer`, `p-audit`).
- Prefixing navigation links with `nav-` (e.g. `nav-home`, `nav-dashboard`).

## Code Style

**Formatting:**
- Compact formatting inside `<script>` blocks with compressed one-liner utility helpers.
- Tabs and single-space margins for main UI control flows.
- Inline CSS styling for minor layout overrides (e.g. `<div style="padding:0">`, `<tbody id="degrees-tbody">`).

**Error Handling:**
- Preemptively testing inputs using conditional checks:
  ```javascript
  if(!sid||!date||!uni){ showToast('Fill in University, Student ID, and Date first.','warn'); return; }
  ```
- Reverting smart contract transaction simulations when verification matches no records on-chain.

---

*Conventions analysis: 2026-06-05*
*Update as conventions develop*
