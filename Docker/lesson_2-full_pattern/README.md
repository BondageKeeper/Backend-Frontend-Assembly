# Lesson 2: Multi-Container Orchestration & Live Database Inspections

## Key Skills Acquired

* **Docker Compose Engineering:** Mastered bundling an asynchronous FastAPI web service and an isolated PostgreSQL 15 database instance into a unified, single-network ecosystem.
* **Network Topology Demystification:** Understood why containerized servers require binding to `--host 0.0.0.0` to receive external computer loops, while utilizing internal DNS link aliases (`db_postgres:5432`) for secure cross-container communication.
* **Port Conflict Resolution:** Solved system-wide port deadlock bugs (default `5432` collision) by manually separating local development environments and routing database tunnels through clean alternative lines (`5433:5432`).
* **Live Database Inspection:** Connected native administration tools (pgAdmin 4) into active virtual containers to inspect live automated SQLAlchemy tables and data inserts in real-time.

## 🛠️ Essential Docker Commands Reference

### 1. The Power Starters (Run & Build)
* `docker compose up` — Wakes up all sleeping containers and launches the network stack instantly using cached recipes.
* `docker compose up --build` — Forces Docker to erase outdated components, re-read the Dockerfile instructions, install dependencies, and spin up clean microservices.

### 2. The Clean Up Crew (Stop & Erase)
* `Ctrl + C` — The universal terminal trigger to immediately halt execution logs and freeze current processes.
* `docker compose down` — Gracefully stops all active containers and destroys virtual network bridges to completely free up system resources.
 
