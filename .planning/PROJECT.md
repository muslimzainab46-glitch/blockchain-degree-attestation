# ChainCred - Blockchain Degree Attestation System

## What This Is

ChainCred is a secure, automated blockchain-based academic credential attestation platform. It allows students to register using institutional emails, upload identity and grade documents, and pay fees via simulated payment systems. The platform uses OCR and AI agents to verify documents automatically, deploy smart contract records on a private blockchain network, and generate verifiable PDF degrees embedded with cryptographic QR codes.

## Core Value

Ensure absolute academic credential integrity with automated OCR-to-blockchain verification, eliminating manual overhead.

## Requirements

### Validated

- [x] Client-side dashboard prototype (`blockchain_degree_attestation_website.html`)

### Active

- [ ] **AUTH-01**: Secure registration/login restricted to `@iqra.edu.pk` email domains.
- [ ] **AUTH-02**: Two-factor/Email verification during signup.
- [ ] **USER-01**: User dashboard form for personal metadata (First Name, Last Name, CNIC, Passport) and Degree program selection.
- [ ] **DOC-01**: Document upload interface for CNIC Front, CNIC Back, Matric Marksheet, and Inter Marksheet.
- [ ] **PAY-01**: Payment processing interface (Crypto wallet address hash or 1Link transfer) with receipt/screenshot upload.
- [ ] **ADMIN-01**: Admin dashboard listing attestation requests and audit records.
- [ ] **OCR-01**: Automated document analysis using OCR text extraction from uploaded images.
- [ ] **VER-01**: Validation logic checking CNIC expiration date and verifying Inter marksheet percentage is >= 50%.
- [ ] **BC-01**: Solidity smart contract (`DegreeContract.sol`) deployed to register degree hashes on-chain.
- [ ] **AGENT-01**: AI agent degree generation creating a PDF degree with a QR code referencing the blockchain hash.
- [ ] **UI-01**: Refined responsive web interface styled with a Sea Green & White theme.

### Out of Scope

- [ ] Real payment processor API integrations — only simulated receipt uploads and hash checks are performed.
- [ ] Multi-tenant institutional SSO — authentication is restricted to the simulated domain check.

---
*Last updated: 2026-06-05 after initialization*
