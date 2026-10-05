# ⚡ Module 6: Cool Tricks & Docker Superpowers

Here is a collection of high-impact, practical Docker tricks that every developer should know to boost their everyday productivity.

---

## 🎩 Trick 1: Run Any Tool Without Installing It on Your Laptop

Need Python 3.13, Node 22, Rust, or Go for a 2-minute test, but don''t want to pollute your laptop with global runtimes? Use `docker run --rm`:

#### Run a one-line Python script:
```bash
docker run --rm python:3.12-alpine python -c "import sys; print('Python', sys.version)"
```

#### Test a Node.js snippet:
```bash
docker run --rm node:22-alpine node -e "console.log('Today is:', new Date().toLocaleDateString())"
```

#### Format JSON with `jq` without installing jq:
```bash
echo '{"status": "awesome", "count": 42}' | docker run --rm -i stedolan/jq .status
```

> **Why `--rm` matters:** The `--rm` flag tells Docker to instantly destroy and delete the container as soon as the command finishes. Your disk stays completely clean!

---

## 📊 Trick 2: Live Resource Monitoring with `docker stats`

Want to see live CPU, Memory, Network I/O, and PID usage of all running containers in a terminal dashboard?

```bash
docker stats
```

To see a single non-streaming snapshot:
```bash
docker stats --no-stream
```

---

## 🔍 Trick 3: Executing a Live Shell in a Running Container

Never wonder what is happening inside a container. Drop directly into an active container with `docker exec`:

```bash
docker exec -it <container_name> sh
```
*(Or `bash` if the container has bash installed).*

You can run commands directly without entering the interactive shell:
```bash
docker exec <container_name> env
docker exec <container_name> df -h
```

---

## 📂 Trick 4: Copy Files In and Out of Containers with `docker cp`

You don''t need to rebuild an image or mount a volume just to extract a log file or inject a configuration file!

#### Copy a file FROM a container to your laptop:
```bash
docker cp <container_name>:/app/data/notes.json ./extracted-notes.json
```

#### Copy a file FROM your laptop INTO a container:
```bash
docker cp ./my-config.txt <container_name>:/app/config.txt
```

---

## 🔎 Trick 5: Extract Exact IP Addresses with `docker inspect`

Need to know the internal virtual IP address of a container without scrolling through 200 lines of JSON? Use `--format`:

```bash
docker inspect --format "{{ .NetworkSettings.IPAddress }}" <container_name>
```

Or on custom bridge networks:
```bash
docker inspect --format "{{ range .NetworkSettings.Networks }}{{ .IPAddress }}{{ end }}" <container_name>
```

---

## ⏸️ Trick 6: Freeze Containers Instantly with `docker pause`

Need to free up your CPU while playing a game or compiling heavy code without terminating your running containers and losing memory state?

```bash
# Freeze all processes in the container (uses SIGSTOP cgroup)
docker pause <container_name>

# Unfreeze instantly (uses SIGCONT)
docker unpause <container_name>
```

---

## 🧹 Trick 7: Find What is Eating Your Disk Space & Nuke It

Containers, dangling images, and build caches can consume gigabytes over time.

#### 1. See exactly where your disk space is going:
```bash
docker system df
```

*Example Output:*
```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          12        3         1.42GB    850MB (59%)
Containers      4         2         12.4kB    6.2kB (50%)
Local Volumes   5         2         120MB     80MB (66%)
Build Cache     34        0         2.1GB     2.1GB
```

#### 2. Clean unused dangling images and stopped containers:
```bash
docker system prune
```

#### 3. The Nuclear Option (Clean Slate):
Deletes all stopped containers, all unused networks, all dangling images, and build caches:
```bash
docker system prune -a --volumes
```

---

## ⚡ Useful Shell Aliases

Add these to your shell config for instant shortcuts:

#### 🪟 Windows (Add to `$PROFILE` in PowerShell):
```powershell
function dps { docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" }
function dstopall { docker stop $(docker ps -q) }
function drmall { docker rm -f $(docker ps -aq) }
```

#### 🐧 Linux / macOS (Add to `~/.bashrc` or `~/.zshrc`):
```bash
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dstopall='docker stop $(docker ps -q)'
alias drmall='docker rm -f $(docker ps -aq)'
alias dprune='docker system prune -a --volumes'
```