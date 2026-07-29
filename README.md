# PortSwigger Web Security Academy — Lab Writeups

Personal writeups from completing labs on [PortSwigger's Web Security Academy](https://portswigger.net/web-security), documenting the vulnerability, exploitation approach, and remediation for each solved lab.

Each writeup follows a consistent format defined in [`TEMPLATE.md`](./TEMPLATE.md): **Description → Where It Lived → Objective → Payload → How It Works → Impact → Remediation.**

---

## 📊 Progress Tracker

> Auto-updated by `.github/workflows/update-progress.yml` on every push to `main` — just add a writeup file to a category folder and commit. Edit `scripts/totals.json` to adjust total lab counts per category.

<!-- PROGRESS-TABLE-START -->
| Category | Solved | Total | Progress |
|---|---|---|---|
| XSS | **2** | 30 | █░░░░░░░░░ |
| SQL Injection | **4** | 18 | ██░░░░░░░░ |
| Authentication | 0 | 14 | ░░░░░░░░░░ |
| Path Traversal | 0 | 6 | ░░░░░░░░░░ |
| Access Control | 0 | 13 | ░░░░░░░░░░ |
| CSRF | 0 | 12 | ░░░░░░░░░░ |
| CORS | 0 | 3 | ░░░░░░░░░░ |
| Clickjacking | 0 | 5 | ░░░░░░░░░░ |
| Cross-Site WebSocket Hijacking | 0 | 3 | ░░░░░░░░░░ |
| SSRF | 0 | 7 | ░░░░░░░░░░ |
| XXE Injection | 0 | 9 | ░░░░░░░░░░ |
| HTTP Request Smuggling | 0 | 22 | ░░░░░░░░░░ |
| SSTI | 0 | 7 | ░░░░░░░░░░ |
| Insecure Deserialization | 0 | 10 | ░░░░░░░░░░ |
| Information Disclosure | 0 | 5 | ░░░░░░░░░░ |
| Business Logic Vulnerabilities | 0 | 12 | ░░░░░░░░░░ |
| HTTP Host Header Attacks | 0 | 7 | ░░░░░░░░░░ |
| OAuth | 0 | 6 | ░░░░░░░░░░ |
| File Upload Vulnerabilities | 0 | 7 | ░░░░░░░░░░ |
| JWT | 0 | 8 | ░░░░░░░░░░ |
| Prototype Pollution | 0 | 10 | ░░░░░░░░░░ |
| GraphQL API Vulnerabilities | 0 | 5 | ░░░░░░░░░░ |
| Race Conditions | 0 | 6 | ░░░░░░░░░░ |
| NoSQL Injection | 0 | 4 | ░░░░░░░░░░ |
| API Testing | 0 | 5 | ░░░░░░░░░░ |
| Web LLM Attacks | 0 | 8 | ░░░░░░░░░░ |
| Web Cache Deception | 0 | 5 | ░░░░░░░░░░ |
| Web Cache Poisoning | 0 | 13 | ░░░░░░░░░░ |
| Essential Skills | 0 | 2 | ░░░░░░░░░░ |

**Total labs solved: 6**
<!-- PROGRESS-TABLE-END -->

---

## 📁 Repo Structure

```
PortSwigger-Labs/
├── README.md                    ← this file (master index + tracker)
├── TEMPLATE.md                  ← blank writeup template
│
├── xss/
│   ├── README.md
│   └── xss-stealing-cookies.md
│
├── sqli/                        ← add as solved
├── authentication/
├── path-traversal/
├── access-control/
├── csrf/
├── cors/
├── clickjacking/
├── websocket-hijacking/
├── ssrf/
├── xxe/
├── request-smuggling/
├── ssti/
├── insecure-deserialization/
├── information-disclosure/
├── business-logic/
├── host-header-attacks/
├── oauth/
├── file-upload/
├── jwt/
├── prototype-pollution/
├── graphql/
├── race-conditions/
├── nosql-injection/
├── api-testing/
├── web-llm-attacks/
├── web-cache-deception/
├── web-cache-poisoning/
├── essential-skills/
│
└── assets/
    └── screenshots/              ← optional proof-of-exploit images per lab
```

**Convention:** lowercase, hyphen-separated folder and file names (`xss/xss-stealing-cookies.md`, not `Cross-site-scripting-XSS/...`). Create a category folder only when you have your first writeup for it — don't pre-create all of these empty at once, or the repo will look padded. Add folders as you go.

---

## 🎯 Purpose

Tracks hands-on progress through the Web Security Academy as part of ongoing offensive security practice, alongside HTB/THM work in [HackMyVM](https://github.com/om-root/HackMyVM).
