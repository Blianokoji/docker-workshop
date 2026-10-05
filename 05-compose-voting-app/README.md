# 🚀 Module 5: Docker Compose — The Real World

Until now, we ran individual containers manually with long `docker run` commands. In production, real applications consist of multiple microservices, background workers, and databases that need to work together.

**Docker Compose** is a tool for defining and running multi-container Docker applications using a single, readable YAML file (`docker-compose.yml`).

---

## 💡 The Architecture of Our App

```text
[ Browser (User) ]
       │
       ├──► :3000 ──► [ vote-api (Python) ] ──► (Internal) ──► [ redis (In-Memory DB) ]
       │                                                               ▲
       └──► :3001 ──► [ dashboard (Nginx) ] ── (Polls /results) ───────┘
```

1. **`vote-api`**: Python microservice handling votes and serving the voting interface on port 3000.
2. **`redis`**: Official Redis container storing the persistent vote counts.
3. **`dashboard`**: Nginx web server displaying real-time voting percentages and progress bars on port 3001.

---

## 🛠️ Step-by-Step Exercise

### Step 1: Navigate to the Directory

#### 🪟 Windows (PowerShell)
```powershell
cd Documents\docker-workshop\05-compose-voting-app
```

#### 🐧 Linux / macOS (Bash)
```bash
cd ~/docker-workshop/05-compose-voting-app
```

---

### Step 2: Inspect `docker-compose.yml`

Take a look at how clean and declarative the configuration is:

#### 🪟 Windows (PowerShell)
```powershell
Get-Content docker-compose.yml
```

#### 🐧 Linux / macOS (Bash)
```bash
cat docker-compose.yml
```

> **Key Declarations in the YAML:**
> - `services`: The list of containers to deploy.
> - `depends_on`: Tells Docker the order of startup (e.g., start Redis before starting the API).
> - `environment`: Passes configuration (e.g. `REDIS_HOST=redis`) so code doesn't hardcode IPs.
> - `volumes`: Attaches `redis-data` so voting tallies survive even if the containers restart!
> - Docker Compose **automatically creates a shared network** for all services in the file!

---

### Step 3: Launch the Entire Stack with One Command!

#### 🪟 Windows / 🐧 Linux
```bash
docker compose up -d
```

*Watch what happens:*
1. Docker automatically creates the default bridge network (`05-compose-voting-app_default`).
2. Docker creates the persistent Redis volume (`05-compose-voting-app_redis-data`).
3. Docker starts `redis`, waits, starts `vote-api`, then starts `dashboard`.

---

### Step 4: Verify Running Services

Check the status of all containers in your compose project:

```bash
docker compose ps
```

*Expected Output:*
```text
NAME                                  IMAGE                                           COMMAND                  SERVICE     CREATED         STATUS         PORTS
05-compose-voting-app-dashboard-1     dracalar/docker-workshop-vote-dashboard:latest  "/docker-entrypoint.…"   dashboard   5 seconds ago   Up 4 seconds   0.0.0.0:3001->80/tcp
05-compose-voting-app-redis-1         redis:7-alpine                                  "docker-entrypoint.s…"   redis       5 seconds ago   Up 4 seconds   6379/tcp
05-compose-voting-app-vote-api-1      dracalar/docker-workshop-vote-api:latest        "python main.py"         vote-api    5 seconds ago   Up 4 seconds   0.0.0.0:3000->3000/tcp
```

---

### Step 5: Test the Multi-Container Experience

1. Open **[http://localhost:3000](http://localhost:3000)** in your browser:  
   👉 Cast several votes for **Cats 🐱**, **Dogs 🐶**, or **Capybaras 🦫**!
2. Open **[http://localhost:3001](http://localhost:3001)** in a side-by-side browser window:  
   👉 Watch the live progress bars update in real time as votes are registered in Redis!

---

### Step 6: View Unified Logs in Real Time

Instead of running `docker logs` on 3 separate containers, Docker Compose aggregates all logs into a unified, color-coded stream:

```bash
docker compose logs -f
```
*(Press `Ctrl+C` to stop following logs).*

To follow logs for just the API service:
```bash
docker compose logs -f vote-api
```

---

### Step 7: Peek Inside Redis with `docker compose exec`

Want to see the actual keys and counters inside Redis without installing Redis tools on your computer?

```bash
docker compose exec redis redis-cli MGET vote:cats vote:dogs vote:capybaras
```
*Expected Output:* You will see the raw integer counts stored in the database!

---

### Step 8: Scaling Services Effortlessly

Need more API throughput? With Compose, you can scale stateless microservices in one command:

```bash
docker compose up -d --scale vote-api=3
```

Check running services again:
```bash
docker compose ps
```
You now have **3 parallel API containers** running simultaneously!

---

### Step 9: Clean Teardown

To stop and remove all containers, networks, and volumes cleanly:

```bash
docker compose down -v
```
*(The `-v` flag also removes the Redis named volume, giving you a fresh start).*

---

## 🎯 Key Takeaways
1. Docker Compose allows you to manage multi-container apps as **Infrastructure as Code**.
2. Service names (e.g. `redis`) become internal hostnames for DNS resolution.
3. One command (`docker compose up -d`) starts the entire application stack.
4. One command (`docker compose down -v`) tears everything down cleanly.