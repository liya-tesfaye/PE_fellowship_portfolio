# Portfolio Service — Containerized, Reverse-Proxied, TLS-Terminated

A personal portfolio site built with Flask, deployed as a multi-container production service on a self-managed Linux VPS — built during the MLH × Meta Production Engineering Fellowship.

This isn't just a portfolio site — it's the infrastructure around it: containerization, orchestration, reverse proxying, TLS automation, and deployment automation, all built and operated end-to-end.

## Architecture

```
                    Internet
                       │
                  ┌─────────┐
                  │  Nginx  │  ← TLS termination (Let's Encrypt / certbot)
                  │ (proxy) │  ← per-IP rate limiting on API routes
                  └────┬────┘
                       │ HTTP (internal)
                  ┌────┴─────┐
                  │  Flask   │  ← REST API (GET/POST timeline)
                  │  (app)   │
                  └────┬─────┘
                       │
                  ┌────┴─────┐
                  │ MariaDB  │  ← persisted via named Docker volume
                  │  (db)    │
                  └──────────┘
```

All three services run as independently managed Docker containers, orchestrated with Docker Compose.

## Features

- **Multi-container orchestration** via Docker Compose — Flask app, MariaDB, and Nginx reverse proxy each run as separate, independently manageable containers
- **Nginx reverse proxy** with automated **Let's Encrypt TLS certificate generation** (via `jonasal/nginx-certbot`) for HTTPS termination
- **Per-IP rate limiting** on the `POST /api/timeline_post` endpoint to prevent abuse
- **Persistent storage** via named Docker volumes — database state and TLS certs survive container rebuilds and reboots
- **Separate dev/prod Compose configurations** (`docker-compose.yml` for local development with hot-reload volume mounts, `docker-compose.prod.yml` for the VPS)
- **Automated deployment** via a `redeploy-site.sh` script: pulls latest `main`, tears down containers, rebuilds images, and brings the stack back up
- **CI/CD pipeline** for automated testing on changes
- **Unit tests** covering core API functionality

## Tech Stack

- **App**: Flask (Python), REST API (GET/POST)
- **Database**: MariaDB (MySQL-compatible, lower resource footprint)
- **Reverse Proxy / TLS**: Nginx, Let's Encrypt (certbot)
- **Orchestration**: Docker, Docker Compose
- **Infra**: DigitalOcean Linux VPS, systemd
- **Automation**: Bash, SSH, CI/CD

## Local Development

```bash
docker compose up -d --build
```

Visit `http://localhost:5000` to view the site and test the timeline API.

```bash
curl http://localhost:5000/api/timeline_post
curl -X POST http://localhost:5000/api/timeline_post -d 'name=Liya&message=hello'
```

## Production Deployment

On the VPS:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Redeploys (after pushing changes to `main`) are handled by:

```bash
~/redeploy-site.sh
```

which runs:
1. `git fetch && git reset origin/main --hard`
2. `docker compose -f docker-compose.prod.yml down`
3. `docker compose -f docker-compose.prod.yml up -d --build`

## Rate Limiting

The `POST /api/timeline_post` endpoint is rate-limited at the Nginx layer (1 request/minute per IP) to prevent abuse, configured in `user_conf.d/myportfolio.conf`.

## Author

**Liya Tesfaye** — built during the Major League Hacking × Meta Production Engineering Fellowship
