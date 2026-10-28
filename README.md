
# 🏦 FDR Management Portal
### AI-Powered Security Deposit & Fixed Deposit Receipt Management

**Team Zorax | Problem Statement ID: 26265**

An intelligent, secure, and centralized portal designed to streamline the complete lifecycle of institutional security deposits and Fixed Deposit Receipts (FDRs) for AICTE-related approval and compliance processes.

---

## 🚩 Problem Statement

Managing institutional FDRs through spreadsheets, physical documents, and manual correspondence can cause:

- Missing or inconsistent financial records.
- Delays in document verification.
- Missed FDR maturity and renewal deadlines.
- Limited visibility into pending approvals.
- Difficulty maintaining audit trails and document histories.

## 💡 Our Solution

The FDR Management Portal provides a centralized digital platform for document intelligence, verification tracking, automated maturity monitoring, renewal management, and authorized release workflows.

### ✨ Key Features

- **Centralized Repository:** Institution-wise and instrument-wise FDR records.
- **AI Document Intelligence:** Extract relevant fields from uploaded FDR PDFs and scans.
- **Automated Validation:** Detect missing fields and inconsistent information.
- **Human-in-the-Loop Review:** Route uncertain extractions to authorized officials.
- **Maturity Monitoring:** Track expiry dates and generate advance reminders.
- **Renewal Management:** Maintain renewal and replacement history.
- **Release & Refund Workflow:** Track requests, scrutiny, approvals, and status.
- **Interactive Dashboard:** Monitor active, expiring, matured, renewed, and released instruments.
- **Secure Access Control:** Role-based permissions and traceable audit logs.

## 🔄 System Workflow

1. Institution uploads an FDR document.
2. Image preprocessing improves document readability.
3. AI/OCR extracts candidate FDR metadata.
4. Schema validation and business rules check the extracted fields.
5. Discrepancies and low-confidence results are sent for human review.
6. Authorized officials verify instrument details through approved sources.
7. Validated records and verification status are stored securely.
8. The maturity engine schedules alerts and escalations.
9. Renewal, replacement, and release requests follow controlled workflows.
10. Dashboards and reports provide administrative visibility.

## 🧠 AI Models & Algorithms

| Model / Algorithm | Functionality |
|---|---|
| NVIDIA Nemotron Document Parsing Model | Document layout extraction |
| Vision-Language Model (VLM) | Intelligent FDR data extraction |
| PaddleOCR / Tesseract OCR | Scanned text extraction |
| OpenCV | Document image preprocessing |
| Pydantic / JSON Schema | Structured data validation |
| Rule-Based Validation | Business rule enforcement |
| Isolation Forest (optional) | Anomaly detection |
| Levenshtein / Jaro-Winkler | Fuzzy record matching |
| Confidence Thresholding | Uncertainty-based review |
| Human-in-the-Loop (HITL) | Manual verification |
| Finite-State Machine (FSM) | FDR lifecycle management |
| Priority Queue Scheduling | Deadline-based prioritization |
| Retrieval-Augmented Generation (RAG) | Regulatory document retrieval |
| Vector Embeddings (optional) | Semantic document search |
| Cryptographic Hash Chaining | Tamper-evident audit logs |

**Note:** Confirm the exact NVIDIA model, its availability, licensing, and deployment requirements before implementation. AI-based extraction does not independently authenticate an FDR.

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL, pgvector (optional) |
| AI Document Processing | NVIDIA document model, PaddleOCR, OpenCV |
| Background Jobs | Celery, Redis |
| Authentication | OAuth 2.0 / OpenID Connect |
| Authorization | Role-Based Access Control (RBAC) |
| Security | TLS, encryption at rest, audit logging |
| Integrations | Authorized bank APIs, email/SMS gateways, AICTE APIs where available |

*Technology versions should be pinned and tested for compatibility before deployment. Components listed here represent the proposed stack unless already implemented.*

## 🏗️ Architecture

```text
Institution / Authorized Official
              |
       React Web Interface
              |
           FastAPI
              |
     Authentication + RBAC
              |
   AI Document Processing
    OCR / VLM / OpenCV
              |
   Schema & Rule Validation
              |
       Human Review Queue
              |
       PostgreSQL Database
          /           \
  Maturity Engine    Audit Trail
          |
    Celery + Redis
          |
 Notifications & Alerts
          |
   Dashboard & Reports
```

## 🔐 Security & Compliance

