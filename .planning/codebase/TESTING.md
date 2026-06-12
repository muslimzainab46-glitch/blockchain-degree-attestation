# Testing Patterns

**Analysis Date:** 2026-06-05

## Test Framework

**Runner:**
- No automated testing framework (such as Jest, Mocha, Cypress, or Playwright) is currently configured in the workspace.

**Verification Methodology:**
- **Manual Verification:** Interactive verification is performed by loading the static HTML file in a browser and verifying component interactions.

## Manual Verification Scenarios

**1. Base State Initialization:**
- Open the webpage in a browser.
- Verify counts for issued, verified, and fraud match the initial seeded list:
  - Total Issued: 5
  - Verifications: 3
  - Fraud Attempts: 1

**2. Degree Issuance flow:**
- Navigate to the **Issue Degree** page.
- Select FAST-NUCES, enter a student name/ID, graduation date, and CGPA.
- Click **Generate Hash** and check if the SHA-256 hash is generated deterministically in the box.
- Click **Issue on Blockchain** and verify that:
  - Toast notification "Degree issued on-chain..." pops up.
  - The transaction details in the "Transaction Preview" show confirmed status.
  - The block count and transaction log update.

**3. Verification & Fraud detection:**
- Navigate to the **Verify** page.
- Click **Load Valid Hash** to load a valid hash, click **Verify on Blockchain**, and confirm the result says "DEGREE VERIFIED" in green.
- Click **Load Fake Hash** to load a simulated fake hash, click **Verify on Blockchain**, and confirm the result says "FRAUD DETECTED" in red.

**4. Audit Export:**
- Navigate to the **Audit Log** page.
- Click **Export CSV** and verify that a CSV file named `chaincred_audit_log.csv` is downloaded locally.

---

*Testing patterns analysis: 2026-06-05*
*Update when testing frameworks are integrated*
