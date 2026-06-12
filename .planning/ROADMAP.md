# Roadmap: ChainCred Degree Attestation System

## Overview

This roadmap defines the transition of the ChainCred project from a client-side mockup to a fully operational hybrid blockchain-based degree attestation system. The development focuses on setting up the local blockchain environment, constructing the Solidity smart contracts, building the Python backend with OCR validation and Web3 connectivity, and refining the frontend with a premium Sea Green & White UI theme.

## Phases

- [ ] **Phase 1: Solidity Smart Contract & Blockchain Setup** - Create the smart contracts and set up the local blockchain test environment.
- [ ] **Phase 2: Python Backend & Authentication** - Build the API server with restricted email signup and file uploads.
- [ ] **Phase 3: OCR Text Extraction & Verification Logic** - Implement document OCR parsing and verification rules.
- [ ] **Phase 4: Agent Attestation & PDF Generation** - Create PDF degrees with transaction-embedded QR codes.
- [ ] **Phase 5: Refined Sea Green & White Frontend UI** - Refactor the UI and connect it to the Python API.
- [ ] **Phase 6: Integration Testing & Git Deployment** - Run end-to-end verification and push code to GitHub.

## Phase Details

### Phase 1: Solidity Smart Contract & Blockchain Setup
**Goal**: Create blockchain ledger interface and local developer test environment.
**Depends on**: Nothing
**Requirements**: BC-01, BC-02
**Success Criteria**:
  1. Local Ganache or Hardhat network runs successfully in the workspace.
  2. Solidity contract `DegreeContract.sol` compiles and deploys to the test network.
  3. Simple Python script verifies it can read and write data to the deployed contract.
**Plans**: 2 plans

Plans:
- [ ] 01-01: Set up local blockchain test environment (Hardhat/Ganache CLI).
- [ ] 01-02: Write, compile, and deploy `DegreeContract.sol` to the network.

---

### Phase 2: Python Backend & Authentication
**Goal**: Implement the core API backend with restricted access and document upload storage.
**Depends on**: Phase 1
**Requirements**: AUTH-01, AUTH-02, AUTH-03, USER-01, DOC-01
**Success Criteria**:
  1. API server starts and listens to requests locally.
  2. Account signup restricts registration to `@iqra.edu.pk` email domains.
  3. Upload endpoints successfully write CNIC and marksheet files to a local upload directory.
**Plans**: 2 plans

Plans:
- [ ] 02-01: Create FastAPI/Flask application with SQLite database and authentication middleware.
- [ ] 02-02: Implement personal metadata profiles and multipart file upload endpoints.

---

### Phase 3: OCR Text Extraction & Verification Logic
**Goal**: Automate CNIC and marksheet document validation.
**Depends on**: Phase 2
**Requirements**: OCR-01, OCR-02, OCR-03, VER-01, VER-02
**Success Criteria**:
  1. Python script extracts text from uploaded sample CNIC and Inter marksheet images.
  2. Expiration dates are successfully parsed from the CNIC text and compared to current dates.
  3. Verification logic flags marksheet scores below the 50% threshold.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Integrate OCR library (such as `pytesseract` or a dedicated wrapper) in Python.
- [ ] 03-02: Implement CNIC expiration check and aggregate score validation rules.

---

### Phase 4: Agent Attestation & PDF Generation
**Goal**: Issue PDF degrees linked to blockchain record hashes.
**Depends on**: Phase 3
**Requirements**: AGENT-01, AGENT-02, AGENT-03, BC-03
**Success Criteria**:
  1. Attestation triggers PDF compilation containing verified student details.
  2. Web3 transaction records degree hash on-chain and returns block details.
  3. PDF embeds a QR code which, when scanned, redirects to verification URL.
**Plans**: 2 plans

Plans:
- [ ] 04-01: Write Python Web3 integration to broadcast degree hashes on-chain.
- [ ] 04-02: Build PDF compilation logic embedding transaction-linked QR codes.

---

### Phase 5: Refined Sea Green & White Frontend UI
**Goal**: Connect the user and admin views to the Python API with a premium layout.
**Depends on**: Phase 4
**Requirements**: PAY-01, PAY-02, PAY-03, ADMIN-01, UI-01
**Success Criteria**:
  1. The SPA dashboard switches view states using sea green and white themes.
  2. Students can submit metadata, upload documents, and upload payment screenshots.
  3. Admin can view pending requests, trigger OCR verification, and view generated PDFs.
**Plans**: 2 plans

Plans:
- [ ] 05-01: Redesign the SPA dashboard with a modern Sea Green & White styling system.
- [ ] 05-02: Integrate frontend components with the Python API endpoints.

---

### Phase 6: Integration Testing & Git Deployment
**Goal**: Verify the end-to-end system and push all source files to GitHub.
**Depends on**: Phase 5
**Requirements**: v1 Complete
**Success Criteria**:
  1. Full attestation workflow (register -> upload docs -> pay -> OCR verify -> blockchain issue -> PDF QR check) completes successfully.
  2. Git repository has clean commit logs and is pushed to the remote repository.
**Plans**: 1 plan

Plans:
- [ ] 06-01: Run full system walkthrough, verify all criteria, and execute final git push.

---
*Last updated: 2026-06-05*
