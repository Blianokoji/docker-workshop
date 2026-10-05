# 🌐 Module 4: Container Networking & Service Discovery

In real-world applications, systems are composed of multiple microservices: frontends, APIs, background workers, and databases.

In this module, you will learn how **Docker Networks** allow containers to talk to each other securely using **automatic DNS service discovery** without hardcoding IP addresses.

---

## 💡 The Core Concepts

### 1. The Default Bridge vs User-Defined Networks
When Docker installs, it creates a default network named `bridge`.
- ❌ **Default `bridge` limitation**: Containers on the default bridge can only reach each other by **IP address**, NOT by container name!
- ✅ **User-Defined Bridge Network**: Automatically includes an **embedded DNS server**. Containers on the same custom network can find each other using their container names (e.g. `http://api:8000`)!

### 2. Network Security & Port Isolation
If your backend database or internal API should only be accessed by your web server, **you do not publish its port to your host machine (`-p`)**.
- Only the frontend publishes its port to the outside world (`-p 8080:80`).
- The backend remains invisible to the outside internet, accessible solely inside the private Docker network.

---

## 🛠️ Step-by-Step Exercise

### Part 1: The Failure — Running Without a Network

Let''s start the frontend container without our backend API.

#### 🪟 Windows (PowerShell) / 🐧 Linux (Bash)
```bash
docker run -d -p 8080:80 --name test-frontend dracalar/docker-workshop-frontend
```

Now open your browser to **[http://localhost:8080](http://localhost:8080)**.
- *Notice:* The UI shows **"Backend Unreachable"** and an error message explaining that it cannot resolve or reach `http://api:8000`.

#### Clean up before Part 2:
```bash
docker rm -f test-frontend
```

---

### Part 2: The Solution — Custom Bridge Network & DNS

#### 1. Create a custom user-defined bridge network:
```bash
docker network create workshop-net
```

#### 2. Run the backend API on `workshop-net`:
```bash
docker run -d --network workshop-net --name api dracalar/docker-workshop-api
```

> **Security Note:** Notice there is **NO `-p 8000:8000`** flag!  
> The API container is only accessible to other containers attached to `workshop-net`.

#### 3. Run the frontend on `workshop-net` (and expose it to your browser):
```bash
docker run -d --network workshop-net --name frontend -p 8080:80 dracalar/docker-workshop-frontend
```

#### 4. Test in your browser:
Open **[http://localhost:8080](http://localhost:8080)** and click **"Fetch New Fact from API"**.

🎉 **It works instantly!**
- The status pill turns **Green (Connected)**.
- The UI shows real-time programming facts returned from the backend.
- The **Backend Host** matches the internal hostname of the `api` container!

---

### Part 3: Inspecting Docker DNS Under the Hood

How does `frontend` know where `api` is? Let''s peek into the network using `docker exec` and `docker network inspect`.

#### 1. Ping the `api` container from inside the `frontend` container:
```bash
docker exec -it frontend ping -c 3 api
```
*Expected Output:*
```text
PING api (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.108 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.082 ms
```
Docker''s internal DNS automatically resolved the name `api` to its virtual IP (e.g. `172.18.0.2`)!

#### 2. Inspect the network details:
```bash
docker network inspect workshop-net
```
You will see both `api` and `frontend` listed under `"Containers"` with their allocated IP addresses.

---

### Part 4: Clean Up

Stop and remove the containers and remove the custom network:

```bash
docker rm -f api frontend
docker network rm workshop-net
```

---

## 🎯 Key Takeaways
1. Never hardcode container IP addresses; IP addresses change whenever containers restart.
2. Always create a custom bridge network (`docker network create <name>`) for multi-container applications.
3. Internal backend services (databases, internal APIs) do not need `-p` port publishing.