# Codebase Structure

**Analysis Date:** 2026-06-05

## Directory Layout

```
[project-root]/
├── .planning/                              # GSD planning and design state directory
│   └── codebase/                           # Tech stack, architecture, and conventions mapping
│       ├── ARCHITECTURE.md
│       ├── CONCERNS.md
│       ├── CONVENTIONS.md
│       ├── INTEGRATIONS.md
│       ├── STACK.md
│       ├── STRUCTURE.md
│       └── TESTING.md
├── README.md                               # Repository README documentation
├── blockchain_degree_attestation_website.html # Monolithic UI, CSS, and simulation script file
└── [Media Files]/                           # WhatsApp voice/video recordings from user
    ├── WhatsApp Audio 2026-06-03 at 4.15.01 PM.mp4
    ├── WhatsApp Audio 2026-06-03 at 4.15.02 PM (1).mp4
    ├── WhatsApp Audio 2026-06-03 at 4.15.02 PM.mp4
    ├── WhatsApp Audio 2026-06-03 at 4.15.03 PM.mp4
    ├── WhatsApp Audio 2026-06-03 at 4.15.04 PM (1).mp4
    ├── WhatsApp Audio 2026-06-03 at 4.15.04 PM.mp4
    ├── WhatsApp Audio 2026-06-03 at 9.34.19 PM.ogg
    └── WhatsApp Ptt 2026-06-03 at 8.17.25 PM.ogg
```

## Directory Purposes

**`[project-root]`:**
- Purpose: Contains the single-file web application and supporting documentation.
- Contains: `.html` web entry point, `README.md`, and media files.
- Key files: `blockchain_degree_attestation_website.html`

**`.planning/`:**
- Purpose: Stores GSD configuration, plans, requirements, and codebase mappings.
- Contains: Markdown planning documents.
- Key files: `.planning/codebase/*.md`

## Key File Locations

**Application Entry Point:**
- `blockchain_degree_attestation_website.html`: Contains all presentation (HTML), visual styling (CSS), and simulation logic (JS) for the degree attestation blockchain website.

**Documentation:**
- `README.md`: Basic project introduction.

---

*Structure analysis: 2026-06-05*
*Update when directories are restructured or files are added*
