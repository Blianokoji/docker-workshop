# 🐳 Zero to Docker: Complete Hands-On Workshop

[![Docker](https://img.shields.io/badge/Docker-27.x-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Compose](https://img.shields.io/badge/Docker_Compose-v2-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Platforms](https://img.shields.io/badge/Platforms-Windows%20%7C%20Linux%20%7C%20macOS-blue)](CHEATSHEET.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A battle-tested, 90-minute interactive Docker workshop designed for mixed skill levels. Every module provides hands-on exercises, pre-built Docker Hub images, and side-by-side terminal commands for **Windows (PowerShell)** and **Linux / macOS (Bash)**.

---

## 🗺️ Workshop Curriculum

| Module | Topic | Core Focus | Link |
|:---|:---|:---|:---|
| **01** | **What Even Is a Container?** | Process isolation, namespaces, cgroups, ephemeral filesystem | [Start Module 1 ➔](01-explore/README.md) |
| **02** | **Images, Layers & Debugging** | Diagnosing build failures, layer caching, multi-stage best practices | [Start Module 2 ➔](02-fix-the-dockerfile/README.md) |
| **03** | **Volumes & Data Persistence** | Ephemeral storage vs Docker Named Volumes vs Host Bind Mounts | [Start Module 3 ➔](03-volumes/README.md) |
| **04** | **Networks & Service Discovery** | Bridge networks, embedded DNS resolution, port security | [Start Module 4 ➔](04-networking/README.md) |
| **05** | **Docker Compose in Action** | Multi-tier voting app (API + Redis + Dashboard), service scaling | [Start Module 5 ➔](05-compose-voting-app/README.md) |
| **06** | **Cool Tricks & CLI Mastery** | Resource monitoring, `docker cp`, `docker exec`, emergency cleanup | [Start Module 6 ➔](06-cool-tricks/README.md) |

---

## 🛠️ Participant Prerequisites

Before the session starts, ensure you have:
1. **Docker Desktop** installed and running:
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - *Windows Users:* Ensure the **WSL 2 backend** is checked in Docker Desktop Settings.
2. **Git** installed on your laptop:
   - Clone this repository to your machine:
     ```bash
     git clone https://github.com/Blianokoji/docker-workshop.git
     cd docker-workshop
     ```
3. **A Terminal**:
   - **Windows:** PowerShell 7 or Windows Terminal (PowerShell).
   - **Linux / macOS:** Any standard Bash or Zsh terminal.

> 💡 **No Docker on your machine?** Use the browser-based sandbox: [Play with Docker](https://labs.play-with-docker.com/).

---

## 📦 Pre-Built Docker Hub Images (`dracalar/*`)

All images are pre-compiled, based on ultra-lightweight Alpine Linux (<50MB each), and hosted on Docker Hub under the `dracalar` namespace:

```bash
docker pull dracalar/docker-workshop-explore
docker pull dracalar/docker-workshop-broken
docker pull dracalar/docker-workshop-notebook
docker pull dracalar/docker-workshop-api
docker pull dracalar/docker-workshop-frontend
docker pull dracalar/docker-workshop-vote-api
docker pull dracalar/docker-workshop-vote-dashboard
```

---

## 🏗️ Architecture: The Module 5 Compose Voting App

```text
               ┌────────────────────────────────────────────────────────┐
               │              Docker Network (workshop-net)             │
               │                                                        │
[ Browser ] ───┼──► :3000 ──► [ vote-api (Python) ] ──► [ redis:6379 ]  │
               │                        │                      ▲        │
[ Browser ] ───┼──► :3001 ──► [ dashboard (Nginx) ] ───────────┘        │
               │               (Live Polling Engine)                    │
               └────────────────────────────────────────────────────────┘
```

---

## 📚 Essential Workshop References

- 📖 **[Master Cheatsheet](CHEATSHEET.md)**: Side-by-side Windows PowerShell vs Linux Bash command reference.
- 🎓 **[Instructor Guide](INSTRUCTOR_GUIDE.md)**: 90-minute session delivery script, speaker notes, live demo commands, and troubleshooting.

---

## 🚀 Instructor Image Building & Publishing

To build all 7 images and push them to Docker Hub under `dracalar`:

#### 🪟 Windows (PowerShell)
```powershell
.\build-and-push.ps1 -Username dracalar
```

#### 🐧 Linux / macOS (Bash)
```bash
chmod +x build-and-push.sh
./build-and-push.sh dracalar
```
*(Add `-NoPush` or `--no-push` to test local image building without publishing).*