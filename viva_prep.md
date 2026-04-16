# 🎓 Viva Prep Guide — Shiksha DC (Zenith1009)

> Your role: **Auth Service (JWT + Redis)** + **Service Worker / PWA Offline Caching**

---

## 🗺️ Part 1: The Big Picture — Know the Project Cold

### What is Shiksha DC?
A **distributed, microservices-based smart classroom platform**. A teacher uploads slides; the system syncs them in real-time to display screens across multiple rooms — even when the network is flaky.

### How to explain it in 30 seconds (elevator pitch):
> "Shiksha DC is a distributed classroom system. Teachers can upload presentations and control what's shown on display screens across multiple rooms in real time. It uses microservices, WebSockets for live sync, and Kafka for event streaming. My job was to build the authentication backbone and ensure the frontend displays keep working even when the network drops."

### Architecture at a Glance
```
[Teacher Browser]
      |
   [NGINX Gateway] ← reverse proxy, load balancer
      |
  ┌───┴──────────────────────────────────┐
  │                                      │
[Auth Service]  [Content Service]  [Classroom Service]
  JWT + Redis    FastAPI + MinIO    WebSocket + Device Reg
      │
  [CockroachDB]   [Redis]   [Kafka]
```

---

## 🔐 Part 2: Your Contribution 1 — JWT + Redis Auth Service

### What you built
The full authentication system for the platform — `/signup`, `/login`, `/me` endpoints.

---

### 📖 Concept: What is JWT?

**JWT = JSON Web Token** — a compact, self-contained token for securely transmitting information.

**Structure:** `header.payload.signature`
- **Header**: algorithm used (e.g., HS256)
- **Payload**: claims — user ID, email, expiry time (`exp`)
- **Signature**: `HMAC(base64(header) + "." + base64(payload), SECRET_KEY)`

**How it works:**
1. User logs in → server creates a JWT signed with a secret key
2. Server sends JWT to the client
3. Client sends JWT in every subsequent request (usually in `Authorization: Bearer <token>` header)
4. Server verifies the signature — if valid, trusts the claims inside

**Why JWT?**
- **Stateless** — server doesn't need to store tokens (payload is self-contained)
- **Scalable** — any service can verify the token without a central session store
- **Secure** — tamper-proof due to cryptographic signature

---

### 📖 Concept: What is Redis?

**Redis = Remote Dictionary Server** — an in-memory key-value store used for caching, sessions, pub/sub.

**Key properties:**
- Blazing fast (sub-millisecond) because data lives in RAM
- Supports TTL (Time-To-Live) — keys auto-expire
- Used for session management because it's fast and distributed

**Commands you used:**
```js
redis.set("session:" + userId, token, { EX: 3600 }) // store with 1hr expiry
redis.get("session:" + userId)                        // retrieve
```

---

### 🔗 How JWT + Redis Work Together in Your System

> **"Why use Redis if JWT is already stateless?"** — This is the classic viva question!

**Answer:** JWT alone can't be invalidated before expiry. If a teacher logs out, the JWT is still valid until it expires. Redis solves this:

1. On `/login` → issue JWT **AND** store it in Redis with a TTL
2. On `/me` → verify JWT signature **AND** check Redis that the session still exists
3. On logout → delete the key from Redis → session instantly invalid, even if the JWT hasn't expired yet

This gives you the best of both worlds: **JWT's statelessness + Redis's revocability**.

---

### 🛣️ Your 3 Endpoints — Know Them Like the Back of Your Hand

#### `/signup`
```
1. Receive { email, password }
2. Check CockroachDB — does this email already exist?
   → If yes: return 409 Conflict
3. Hash the password (bcrypt)
4. Insert new user into CockroachDB
5. Return 201 Created
```

#### `/login`
```
1. Receive { email, password }
2. Query CockroachDB for the user by email
   → If not found: return 401 Unauthorized
3. Compare password hash (bcrypt.compare)
   → If wrong: return 401 Unauthorized
4. Sign a JWT: jwt.sign({ userId, email }, SECRET, { expiresIn: '1h' })
5. Store session in Redis: redis.set("session:userId", token, { EX: 3600 })
6. Return { token }
```

