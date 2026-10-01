# 🛡️ PhishShield — Real-Time ML Phishing Detection Engine

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Hardware](https://img.shields.io/badge/Optimized%20For-Apple%20Silicon%20M1-black?style=for-the-badge&logo=apple&logoColor=white)](https://apple.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> An end-to-end cybersecurity solution that detects phishing, credential harvesters, and malicious domain masking in sub-milliseconds without resolving or rendering dangerous web content.

---

## ⚡ Highlights

- **Static Lexical Extraction:** Analyzes URLs directly via structural heuristics—eliminates zero-day payload execution risks.
- **Ensemble ML Classification:** Random Forest classifier parallelized across all CPU cores.
- **REST API with CORS:** Built using FastAPI, complete with auto-generated Swagger UI and non-blocking cross-origin communication.
- **Dual Client Access:** Includes a standalone visual dashboard (`index.html`) and an active browser companion (Manifest V3 Chrome Extension).

---

## 🏗️ Architecture Pipeline

```text
[ Inbound Target URL ]
          │
          ▼
 [ Lexical Feature Extractor ]
    ├── Shannon Character Entropy Calculation
    ├── Hostname Delimiter & Subdomain Tree Parsing
    ├── Direct IPv4 / IPv6 Pattern Validation
    └── Suspicious Delimiter Checks (@, //, -, _)
          │
          ▼
 [ Random Forest Classification (100 Trees) ]
          │
          ▼
 ┌─────────────────┬───────────────────┬──────────────────┐
 │   Safe (<40%)   │ Suspicious (40-75%)│ Phishing (>=75%) │
 └─────────────────┴───────────────────┴──────────────────┘

[spreadsheet.pdf](https://github.com/user-attachments/files/32924051/spreadsheet.pdf)

