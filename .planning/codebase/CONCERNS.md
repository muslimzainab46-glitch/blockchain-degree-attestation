# Codebase Concerns

**Analysis Date:** 2026-06-05

## Tech Debt

**Monolithic Single File (`blockchain_degree_attestation_website.html`):**
- **Issue:** All presentation layout (HTML), page styling (CSS), and simulation/state logic (JS) are bundled together in a single file.
- **Why:** Developed as a quick, self-contained mockup or simulation dashboard.
- **Impact:** Harder to modularize, scale, or integrate with real smart contracts or backends. Code readability decreases as size grows.
- **Fix approach:** Split the file into structured directories:
  - `/public` or `/src` for HTML templates
  - `/src/styles` for CSS sheets
  - `/src/js` for JS controllers and services

**Simulated Blockchain Ledger:**
- **Issue:** The blockchain network, mining, and transaction validations are entirely mock operations simulated in browser RAM.
- **Why:** Setup as a pure frontend prototype.
- **Impact:** Refreshing the web browser resets all state data (issued degrees, verified records, mined blocks) back to seed variables.
- **Fix approach:** Connect the frontend to a real Ethereum-compatible blockchain client (e.g. Ganache, Hardhat, or Sepolia testnet) using `ethers.js` or `web3.js` and implement Web3 wallet connectors (e.g. MetaMask).

**Deterministic Hash Collision:**
- **Issue:** The custom `simHash()` function relies on a basic additive string hash algorithm to simulate SHA-256 deterministic hash calculations.
- **Why:** Written to run without external JS library dependencies.
- **Impact:** Susceptible to collisions and doesn't represent standard cryptographic hashing.
- **Fix approach:** Use browser-native `crypto.subtle.digest('SHA-256', ...)` APIs to perform real cryptographic hashing on client inputs.

## Known Bugs

**None:**
- No syntax or UI layout bugs are currently known within the simulation parameters.

## Security Considerations

**Vulnerable Simulated State:**
- **Risk:** Since all state lives in global client-side variables (`S`), malicious users can manipulate values (e.g., adding false degrees, overriding counts) directly from the browser's developer console.
- **Mitigation:** Safe for local prototype use. For production, the database state must be decentralized (smart contract ledger) or secured behind an API server with proper authentication.

---

*Codebase concerns analysis: 2026-06-05*
*Update when security audits or bugs are logged*
