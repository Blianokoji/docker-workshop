# 📖 Docker Workshop Master Cheatsheet (Dual Platform)

This reference sheet covers all commands used in the workshop side-by-side for **Windows (PowerShell)** and **Linux / macOS (Bash)**.

---

## 🖥️ Shell Differences at a Glance

| Task | 🪟 Windows (PowerShell) | 🐧 Linux / macOS (Bash) |
|:---|:---|:---|
| **Current directory variable** | `${PWD}` | `$(pwd)` |
| **Print file to terminal** | `Get-Content file.txt` | `cat file.txt` |
| **Invoke curl reliably** | `curl.exe http://...` | `curl http://...` |
| **Create directory** | `New-Item -ItemType Directory -Path name` | `mkdir -p name` |
| **Remove directory/files** | `Remove-Item -Recurse -Force name` | `rm -rf name` |
| **Set environment variable** | `$env:MY_VAR = "value"` | `export MY_VAR="value"` |
| **Multiline command continuation** | `` ` `` (backtick) at line end | `\` (backslash) at line end |

---

## 🐳 Core Docker Commands

### 1. Containers
| Action | Command | Notes |
|:---|:---|:---|
| Run interactive container | `docker run -it --rm <image>` | Exits clean with `--rm` |
| Run in background | `docker run -d --name <name> <image>` | Prints container ID |
| Publish port to host | `docker run -d -p <host>:<container> <image>` | E.g. `-p 3000:3000` |
| List running containers | `docker ps` | Only shows active containers |
| List ALL containers | `docker ps -a` | Includes stopped/exited |
| View container output | `docker logs <container>` | Use `-f` to stream/follow |
| Execute command inside | `docker exec -it <container> sh` | Drops into running shell |
| Stop a container | `docker stop <container>` | Graceful `SIGTERM` |
| Kill/force remove | `docker rm -f <container>` | Immediate `SIGKILL` |

---

### 2. Images & Building
| Action | Command | Notes |
|:---|:---|:---|
| Build an image | `docker build -t <tag> .` | Dot represents current folder |
| Build without cache | `docker build --no-cache -t <tag> .` | Fresh download of layers |
| List local images | `docker images` | Shows tags and sizes |
| Remove local image | `docker rmi <image>` | Frees local disk space |
| Pull from Docker Hub | `docker pull <image>` | Downloads latest image |
| Push to Docker Hub | `docker push <image>` | Requires prior `docker login` |

---

### 3. Volumes & Storage
| Action | 🪟 Windows (PowerShell) | 🐧 Linux / macOS (Bash) |
|:---|:---|:---|
| Run with **Named Volume** | `docker run -v my-vol:/app/data <image>` | `docker run -v my-vol:/app/data <image>` |
| Run with **Bind Mount** | `docker run -v ${PWD}/data:/app/data <image>` | `docker run -v $(pwd)/data:/app/data <image>` |
| List all volumes | `docker volume ls` | `docker volume ls` |
| Inspect volume details | `docker volume inspect <name>` | `docker volume inspect <name>` |
| Delete a volume | `docker volume rm <name>` | `docker volume rm <name>` |
| Clean unused volumes | `docker volume prune` | `docker volume prune` |

---

### 4. Networking & DNS
| Action | Command | Notes |
|:---|:---|:---|
| Create user network | `docker network create <net-name>` | Creates custom bridge |
| Run on network | `docker run --network <net-name> --name <name> <img>` | Resolvable by `<name>` |
| List networks | `docker network ls` | Shows bridge, host, none |
| Inspect network | `docker network inspect <net-name>` | Shows connected containers & IPs |
| Remove network | `docker network rm <net-name>` | Must stop containers first |

---

### 5. Docker Compose
| Action | Command | Notes |
|:---|:---|:---|
| Start whole stack | `docker compose up -d` | Runs in background |
| Rebuild & start | `docker compose up -d --build` | Forces image recompilation |
| Check stack status | `docker compose ps` | Status of project services |
| Follow all logs | `docker compose logs -f` | Colored unified log stream |
| Execute inside service | `docker compose exec <service> <cmd>` | E.g. `redis-cli` |
| Scale service | `docker compose up -d --scale <svc>=3` | Multiplies container instances |
| Stop and remove | `docker compose down` | Preserves named volumes |
| Teardown + nuke volumes | `docker compose down -v` | Complete fresh start |

---

### 6. Emergency Cleanup & Diagnostics
| Action | Command | Notes |
|:---|:---|:---|
| Disk usage analysis | `docker system df` | See image, volume, and cache sizes |
| Live CPU/RAM monitor | `docker stats` | Live terminal task manager |
| Clean dangling items | `docker system prune` | Safe routine cleanup |
| Nuclear clean slate | `docker system prune -a --volumes` | Destroys ALL stopped containers & images |