# Integrations

**Analysis Date:** 2026-06-05

## External Services

**None:**
- This application runs entirely client-side.
- No external HTTP APIs, databases, or third-party web services are connected.

## Simulated Integrations

**Private Ethereum Blockchain:**
- **Consensus:** Clique Proof of Authority (PoA)
- **Chain ID:** 1337
- **Simulated Contracts:**
  - `DegreeContract.sol` (Address: `0xAbC1...2345`) - Handles issuing and revoking degrees
  - `VerificationContract.sol` (Address: `0xDeF6...7890`) - Handles checking hashes and returning history
  - `AccessControl.sol` (Address: `0x1234...ABcd`) - Manages roles (`issuer`, `verifier`, `admin`, `holder`)
- **Simulated Validators:** `Uni-01` node
- **Simulated Gas:** Gas price 20 gwei, transaction gas estimation around ~45,000 gwei for issuance, ~21,450 gwei for verification.

## Data Storage

**In-Memory State:**
- All data is stored in a global JavaScript object `S` (arrays for `degrees`, `verifications`, `auditLog`, `blocks`, and `transactions`).
- Data is reset on browser page refresh.
- CSV export feature downloads simulated audit log event rows locally.

---

*Integration analysis: 2026-06-05*
*Update when external integrations are introduced*
