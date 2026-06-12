# Requirements: ChainCred Blockchain Degree Attestation

**Defined:** 2026-06-05
**Core Value:** Ensure absolute academic credential integrity with automated OCR-to-blockchain verification, eliminating manual overhead.

## v1 Requirements

### Authentication & Authorization

- [ ] **AUTH-01**: User sign-up must require and validate `@iqra.edu.pk` email addresses. Non-conforming domains must be rejected.
- [ ] **AUTH-02**: Implement two-factor authentication or email verification during account signup.
- [ ] **AUTH-03**: Secure login with role separation: User/Student Portal and Admin/Management Portal.

### User Portal & Document Upload

- [ ] **USER-01**: Personal information form collecting Name, Father's Name, CNIC Number, Date of Birth, and Passport (optional).
- [ ] **USER-02**: Degree selection dropdown covering BSCS, BSSE, BSCB, and BSAI programs.
- [ ] **DOC-01**: Upload interface allowing users to submit image files (PNG/JPG) for:
  - CNIC Front
  - CNIC Back
  - Matric Marksheet
  - Inter Marksheet

### Payment Flow

- [ ] **PAY-01**: Payment page providing two options: Cryptocurrencies (displaying a destination wallet address) and 1Link transfer.
- [ ] **PAY-02**: Upload interface for payment screenshots/receipts to prove payment.
- [ ] **PAY-03**: Payment status is set to "Pending Admin Verification" after submission.

### OCR & Verification Logic

- [ ] **OCR-01**: Admin-triggered automated OCR pipeline using Python.
- [ ] **OCR-02**: Text extraction from CNIC images to identify and parse the "Expiration Date".
- [ ] **OCR-03**: Text extraction from Inter Marksheet images to parse scores and confirm the aggregate marks/GPA meets the admission threshold.
- [ ] **VER-01**: Validation logic verifying that:
  - The CNIC expiration date is after the current system date.
  - The Inter marksheet aggregate percentage is greater than or equal to 50%.
- [ ] **VER-02**: Requests that fail validation generate alerts detailing the specific failure (e.g. "CNIC Expired" or "Grade Below 50%").

### Smart Contract & Blockchain

- [ ] **BC-01**: Solidity smart contract `DegreeContract.sol` containing functions to issue, revoke, and verify degree hashes.
- [ ] **BC-02**: Python integration using `web3.py` to deploy and interact with the contract on a private blockchain.
- [ ] **BC-03**: Blockchain transactions are recorded in the system audit log and Explorer.

### PDF & QR Code Generation

- [ ] **AGENT-01**: Automated generation of the attested degree as a PDF.
- [ ] **AGENT-02**: Generation of a unique QR code representing the block hash of the degree attestation on the blockchain.
- [ ] **AGENT-03**: Embedding the QR code into the PDF degree. Scanning the QR code links to a public verification page showing the blockchain transaction details.

### UI Styling & Layout

- [ ] **UI-01**: Modern and polished Single Page Application (SPA) dashboard matching a clean Sea Green & White color scheme.

## v2 Requirements

- [ ] **PROD-01**: Integration with real Sepolia/Ethereum testnets.
- [ ] **PROD-02**: Real-world payment gateway integrations (Stripe, 1Link API).

---
*Last updated: 2026-06-05*
