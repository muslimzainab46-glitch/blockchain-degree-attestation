# Architecture

**Analysis Date:** 2026-06-05

## Pattern Overview

**Overall:** Monolithic Single-Page Application (SPA) simulation inside a single static HTML file.

**Key Characteristics:**
- All HTML structure, CSS layouts, and JavaScript logic reside in `blockchain_degree_attestation_website.html`.
- Global in-memory state objects simulate blockchain ledger operations.
- Client-side DOM navigation switches views instantly.

## Layers

**View/Presentation Layer:**
- Purpose: Render the UI dashboard, forms, tables, blockchain visualization, and toast notifications.
- Contains: HTML5 markup and vanilla CSS3 selectors.
- Locations: Inline `<style>` tag and `<body>` tags in `blockchain_degree_attestation_website.html`.
- Depends on: State layer for populating dynamic listings.

**State/Simulation Layer:**
- Purpose: Manage the simulated blockchain database, transactions, block creation, and auditing logs.
- Contains: Global JavaScript state objects (`S`), static metadata constants (`UNIS`, `EMPLOYERS`, `PARTICIPANTS`), and business logic functions.
- Locations: Inline `<script>` block in `blockchain_degree_attestation_website.html`.
- Used by: Presentation layer via onclick callbacks.

## Data Flow

**Degree Issuance Lifecycle:**
1. Issuer fills out the metadata form (University, Student Name, Student ID, Degree Type, Graduation Date, CGPA, Notes).
2. Issuer clicks "Generate Hash" which deteminingly computes a SHA-256 hash representation of inputs via `simHash()`.
3. Issuer clicks "Issue on Blockchain" (`issueDegree()`).
4. Logic verifies the Student ID is not a duplicate in the in-memory array `S.degrees`.
5. A new simulated block and transaction are generated, state counts are incremented, and an audit log event is appended.
6. DOM functions (`renderRecentIssues()`, `renderExplorer()`, `renderAudit()`, `renderDashboard()`) update the tables, stats cards, and blockchain visualization.
7. Toast notification confirms block completion.

**Verification Flow:**
1. Verifier selects an employer and inputs a degree hash (or clicks "Load Fake Hash" / "Load Valid Hash").
2. Verifier clicks "Verify on Blockchain" (`verifyDegree()`).
3. Logic searches `S.degrees` for the matching hash.
4. Result is displayed as VALID, REVOKED, or FRAUD, and the details are printed.
5. Verification count is updated, transactions are recorded, audit logs are updated, and the tables are refreshed.

## Key Abstractions

**Global State (`S`):**
- Purpose: Simulated blockchain database.
- Properties: `degrees`, `verifications`, `auditLog`, `blocks`, `transactions`, `blockCount`, `issuedCount`, `verifiedCount`, `fraudCount`, `validVCount`, `fakeVCount`.

**Determinisic Hashing (`simHash`):**
- Purpose: Simulates SHA-256 hash generation of credentials.
- Signature: `simHash(sid, deg, date, uni)` returning a 64-character simulated hex hash.

## Entry Points

**Web Page Load:**
- Location: `blockchain_degree_attestation_website.html`
- Triggers: Browser loading the file.
- Responsibilities: Seeds initial data (`initSeed()`), starts background simulation loops (`liveTicker()`), and sets up dates.

## Error Handling

**Strategy:** Inline validation check and toast notifications.

**Patterns:**
- Input check: Verifies required fields are filled before generating hashes or broadcasting.
- Duplication checks: Prevents duplicate Student IDs on-chain by flashing error toasts.
- Reverted states: Simulates contract execution reverts on invalid verifications.

## Cross-Cutting Concerns

**Logging:**
- Custom simulated `auditLog` in state `S`.
- Event types: `issue`, `verify`, `fraud`, `revoke`.
- Exportable to local CSV format via `exportAudit()`.

**Navigation:**
- JavaScript-driven page swapping using `showPage(id)` which changes styling/visibility class `.page.active`.

---

*Architecture analysis: 2026-06-05*
*Update when major patterns change*