#### `/me`
```
1. Extract token from Authorization header
2. Verify JWT: jwt.verify(token, SECRET)
   → If invalid/expired: return 401
3. Check Redis: redis.get("session:" + userId)
   → If session missing (logged out): return 401
4. Return user profile data
```

---

### 🔥 Viva Q&A — Auth Service

| Question | Answer |
|---|---|
| What is JWT? | A compact, self-contained token with a cryptographic signature used for stateless authentication |
| Why use Redis with JWT? | JWT can't be revoked; Redis gives us session invalidation (logout) capability |
| What does `jwt.sign()` take? | Payload (claims), secret key, options (expiry) |
| What does `jwt.verify()` do? | Checks the signature AND expiry of a token |
| Where is the token stored on the client? | Typically in `localStorage` or an HTTP-only cookie |
| What's a TTL in Redis? | Time-To-Live — the key automatically expires after this duration |
| What's CockroachDB? | A distributed SQL database (Postgres-compatible) that's fault-tolerant |
| How does `/me` prevent forged tokens? | The JWT signature is verified using the server's secret key |
| What if Redis goes down? | All `/me` checks would fail — this is a trade-off; for resilience, Redis should be replicated |
| Why not store passwords in plain text? | Passwords must be hashed (bcrypt) so that even if DB is breached, passwords aren't exposed |

---

## 🧱 Part 3: Your Contribution 2 — Service Worker / PWA Offline Cache

### What you built
Made the **frontend work offline** by registering a Service Worker that caches static assets.

---

### 📖 Concept: What is a Service Worker?

A **Service Worker** is a JavaScript file that runs in the **background**, separate from the main browser thread. It acts as a **proxy between the browser and the network**.

**What it can do:**
- Intercept network requests
- Serve cached responses when offline
- Push notifications
- Background sync

**Lifecycle:**
```
Register → Install → Activate → Fetch (intercepts requests)
```

**Your `sw.js` used the "Cache-First" strategy:**
```
Request comes in
  → Is it in the cache?
      Yes → Serve from cache (works offline!)
      No  → Fetch from network → cache it → return it
```

---

### 📖 Concept: What is a PWA?

**PWA = Progressive Web App** — a web app that behaves like a native app:
- Works offline (via service workers)
- Can be installed on home screen
- Fast and reliable even on bad networks

**Why this matters for Shiksha DC:**
> Classroom display screens are often on school WiFi which can be unreliable. If the network drops mid-class, the display should keep showing the current slide, not a blank screen. The service worker ensures this by caching the app shell.

---

### 🗂️ Files You Created

#### `frontend/public/sw.js`
```js
// On install — cache the app shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('shiksha-cache-v1').then(cache =>
      cache.addAll(['/', '/index.html', '/main.js', '/styles.css'])
    )
  );
});

// On fetch — serve from cache, fall back to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then(response =>
      response || fetch(event.request)
    )
  );
});
```

#### `frontend/app/ServiceWorkerRegister.js`
```js
'use client' // Next.js client component
useEffect(() => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
  }
}, []);
```
> Only registers if the browser supports service workers — graceful degradation.

#### `frontend/app/layout.js` (modified)
- Added `<ServiceWorkerRegister />` to the root layout so it's active across the **entire app**

---

### 🔥 Viva Q&A — Service Worker

| Question | Answer |
|---|---|
| What is a service worker? | A background JS script that intercepts network requests and can serve cached content |
| Why did you add a service worker? | To make classroom displays resilient to network drops — they cache the app shell and keep working offline |
| What is `cache.addAll()`? | Caches a list of URLs during the install phase (app shell caching) |
| What is `caches.match()`? | Checks if a request has a cached response |
| What is `event.respondWith()`? | Intercepts a fetch and responds with a custom response (e.g., from cache) |
| What's the difference between `install` and `activate` events? | `install` caches assets; `activate` is used to clean up old caches |
| Why use `'use client'` in Next.js? | Service workers need browser APIs (`navigator`), which don't exist during server-side rendering |
| What happens if service worker registration fails? | The app still works normally (no offline support) — the `if ('serviceWorker' in navigator)` check is a safe guard |
| What is a PWA? | A web app with native-like features (offline, installable) via service workers + web manifests |
| Can service workers intercept POST requests? | Yes, but typically only GET requests are cached; POST (form submissions) usually go to network |

