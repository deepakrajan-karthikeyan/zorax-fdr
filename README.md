🏦 FDR Management Portal
AI-Assisted Security Deposit & Fixed Deposit Receipt Lifecycle Management
Team Zorax · Problem Statement ID: 26265
A secure, centralized portal concept for managing institutional security
deposits and Fixed Deposit Receipts (FDRs) across their administrative
lifecycle---from submission and document review to maturity monitoring,
renewal, and authorized release.
> **Project status:** Prototype / proposed architecture. Update this
> section to reflect which features are currently implemented, in
> progress, or planned.

---
🚩 Problem Statement
Institutions may need to submit or maintain security deposits and FDRs
as part of approval and compliance processes. When records are spread
across spreadsheets, emails, and physical documents, officials can face:
Missing or inconsistent FDR information
Time-consuming manual document review
Missed maturity and renewal deadlines
Limited visibility into pending verification and approval cases
Difficulty tracking changes and maintaining a reliable audit history
💡 Our Solution
The FDR Management Portal brings institution-wise records, instrument
metadata, supporting documents, verification status, deadline reminders,
and release workflows into one role-controlled platform.
Core Features
Centralized FDR Repository --- Store institution and instrument
records in one searchable system.
Digital Document Upload --- Upload FDR PDFs or scans and
associate them with structured records.
AI-Assisted Document Extraction --- Use
OCR/document-intelligence models to extract candidate fields such as
bank name, FDR number, amount, issue date, and maturity date.
Validation & Discrepancy Flags --- Check required fields, date
consistency, and mismatches between extracted and submitted values.
Human Review --- Route low-confidence extractions or
discrepancies to an authorized reviewer.
Maturity Monitoring --- Track approaching and overdue dates and
generate configurable reminders.
Renewal & Replacement Tracking --- Preserve the history of
renewed or replacement instruments.
Release/Refund Workflow --- Track requests, scrutiny, approval
checkpoints, and final status.
Dashboard & Reports --- Summarize active, expiring, matured,
renewed, released, and pending instruments.
Audit Trail & Access Control --- Record important actions and
restrict functions according to user roles.
🔄 Workflow
An institution submits an FDR document and its details.
The system preprocesses the document and extracts candidate
metadata.
Schema checks and business rules validate the submitted fields.
Incomplete, inconsistent, or low-confidence records are sent for
human review.
Authorized officials verify instrument details through approved
sources where available.
The record is stored with its verification status and audit history.
The maturity engine monitors deadlines and sends configured alerts.
Renewal, replacement, or release requests move through the
authorized workflow.
Dashboards and reports show current status and pending actions.
🧠 AI Models & Algorithms
---
Model / Algorithm                   Purpose
---
NVIDIA Nemotron document-parsing    Document layout and field
model*                             extraction
OCR (PaddleOCR or Tesseract)        Text extraction from scanned FDRs
OpenCV preprocessing                Image cleanup and document-quality
checks
JSON Schema / Pydantic validation   Enforce structured metadata formats
Rule-based validation               Check required fields, dates, and
consistency
Fuzzy matching (Levenshtein /       Flag possible text and reference
Jaro-Winkler)                       mismatches
Confidence-threshold routing        Send uncertain results for manual
review
Finite-State Machine (FSM)          Control permitted FDR lifecycle
transitions
Scheduled jobs / priority queues    Prioritize maturity reminders and
overdue actions
RAG + vector embeddings (optional)  Search approved regulations and
guidance documents
Cryptographic hash chaining         Make audit-log tampering detectable
(optional)
*Select the exact NVIDIA model and confirm its current availability,
license, deployment requirements, and suitability before implementation.
AI extraction supports review; it does not independently prove that
an FDR is authentic.
🧰 Proposed Technology Stack
---
Layer                   Technologies            Responsibility
---
Frontend                React, TypeScript,      Responsive dashboards
Tailwind CSS            and role-specific
screens
Backend                 Python, FastAPI,        REST APIs, validation,
Pydantic                and business logic
Database                PostgreSQL              Institution records,
FDR metadata, workflow
states
Document intelligence   NVIDIA document model   Document parsing and
and/or                  preprocessing
PaddleOCR/Tesseract,  
OpenCV
Background jobs         Celery, Redis           Scheduled checks and
asynchronous tasks
Security                OAuth 2.0 / OpenID      Authentication,
Connect, RBAC, TLS,     authorization, and data
encryption              protection
Integrations            Approved bank APIs,     Verification and
email/SMS gateways,     notifications
AICTE APIs where  
available
Version note: Pin and test exact dependency versions in project
files before deployment. The table describes a proposed stack; it should
not be interpreted as proof that every component is already integrated.
🏗️ High-Level Architecture
``` text
Institution / Authorized Official
              |
       React Web Interface
              |
          FastAPI
              |
   Authentication + RBAC
              |
   Document Processing Pipeline
   (OCR / AI Parsing / Validation)
              |
       Human Review Queue
              |
       PostgreSQL Database
          /           \
 Maturity & Alerts   Audit Trail
          \           /
      Dashboard & Reports
      
```
🔐 Security & Responsible Verification
Apply least-privilege role-based access for institutions, reviewers,
and approving authorities.
Protect data in transit with TLS and encrypt stored documents and
backups.
Validate uploaded files and restrict permitted file types and sizes.
Keep sensitive documents in controlled object storage rather than
exposing public links.
Log submissions, reviews, status changes, and approvals with
timestamps and actor identity.
Use approved bank verification mechanisms wherever available.
Keep human authorization in release/refund decisions and other
regulated actions.
Avoid storing unnecessary personal or financial information.
🧪 Suggested Test Scenarios
Submit a complete FDR record and document.
Upload a scan with missing or unreadable fields.
Detect a mismatch between the submitted amount and extracted amount.
Trigger a reminder for an FDR nearing maturity.
Record renewal or replacement and preserve the previous instrument
history.
Submit a release request and verify that only authorized roles can
approve it.
Confirm that every important status change appears in the audit
history.
Verify that one institution cannot access another institution's
restricted records.
📊 Expected Impact
Less repetitive manual tracking
Better visibility into expiring and overdue instruments
More consistent FDR metadata
Faster routing of incomplete records for review
Traceable renewal and release workflows
Improved administrative reporting and accountability
These are intended outcomes. Measure them with prototype tests and
baseline comparisons before claiming quantified improvements.
🚀 Getting Started
Setup instructions depend on the repository implementation. Once the
application code is available, document:
Prerequisites and supported runtime versions
Environment-variable configuration using a `.env.example` file
Database creation and migrations
Backend installation and startup commands
Frontend installation and startup commands
Test commands and sample/demo data
Deployment instructions
Never commit credentials, API keys, production FDRs, or confidential
institutional documents to GitHub.
🗺️ Roadmap
[ ] Institution and instrument registration
[ ] Secure FDR upload and retrieval
[ ] Structured metadata extraction
[ ] Validation and discrepancy review
[ ] Maturity reminders and escalation rules
[ ] Renewal/replacement history
[ ] Authorized release/refund workflow
[ ] Dashboard and exportable reports
[ ] Audit and access-control tests
[ ] Approved external-system integration
👥 Team
Team Zorax
Built as a proposed solution for Problem Statement ID 26265 ---
Streamline of Security Deposit / FDR Portal.
⚖️ Disclaimer
This project is intended to support administrative tracking and review.
It does not replace official bank confirmation, applicable AICTE
regulations, or approval by a competent authority. Verification and
release decisions must follow authorized procedures.
---
If you find this project useful, consider starring the repository and
sharing feedback.
