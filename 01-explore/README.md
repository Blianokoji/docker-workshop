# 🧭 Module 1: What Even Is a Container?

Welcome to your first hands-on Docker module! The purpose of this module is to demystify what a container actually is.

---

## 💡 The Core Concept: Process Isolation, Not a Virtual Machine

A virtual machine emulates an entire physical computer, including a virtual CPU, virtual memory, and a full guest operating system running on top of a hypervisor. This makes VMs heavy (gigabytes in size) and slow to boot (minutes).

**A Docker container is NOT a virtual machine.**
A container is simply a **normal host process** restricted and isolated using two fundamental Linux kernel features:
1. **Namespaces**: Isolates what a process can *see* (hostname, process tree, network interfaces, filesystem mount points, users).
2. **Control Groups (cgroups)**: Limits what a process can *use* (CPU, RAM, disk I/O).

Because containers share the host Linux kernel (via WSL 2 on Windows or natively on Linux), they boot in milliseconds and consume virtually zero extra memory.

---

## 🛠️ Step-by-Step Hands-On Guide

### Step 1: Pull and Run the Interactive Sandbox
Run the pre-built sandbox container. The `-it` flags attach your interactive terminal to the container.

#### 🪟 Windows (PowerShell / Command Prompt)
```powershell
docker run -it --rm --name my-sandbox dracalar/docker-workshop-explore
```

#### 🐧 Linux / macOS (Bash / Zsh)
```bash
docker run -it --rm --name my-sandbox dracalar/docker-workshop-explore
```

> **Flag Breakdown:**
> - `run`: Tells Docker to create and start a container.
> - `-i` (interactive): Keeps standard input (STDIN) open.
> - `-t` (tty): Allocates a pseudo-terminal (gives you colors and prompt).
> - `--rm`: Automatically deletes the container when you exit (keeps your machine clean).
> - `--name my-sandbox`: Assigns a friendly name instead of a random generated one.
> - `dracalar/docker-workshop-explore`: The image repository on Docker Hub.

---

### Step 2: Inspect Container Isolation

Once you are inside the container prompt (`bash-5.2#`), execute these commands:

#### 1. Check the hostname
```bash
hostname
```
*Notice:* The hostname is a random alphanumeric hash (e.g. `d8b3c4a1e902`). It does **not** match your computer's name!

#### 2. Check the operating system
```bash
cat /etc/os-release
```
*Notice:* Inside the container, you are running **Alpine Linux**, regardless of whether your host laptop is Windows 11, Ubuntu, or macOS.

#### 3. Inspect isolated processes
```bash
ps aux
```
*Notice:* You only see 2 or 3 processes! Process ID 1 (`PID 1`) is your shell process. None of your host's hundreds of background applications are visible.

#### 4. Test network egress
```bash
curl -s https://icanhazip.com
```
*Notice:* The container has its own virtual network card with outbound internet access.

#### 5. Generate ASCII art with pre-installed tools
```bash
figlet "Docker Rocks"
```

---

### Step 3: The "Aha!" Moment — Proving Ephemeral Storage

Containers are **ephemeral** by default. Any files you create inside a container's writable layer exist only as long as that container lives.

#### 1. Create a secret file inside the container:
```bash
echo "Docker was here in 2026!" > /secret.txt
ls -l /secret.txt
cat /secret.txt
```

#### 2. Exit the container:
```bash
exit
```

#### 3. Start a brand new container from the exact same image:
#### 🪟 Windows (PowerShell) / 🐧 Linux (Bash)
```bash
docker run -it --rm dracalar/docker-workshop-explore
```

#### 4. Look for `/secret.txt`:
```bash
ls -l /secret.txt
```
*Expected Output:*
```
ls: /secret.txt: No such file or directory
```

🎉 **Key Takeaway:** The image is immutable (read-only). Every new container starts from a pristine clean slate. (In Module 3, we will learn how **Volumes** solve persistent data storage!)

---

### Step 4: Running in the Background (Detached Mode)

Sometimes you want a container to run in the background (like a web server or database) without tying up your terminal.

#### 1. Start a detached container:
```bash
docker run -d --name bg-sandbox dracalar/docker-workshop-explore sleep 300
```
*Flag `-d` (detached) tells Docker to run the process in the background and print the container ID.*

#### 2. View running containers:
```bash
docker ps
```

#### 3. View container logs:
```bash
docker logs bg-sandbox
```

#### 4. Stop and remove the container:
```bash
docker stop bg-sandbox
docker rm bg-sandbox
```

---

## 📋 Command Quick Reference

| Action | Command |
|:---|:---|
| Run interactive container | `docker run -it <image>` |
| Run in background (detached) | `docker run -d <image>` |
| List running containers | `docker ps` |
| List all containers (including stopped) | `docker ps -a` |
| Stop a running container | `docker stop <container>` |
| Remove a stopped container | `docker rm <container>` |
| Force stop and remove | `docker rm -f <container>` |

---

## ❓ Troubleshooting & Common Pitfalls

- **Error: `Unable to find image locally`**: This is normal! Docker is downloading the image from Docker Hub on your first run.
- **Error: `Conflict. The container name "/my-sandbox" is already in use`**: You have an existing stopped or running container with that name. Run `docker rm -f my-sandbox` and try again.
- **Ctrl+C doesn't exit**: Type `exit` or press `Ctrl+D` to cleanly exit an interactive container.