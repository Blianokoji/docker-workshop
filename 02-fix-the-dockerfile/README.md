# 🔧 Module 2: Images, Layers & Fixing the Broken Dockerfile

In this module, you will learn how Docker builds images, how the **layer cache** works, and how to debug and fix a broken Dockerfile.

---

## 💡 The Core Concepts

### 1. What is an Image?
A Docker **Image** is a read-only blueprint containing:
- A base operating system (e.g., Alpine Linux).
- Runtime environments (e.g., Node.js, Python).
- Your application code and dependencies.
- Configuration metadata (environment variables, default ports, startup command).

A **Container** is simply a running instance of an image with a thin, writable layer on top.

### 2. Dockerfile Instructions
A Dockerfile is an automated recipe:
- `FROM`: Specifies the parent base image.
- `WORKDIR`: Sets the working directory inside the container for all subsequent commands.
- `COPY`: Copies files from your host computer into the container filesystem.
- `RUN`: Executes commands during the image build process (e.g. installing dependencies).
- `EXPOSE`: Documents which network ports the container listens on at runtime.
- `CMD`: The default command to execute when the container starts.

### 3. Layer Caching (The Superpower of Docker)
Each instruction in a Dockerfile generates a cached layer. If an instruction and the files it touches have not changed since the last build, Docker skips that step and uses the cached layer instantly.
- ⚠️ **Best Practice**: Copy dependency files (`package.json`) and run `npm install` *before* copying your source code (`server.js`). That way, editing code doesn't force Docker to re-download dependencies on every build!

---

## 🛠️ Step-by-Step Exercise

### Step 1: Navigate to the Exercise Directory

#### 🪟 Windows (PowerShell)
```powershell
cd Documents\docker-workshop\02-fix-the-dockerfile
```

#### 🐧 Linux / macOS (Bash)
```bash
cd ~/docker-workshop/02-fix-the-dockerfile
```

---

### Step 2: Try Building the Broken Dockerfile (Watch it Fail!)

Run `docker build` to create an image named `my-broken-app`:

#### 🪟 Windows (PowerShell) / 🐧 Linux (Bash)
```bash
docker build -t my-broken-app .
```

> **Syntax Note:** The `.` at the end tells Docker that the **build context** (the directory of files you want Docker to access) is the current directory.

#### What Happens?
The build crashes with an error like:
```text
npm error code ENOENT
npm error syscall open
npm error path /package.json
npm error enoent Could not read package.json
```
**Why did it fail?** Notice the Dockerfile ran `RUN npm install` *before* copying `package.json` into the image!

---

### Step 3: Spot and Fix the 4 Deliberate Mistakes

Open `Dockerfile` in your favorite editor (VS Code, Neovim, or Notepad). 

Here are the 4 bugs you need to resolve:

1. **Bug 1: Missing `WORKDIR`**:
   Without `WORKDIR`, files are copied into the root folder (`/`), polluting the system.
   *Fix:* Add `WORKDIR /app` right after `FROM node:22-alpine`.

2. **Bug 2: Invalid Instruction Order**:
   `RUN npm install` cannot run without `package.json` present!
   *Fix:* Move `COPY package.json .` *before* `RUN npm install`.

3. **Bug 3: Port Mismatch**:
   The Dockerfile has `EXPOSE 8080`, but if you look inside `server.js`, the code listens on port `3000`!
   *Fix:* Change `EXPOSE 8080` to `EXPOSE 3000`.

4. **Bug 4: Non-Exec Form `CMD`**:
   Using `CMD node server.js` runs via a shell wrapper (`/bin/sh -c`), preventing Linux signals like `SIGTERM` (Ctrl+C) from reaching Node directly.
   *Fix:* Use the JSON exec format: `CMD ["node", "server.js"]`.

---

### Step 4: Verify Your Fix

Compare your updated `Dockerfile` with the reference solution in `Dockerfile.solution`:

#### 🪟 Windows (PowerShell)
```powershell
Get-Content Dockerfile.solution
```

#### 🐧 Linux / macOS (Bash)
```bash
cat Dockerfile.solution
```

Your `Dockerfile` should look like this:
```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package.json .
RUN npm install --production

COPY server.js .

EXPOSE 3000

CMD ["node", "server.js"]
```

---

### Step 5: Build Your Fixed Image

Now build the image again with the tag `my-fixed-app`:

#### 🪟 Windows / 🐧 Linux
```bash
docker build -t my-fixed-app .
```

*Notice:* This time the build completes successfully! You will see `=> naming to docker.io/library/my-fixed-app:latest done`.

---

### Step 6: Test Layer Caching

To see Docker layer caching in action:
1. Re-run `docker build -t my-fixed-app .` without changing any files.
   *Result:* Every step outputs `CACHED` and the build finishes in **under 0.2 seconds**!
2. Open `server.js` and edit the message text.
3. Re-run `docker build -t my-fixed-app .`.
   *Result:* Notice that `RUN npm install` is still `CACHED`! Docker only re-ran the steps starting from `COPY server.js .`.

---

### Step 7: Run Your Container and Test It

Start your container and map host port `3000` to container port `3000`:

#### 🪟 Windows / 🐧 Linux
```bash
docker run -d -p 3000:3000 --name fixed-server my-fixed-app
```

> **Port Mapping Explained (`-p 3000:3000`):**
> `<Host Port> : <Container Port>`  
> Traffic hitting your computer on port 3000 is forwarded into port 3000 of the container.

#### Test the server:
- Open your browser to: **[http://localhost:3000](http://localhost:3000)**

Or test from the command line:

#### 🪟 Windows (PowerShell)
```powershell
curl.exe http://localhost:3000
```
*(Use `curl.exe` in PowerShell to invoke the real curl binary rather than PowerShell's Invoke-WebRequest).*

#### 🐧 Linux / macOS (Bash)
```bash
curl http://localhost:3000
```

*Expected JSON Output:*
```json
{
  "message": "🎉 Congratulations! You fixed the Dockerfile and containerized this app!",
  "container_info": {
    "hostname": "8f2d5a39cb12",
    "platform": "linux",
    "architecture": "x64",
    "node_version": "v22.x.x"
  }
}
```

---

### Step 8: Clean Up

Stop and remove the container:
```bash
docker stop fixed-server
docker rm fixed-server
```

---

## 🎯 Key Takeaways
1. Docker builds images from top to bottom.
2. Place slow, rarely changing commands (`npm install`) early in the Dockerfile so they are cached.
3. Always use `WORKDIR` to keep container filesystems organized.
4. Use JSON array syntax for `CMD ["executable", "param1"]`.