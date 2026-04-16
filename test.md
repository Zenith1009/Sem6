# Shiksha DC — Repository Overview & Contributor Summary

## 🎓 What the Project Aims to Achieve

**Shiksha DC** (DC = Distributed Classroom) is a **distributed, microservices-based platform** for teachers to present, synchronize, and manage classroom content across dedicated display screens. Think of it as a "command deck" for a smart classroom: a teacher uploads slides, the system syncs them in real-time to displays across multiple rooms, tracks progress, and remains resilient even if parts of the infrastructure go down.

**Core goals:**
- Real-time slide synchronization across classroom displays via WebSockets
- "Ghost Classroom" — broadcast slides to multiple rooms simultaneously
- Fault-tolerant, production-grade distributed infrastructure
- Teacher analytics and progress tracking
- A clean, professional teacher-first UI

---

## 🏗️ Codebase Structure & Key Technologies

```code
shiksha_dc/
├── frontend/            # Next.js 14 teacher UI
├── gateway/             # Node.js reverse proxy / API gateway
├── microservices/
│   ├── auth-service/    # Node.js — JWT auth + Redis sessions
│   ├── content-service/ # Python/FastAPI — PPT/PDF upload + MinIO storage
│   ├── classroom-service/ # Node.js — WebSocket gateway + device registry
│   ├── progress-service/  # Node.js — Kafka consumer + teaching logs
│   ├── analytics-service/ # Python — Kafka aggregation + analytics API
│   └── sync-service/    # Node.js — slide broadcast WebSocket server
├── infra/
│   ├── nginx/           # Reverse proxy config
│   ├── grafana/         # Dashboards
│   └── prometheus/      # Metrics & alerts
├── docs/                # Architecture docs and booklets
├── docker-compose.dev.yml
└── docker-compose.prod.yml
```


### Key Technologies

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 14, Tailwind CSS, shadcn UI |
| **Auth** | JWT + Redis sessions |
| **Backend services** | Node.js (Express), Python (FastAPI) |
| **Realtime sync** | WebSockets (ws library) |
| **Object storage** | MinIO (4-node cluster, erasure coding EC:2) |
| **Database** | CockroachDB (3-node distributed SQL) |
| **Event streaming** | Apache Kafka + Zookeeper |
| **Caching** | Redis (master + replica) |
| **Reverse proxy / LB** | NGINX |
| **Observability** | Prometheus + Grafana |
| **Containerization** | Docker Compose (dev + prod) |

---

## 👤 Zenith1009 — Contributions (4 commits)

### 1. `feat(auth): jwt + redis sessions` — April 6, 2026
**Files changed:** `microservices/auth-service/index.js`, `microservices/auth-service/package.json`
**Impact: +34 / -7 lines**

Upgraded the auth service from a stub to a real, production-grade implementation:
- Integrated **Redis** for session management (`createClient`, `redis.set`/`redis.get`)
- Implemented **JWT signing and verification** with `jsonwebtoken`
- Added `/signup`, `/login`, and `/me` endpoints with real logic:
  - `/signup` — checks for existing users, inserts into CockroachDB
  - `/login` — validates credentials, creates a Redis session, issues a JWT token
  - `/me` — verifies the JWT and validates the session is still alive in Redis
- Added `jsonwebtoken` and `redis` to `package.json` dependencies

This is the **authentication backbone the entire platform relies on**.

---

### 2. `feat(cache): add service worker registration` — April 5, 2026
**Files added:** `frontend/app/ServiceWorkerRegister.js`, `frontend/public/sw.js`
**Files modified:** `frontend/app/layout.js`
**Impact: +36 / -1 lines**

Added **offline/PWA caching capability** to the frontend:
- Created `ServiceWorkerRegister.js` — a React client component that registers `/sw.js` on page load
- Created `sw.js` — a service worker that caches static assets so the app works even when the network drops
- Wired it into the root `layout.js` so it's active across the entire app

Critical for classroom displays — if the network briefly drops, the display keeps working.

---

### 3. `feat(ui): clarify display card` — April 5, 2026
**File changed:** `frontend/app/page.js`
**Impact: +1 / -1 line**

