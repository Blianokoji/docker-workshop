# 🎓 Docker Workshop Instructor Guide

**Title:** Zero to Docker: Hands-On Container Mastery  
**Target Duration:** ~90 minutes (with 10-15 min Q&A buffer)  
**Target Audience:** Mixed (beginners to intermediate developers)  
**Primary Platforms:** Windows (PowerShell) and Linux/macOS (Bash)  
**Docker Hub Namespace:** `dracalar`  
**GitHub Repository:** `https://github.com/Blianokoji/docker-workshop`  

---

## 📋 Pre-Session Checklist (24 Hours Before)

1. [ ] **Build & Push Workshop Images to Docker Hub**:
   Run the build script to ensure all 7 images are published:
   ```powershell
   .\build-and-push.ps1 -Username dracalar
   ```
2. [ ] **Verify Public Pulling**:
   Test pulling on a separate machine or clean terminal:
   ```bash
   docker pull dracalar/docker-workshop-explore
   ```
3. [ ] **Participant Prerequisites**:
   Send an email or message reminding attendees to install:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ensure WSL 2 backend is enabled on Windows).
   - [Git](https://git-scm.com/).
   - Clone the repo:
     ```bash
     git clone https://github.com/Blianokoji/docker-workshop.git
     ```
4. [ ] **Emergency Fallback (For broken laptops)**:
   If an attendee cannot run Docker Desktop due to corporate permissions or hardware limitations, direct them to:
   👉 **[Play with Docker](https://labs.play-with-docker.com/)** (Free 4-hour browser-based Linux Docker terminal, requires Docker Hub login).

---

## ⏱️ Session Timeline (90 Minutes)

```
00:00 - 00:10 │ 10 min │ Intro: Mental Model (Containers vs Virtual Machines)
00:10 - 00:25 │ 15 min │ Module 1: Process Isolation & Ephemeral Filesystem
00:25 - 00:45 │ 20 min │ Module 2: Images, Layers & Fixing the Broken Dockerfile
00:45 - 01:00 │ 15 min │ Module 3: Persistent Storage with Volumes & Bind Mounts
01:00 - 01:15 │ 15 min │ Module 4: Networks, Service Discovery & Port Isolation
01:15 - 01:30 │ 15 min │ Module 5: Docker Compose Voting App Architecture
01:30 - 01:35 │  5 min │ Module 6: Rapid-Fire Superpowers & Cleanup
01:35 - 01:45 │ 10 min │ Q&A & Wrap-Up
```

---

## 🎤 Module-by-Module Delivery Script

### 1. Opening & The Mental Model (10 min)
- **Opening Hook**: *"How many times have you heard: 'Well, it worked on my machine!'? Docker eliminates that forever by shipping the application together with its entire environment."*
- **Key Visual**: Draw a quick diagram comparing:
  - **VM**: Hardware -> Host OS -> Hypervisor -> Guest OS (Heavy, 2-10GB) -> App.
  - **Container**: Hardware -> Host OS (Linux Kernel) -> Docker Engine -> Isolated App Process (<50MB).
- **Golden Rule**: Containers are just isolated Linux processes running natively on the kernel using **namespaces** and **cgroups**.

---

### 2. Module 1: The Interactive Sandbox (15 min)
- **Goal**: Everyone gets their first instant win within 2 minutes.
- **Projector Demo**:
  ```bash
  docker run -it --rm dracalar/docker-workshop-explore
  ```
- **Key Talking Points**:
  - Point out the prompt: notice the Alpine Linux environment.
  - Run `hostname` and `ps aux`: highlight that the container only sees its own processes.
  - Run the **Ephemeral Test**: create `/secret.txt`, exit, run again, show it's gone!
  - *Instructor tip:* Emphasize that images are immutable read-only templates.

---

### 3. Module 2: Fixing the Broken Dockerfile (20 min)
- **Goal**: Teach Dockerfiles through active debugging rather than dry lecture slides.
- **Story**: *"A junior developer wrote this Dockerfile and left for lunch. It won't build. Let's fix it."*
- **Live Steps**:
  1. Have everyone run: `docker build -t my-broken-app .` inside `02-fix-the-dockerfile`.
  2. Ask the audience: *"Who can tell me why npm failed?"*
  3. Walk through the 4 bugs:
     - Missing `WORKDIR /app`
     - Order of `RUN npm install` vs `COPY package.json .`
     - Exposing port 8080 vs app listening on 3000
     - Non-exec `CMD` syntax
  4. Build the fixed version, then edit `server.js` to demonstrate **Layer Caching**!

---

### 4. Module 3: Persistent Storage & Volumes (15 min)
- **Goal**: Solve the ephemeral storage dilemma.
- **Story**: *"If containers lose all data on exit, how do we run databases like PostgreSQL or MongoDB?"*
- **Live Steps**:
  1. Start `dracalar/docker-workshop-notebook` without a volume.
  2. Add notes at `http://localhost:5000`. Kill the container (`docker rm -f`).
  3. Show the data is gone on restart.
  4. Now add `-v my-notes-volume:/app/data`. Repeat the test.
  5. **Boom!** The notes survived! Show that the container ID changed, but data remained intact.
  6. Demo host bind mounts with `-v ${PWD}/my-local-notes:/app/data` (Windows) and show the file appearing right on your host desktop.

---

### 5. Module 4: Container Networking & Service Discovery (15 min)
- **Goal**: Connect microservices without hardcoding IPs.
- **Story**: *"In Kubernetes or cloud environments, container IPs are dynamically assigned. How do microservices talk?"*
- **Live Steps**:
  1. Run `frontend` alone — open `http://localhost:8080` to show the red "Disconnected" banner.
  2. Create the custom bridge: `docker network create workshop-net`.
  3. Run `api` and `frontend` on `workshop-net`.
  4. Refresh the browser — show the green "Connected" banner and live quotes.
  5. **Crucial Security Lesson**: Point out that the `api` container does NOT have `-p 8000:8000`. It is completely private and shielded from external attacks.

---

### 6. Module 5: Docker Compose Voting App (15 min)
- **Goal**: Connect all concepts into a real 3-tier production architecture.
- **Live Steps**:
  1. Show `docker-compose.yml`. Explain services, dependencies, and volumes.
  2. Run `docker compose up -d`.
  3. Open `http://localhost:3000` (Voting UI) and `http://localhost:3001` (Dashboard) side-by-side.
  4. Ask attendees to vote. Show the live bars adjusting in real time.
  5. Show `docker compose logs -f vote-api`.
  6. Show `docker compose up -d --scale vote-api=3`.
  7. Show `docker compose down -v`.

---

### 7. Module 6: Rapid-Fire Superpowers (5 min)
- Show `docker stats` (interactive live resource dashboard).
- Show `docker system df` and `docker system prune -a --volumes`.
- Show running one-line Python or Node scripts with `docker run --rm`.

---

## 🚨 Troubleshooting Common Attendee Issues

| Problem | Cause | Solution |
|:---|:---|:---|
| `Cannot connect to the Docker daemon` | Docker Desktop is closed | Launch Docker Desktop and wait for the whale icon in the taskbar to turn steady. |
| `Bind for 0.0.0.0:3000 failed: port is already allocated` | Another app or previous container is using port 3000 | Find and kill it: `docker ps` then `docker rm -f <id>`, or change the host port to `-p 3005:3000`. |
| Windows: `The term 'curl' was not recognized` or argument errors | PowerShell alias conflict | Always type `curl.exe` instead of `curl`. |
| Windows: `\r: command not found` | Git converted line endings to CRLF | The repository includes `.gitattributes`. Run `git checkout-index --force --all` or open files in VS Code and switch line endings to LF. |
| Laptop running low on disk space | Leftover images/containers | Run `docker system prune -a --volumes`. |