---

## 🏛️ Part 4: Know the Full Stack (For Context Questions)

Examiners may ask about technologies you *didn't* build. Here's a quick cheat sheet:

| Technology | What It Does | Why Used Here |
|---|---|---|
| **Next.js 14** | React framework with SSR/SSG | Teacher UI — fast, SEO-friendly |
| **WebSockets** | Persistent bidirectional connection | Real-time slide sync to displays |
| **Kafka** | Distributed event streaming | Teaching logs, analytics events |
| **MinIO** | S3-compatible object storage | Stores uploaded PPT/PDF files |
| **CockroachDB** | Distributed SQL (Postgres-compat) | Fault-tolerant user/class data |
| **NGINX** | Reverse proxy + load balancer | Single entry point, routes to services |
| **Prometheus** | Metrics collection | Monitors service health |
| **Grafana** | Metrics visualization | Dashboard for the ops team |
| **Docker Compose** | Container orchestration | Runs all services together |

---

## 🎤 Part 5: How to Present in the Viva

### Opening Statement (say this first, confidently)
> "I worked on two core parts of Shiksha DC. First, I built the authentication service — a Node.js/Express service that handles user signup, login, and session validation using JWT tokens and Redis for session management. Second, I added offline caching capability to the frontend using a Service Worker, which is crucial for classroom displays that need to keep working even when the network is unreliable."

### Framework: Explain Your Work Using STAR
- **S**ituation: "The project needed a real auth system — the stub wasn't production-grade"
- **T**ask: "I needed to implement secure login with session management"
- **A**ction: "I used JWT for tokens and Redis to store and revoke sessions"
- **R**esult: "The entire platform now has a working, revocable auth backbone"

### Handling Tough Questions
- **"I'm not sure, but here's my reasoning..."** — never bluff, show thought process
- **"I implemented X, which handles Y. The reason I chose this approach was..."** — always explain WHY
- **Draw a diagram** — if asked how JWT + Redis works, sketch the flow on paper

---

## ⚡ Quick-Fire Facts to Memorize

| Fact | Value |
|---|---|
| Your commits | 4 |
| Auth service language | Node.js (Express) |
| JWT library | `jsonwebtoken` |
| Redis client | `redis` (Node.js) |
| Token expiry | 1 hour (`{ expiresIn: '1h' }`) |
| Service worker file | `frontend/public/sw.js` |
| Registration component | `ServiceWorkerRegister.js` |
| Cache strategy used | Cache-First (serve from cache, fallback to network) |
| Why Redis + JWT? | JWT can't be revoked; Redis enables logout/invalidation |
| Team size | 6 contributors |
| Your rank by commits | 5th (but auth and cache are critical path features) |

---

## 🚨 Potential Trick Questions

1. **"JWT is stateless, but you used Redis — isn't that a contradiction?"**
   → No — JWT handles *verification*, Redis handles *revocation*. They solve different problems.

2. **"What if someone steals the JWT token?"**
   → Set short expiry (`1h`), use HTTPS, store in HTTP-only cookies (not localStorage). The Redis session check adds another layer.

3. **"Why not just use only Redis sessions without JWT?"**
   → JWT is stateless and can be verified by any microservice without hitting Redis. Reduces bottleneck.

4. **"Service workers only work on HTTPS — how does that work in development?"**
   → `localhost` is an exception — browsers allow service workers on localhost for development.

5. **"What's the difference between a service worker and a web worker?"**
   → Both run off the main thread, but service workers intercept network requests and have a lifecycle (install/activate/fetch). Web workers are just for computation.

---

> **Pro Tip**: You only had 4 commits, but they were *high-impact*. Emphasize that you owned **critical path features** — auth is the gatekeeper for the entire platform, and the service worker is what makes displays reliable in real classrooms. Quality > quantity.