- Role-based access and least-privilege permissions.
- TLS-protected network communication.
- Encryption for stored documents and backups.
- Secure file upload and document access controls.
- Auditable submissions, reviews, and approval actions.
- Separation of institution-submitted and independently verified data.
- Authorized human approval for release and refund decisions.
- Protection of confidential financial and institutional information.

## 🧪 Testing Scenarios

1. Upload a valid FDR document.
2. Detect missing or unreadable document fields.
3. Identify mismatches between submitted and extracted values.
4. Trigger an alert for an approaching maturity date.
5. Record an FDR renewal or replacement.
6. Process a release request through authorized approvals.
7. Verify audit history and role-based access restrictions.
8. Test unauthorized access to another institution's records.

## 📊 Expected Impact

- Reduced manual tracking effort.
- Improved financial record consistency.
- Faster identification of incomplete submissions.
- Timely renewal and maturity reminders.
- Better visibility into pending verification and approvals.
- Improved accountability through audit trails.

These are intended outcomes and should be measured through prototype testing before making quantified performance claims.

## 🚀 Getting Started

This repository includes a browser-first demo plus small polyglot service examples.
The extra language files are intentionally narrow and runnable: they document how
the frontend can grow into a real service without pretending that production AI,
bank, or database integrations already exist.

Document the following as the application is developed:

1. Prerequisites and supported software versions.
2. Environment variables in a `.env.example` file.
3. Database setup and migrations.
4. Backend installation and startup.
5. Frontend installation and startup.
6. Test commands and demo data.
7. Deployment instructions.

### Polyglot project layout

| File | Language | Purpose |
|---|---|---|
| `index.html`, `styles.css`, `app.js` | HTML/CSS/JavaScript | Existing interactive portal |
| `api/server.js` | JavaScript (Node.js) | Static server and demo health/capability APIs |
| `types/domain.ts` | TypeScript | Shared domain and extraction contracts |
| `python/intelligence_worker.py` | Python | Dependency-free extraction, validation and audit-hash demo |
| `db/schema.sql` | SQL/PostgreSQL | Institutions, instruments and audit-event schema |
| `workers/deadline_worker.go` | Go | Priority-queue deadline worker example |
| `config/workflow.json` | JSON | Workflow transitions and document policy |

Run the browser and demo API with:

```powershell
npm start
```

Then open `http://127.0.0.1:5500`. The API endpoints are:

- `GET /api/health`
- `GET /api/intelligence/capabilities`

### Supabase configuration

The project is prepared for the supplied Supabase shared pooler PostgreSQL
instance. Copy
`.env.example` to `.env` in your local environment and set
`SUPABASE_DB_PASSWORD` outside source control. The password is URL-encoded by
`db/config.js` when a connection configuration is requested.

The Node server uses the `pg` client for a lightweight connection check.
`GET /api/health` reports the live `configured` and `connected` state without
returning credentials. Apply [db/schema.sql](./db/schema.sql) through a trusted
migration workflow before enabling application persistence.

Never put the real password in `.env.example`, frontend code, Git history, or
the public repository. If the password contains special characters, provide it
as the raw environment value; the helper handles URL encoding.

Run the Python demo without installing dependencies:

```powershell
python python/intelligence_worker.py
```

Run the Go deadline example if Go is installed:

```powershell
go run workers/deadline_worker.go
```

The TypeScript file is a contract source and requires a TypeScript toolchain
before it can be compiled. The SQL file targets PostgreSQL and should be applied
through a migration process in a real deployment.

Never commit API keys, passwords, production FDRs, or confidential institutional documents to GitHub.

## 🗺️ Project Roadmap

- [ ] Institution registration and authentication.
- [ ] FDR metadata management.
- [ ] Secure document upload and retrieval.
- [ ] AI-assisted metadata extraction.
- [ ] Validation and discrepancy review.
- [ ] Maturity alerts and escalation.
- [ ] Renewal and replacement history.
- [ ] Release and refund workflow.
- [ ] Dashboard and administrative reports.
- [ ] Audit and access-control testing.
- [ ] Approved external-system integrations.

## 👥 Team

**Team Zorax**

**Problem Statement ID:** 26265  
**Title:** Streamline of Security Deposit / FDR Portal

## ⚖️ Disclaimer

This platform is intended to support administrative tracking and review. It does not replace official bank verification, applicable AICTE regulations, or approval by the competent authority. Financial instrument verification and release decisions must follow authorized procedures.

---

⭐ If you find this project useful, consider starring the repository and sharing feedback.
