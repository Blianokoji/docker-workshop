# 💾 Module 3: Docker Volumes — Data That Survives

By default, everything written inside a container is written to its temporary writable layer. When the container is deleted (`docker rm`), all of that data is destroyed forever.

In this module, you will learn how **Docker Volumes** and **Bind Mounts** give containers persistent, durable storage.

---

## 💡 The Core Concepts

| Storage Type | Managed By | Where It Lives | Best Used For |
|:---|:---|:---|:---|
| **Container Layer** | Docker | Inside container (ephemeral) | Temporary scratch files |
| **Named Volume** | Docker | `/var/lib/docker/volumes/` | Databases, persistent app state |
| **Bind Mount** | You (Host) | Any host path (e.g. `C:\Users\...` or `/home/...`) | Live code reloading during development |

---

## 🛠️ Step-by-Step Exercise

### Part 1: The Trap — Running WITHOUT a Volume (Watch Data Die)

Let's run the notes app directly without any volume.

#### 🪟 Windows (PowerShell) / 🐧 Linux (Bash)
```bash
docker run -d -p 5000:5000 --name test-unpersisted dracalar/docker-workshop-notebook
```

#### 1. Open the app in your browser:
Navigate to **[http://localhost:5000](http://localhost:5000)** and type a few notes:
- "Note 1: Docker is fast"
- "Note 2: Will this note survive?"

Or post a note via command line:
#### 🪟 Windows (PowerShell)
```powershell
curl.exe -X POST http://localhost:5000/api/notes -H "Content-Type: application/json" -d "{\"note\": \"Hello from PowerShell\"}"
```
#### 🐧 Linux / macOS (Bash)
```bash
curl -X POST http://localhost:5000/api/notes -H "Content-Type: application/json" -d '{"note": "Hello from Linux"}'
```

#### 2. Kill and delete the container:
```bash
docker rm -f test-unpersisted
```

#### 3. Start a fresh container:
```bash
docker run -d -p 5000:5000 --name test-unpersisted-2 dracalar/docker-workshop-notebook
```

#### 4. Refresh [http://localhost:5000](http://localhost:5000):
😱 **Your notes are gone!** Because there was no volume attached, the data died with `test-unpersisted`.

#### Clean up before Part 2:
```bash
docker rm -f test-unpersisted-2
```

---

### Part 2: The Solution — Running WITH a Named Volume

A **Named Volume** is managed completely by Docker. Even when containers are stopped, removed, or upgraded, the volume remains safely stored on disk.

#### 1. Start a container attached to a named volume (`my-notes-volume`):
#### 🪟 Windows / 🐧 Linux
```bash
docker run -d -p 5000:5000 -v my-notes-volume:/app/data --name notes-app-v1 dracalar/docker-workshop-notebook
```

> **Syntax Breakdown (`-v my-notes-volume:/app/data`):**
> `<Volume Name> : <Container Path>`  
> Docker mounts the persistent volume `my-notes-volume` into `/app/data` inside the container. If the volume doesn't exist yet, Docker creates it automatically!

#### 2. Add some important notes:
Visit **[http://localhost:5000](http://localhost:5000)** and add:
- "Critical Note: Docker volumes are persistent!"
- "Another Note: Upgrading containers is safe now."

#### 3. Obliterate the container!
```bash
docker rm -f notes-app-v1
```

#### 4. Start a brand new container attached to the SAME volume:
```bash
docker run -d -p 5000:5000 -v my-notes-volume:/app/data --name notes-app-v2 dracalar/docker-workshop-notebook
```

#### 5. Refresh [http://localhost:5000](http://localhost:5000):
🎉 **ALL YOUR NOTES ARE STILL THERE!**  
Notice that the **Container ID** in the web UI header has changed, but the notes persisted completely intact.

#### Clean up:
```bash
docker rm -f notes-app-v2
```

---

### Part 3: Live Development with Bind Mounts

What if you want to mount a folder from your actual laptop into the container so you can see and edit the files directly from your desktop? That is called a **Bind Mount**.

#### 1. Create a local folder for notes on your host:

#### 🪟 Windows (PowerShell)
```powershell
New-Item -ItemType Directory -Path .\my-local-notes -Force
```

#### 🐧 Linux / macOS (Bash)
```bash
mkdir -p ./my-local-notes
```

#### 2. Run the container with a bind mount:

#### 🪟 Windows (PowerShell)
```powershell
docker run -d -p 5000:5000 -v ${PWD}/my-local-notes:/app/data --name notes-bind-mount dracalar/docker-workshop-notebook
```
*(Notice: In PowerShell, we use `${PWD}` to represent the current directory).*

#### 🐧 Linux / macOS (Bash)
```bash
docker run -d -p 5000:5000 -v $(pwd)/my-local-notes:/app/data --name notes-bind-mount dracalar/docker-workshop-notebook
```
*(Notice: In Linux/macOS, we use `$(pwd)`).*

#### 3. Save a note in the browser:
Go to **[http://localhost:5000](http://localhost:5000)** and save: "Testing Host Bind Mount".

#### 4. Check your host laptop's local folder!

#### 🪟 Windows (PowerShell)
```powershell
Get-Content .\my-local-notes\notes.json
```

#### 🐧 Linux / macOS (Bash)
```bash
cat ./my-local-notes/notes.json
```

🔥 The JSON file is directly on your laptop's filesystem! You can edit `notes.json` in Notepad or VS Code, refresh your browser, and the container instantly reflects your changes.

#### Clean up:
```bash
docker rm -f notes-bind-mount
```

---

### Part 4: Managing Docker Volumes

Docker gives you dedicated commands to manage volumes:

```bash
# List all Docker volumes on your machine
docker volume ls

# Inspect details of a volume (mount point, driver, labels)
docker volume inspect my-notes-volume

# Remove a specific volume (must not be in use by any container)
docker volume rm my-notes-volume

# Remove all unused volumes (frees disk space)
docker volume prune
```

---

## 🎯 Key Takeaways
1. Containers are disposable; data in containers is lost on deletion.
2. Use **Named Volumes** (`-v volume_name:/path`) for databases and production state.
3. Use **Bind Mounts** (`-v ${PWD}/local_folder:/path`) for active local software development.