A small UI polish — updated the landing page's "Live Classroom Display" status card to display `"Active · Display"`, making the live status clearer to users at a glance.

---

### 4. `merge: caching` — April 5, 2026

Merge commit that brought the caching work (commits 2 & 3) into the main branch.

---

## 📊 Full Team Contribution Summary

| Contributor | Commits | Focus Area |
|---|---|---|
| **Sinaker** | 37 | Infra, prod stack, hardening, NGINX, Docker, docs, DB persistence |
| **Shamelesscodes** | 13 | Kafka, progress service, analytics UI, sync/ghost classroom |
| **sujeetrajak22** | 8 | Frontend sync flows, IndexedDB edge cache, UI annotations |
| **Akp2211** | 7 | WebSocket classroom service, JWT auth merges, UI CTA |
| **Zenith1009** | 4 | **Auth service (JWT + Redis)**, service worker/offline cache, UI polish |
| **amanraz2802** | 3 | Analytics page UI, slide frame, hero CTA |

---

## 🔑 Key Takeaway

Zenith1009's contributions were focused but impactful:
1. **Built the real authentication system** (JWT + Redis sessions) that the entire platform depends on
2. **Added offline resilience** to the frontend via a service worker — especially important for classroom displays that must keep working with intermittent connectivity
3. **Polished the landing page UI** for clarity



---
---
---

👤 Your Contributions — Zenith1009 (4 commits)

You made 4 commits across two distinct areas:
1. feat(auth): jwt + redis sessions — April 6, 2026

Files changed: microservices/auth-service/index.js, microservices/auth-service/package.json Impact: 34 additions, 7 deletions

This was a substantial upgrade to the auth service — you replaced what was likely a stub/simple auth with a real, production-grade implementation:

    Integrated Redis for session management (createClient, redis.set/redis.get)
    Implemented JWT signing and verification with jsonwebtoken
    Added the /signup, /login, and /me endpoints with real logic:
        /signup — checks for existing users, inserts into CockroachDB
        /login — validates credentials, creates a Redis session, issues a JWT token
        /me — verifies the JWT and validates the session is still alive in Redis
    Added jsonwebtoken and redis to package.json dependencies

This is the authentication backbone the entire platform relies on.
2. feat(cache): add service worker registration — April 5, 2026

Files added: frontend/app/ServiceWorkerRegister.js, frontend/public/sw.js Files modified: frontend/app/layout.js Impact: 36 additions, 1 deletion

You added offline/PWA caching capability to the frontend:

    Created ServiceWorkerRegister.js — a React client component that registers /sw.js on page load
    Created sw.js — a service worker that caches static assets (shell caching strategy) so the app works even when the network drops
    Wired it into the root layout.js so it's active across the entire app

This is critical for classroom displays — if the network briefly drops, the display keeps working.
3. feat(ui): clarify display card — April 5, 2026

File changed: frontend/app/page.js Impact: 1 addition, 1 deletion

A small but meaningful UI polish — you updated the landing page's "Live Classroom Display" status card to make the display status text clearer (changed to "Active · Display", indicating the card is a live classroom display panel, not just a status indicator).
4. merge: caching — April 5, 2026

This was the merge commit that brought your caching work (commits 2 & 3) into the main branch.
📊 Contribution Summary by Team Member
Contributor	Commits	Focus Area
Sinaker	37	Infra, prod stack, hardening, NGINX, Docker, docs, DB persistence
Shamelesscodes	13	Kafka, progress service, analytics UI, sync/ghost classroom
sujeetrajak22	8	Frontend sync flows, IndexedDB edge cache, UI annotations
Akp2211	7	WebSocket classroom service, JWT auth merges, UI CTA
Zenith1009 (you)	4	Auth service (JWT + Redis), service worker / offline cache, UI polish
amanraz2802	3	Analytics page UI, slide frame, hero CTA

In summary: Your contributions were focused but impactful — you built the real authentication system (JWT + Redis sessions) that the entire platform depends on, and added offline resilience to the frontend via a service worker, which is especially important for classroom displays that must keep working even with intermittent connectivity.