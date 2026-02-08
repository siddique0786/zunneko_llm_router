# 🧠 Zunneko LLM Intelligent Router Platform

A **production-ready multi-LLM routing platform** that intelligently selects the best LLM provider based on request complexity, caching, cost efficiency, and system health.

This system includes **streaming responses, observability, resilience patterns, distributed tracing, and cost tracking** — simulating real enterprise AI infrastructure.

---

# 🚀 Features

## 🤖 Intelligent LLM Routing
Automatically selects best provider based on:

- Request complexity
- Cost optimization
- Provider availability
- System health
- Performance metrics

Supported Providers:

- Groq
- Gemini
- Mock fallback provider

---

## ⚡ Multi-Layer Caching

### Exact Cache
- Instant response for identical prompts

### Semantic Cache
- Uses embeddings similarity search
- Avoids duplicate LLM calls

---

## 📡 Streaming Responses
Supports real-time token streaming via FastAPI.

---

## 📊 Observability & Monitoring

### Metrics Tracking
Tracks:

- Cache hit ratio
- Provider usage
- Token usage
- Cost estimation
- Latency metrics

### Distributed Tracing
Tracks:

- Cache lookup time
- Request analysis time
- Provider execution latency
- End-to-end request latency

---

## 🛡 Resilience Patterns

### Circuit Breaker
Automatically disables failing providers.

### Retry Logic
Retries failed provider calls with exponential backoff.

### Fallback Provider
Ensures system reliability.

---

## 💰 Cost Tracking
Estimates cost based on token usage per provider.

---

## 📦 Metrics Snapshot Export
Download JSON snapshot of system metrics.

---

# 🏗 Architecture

User → FastAPI → Intelligent Router
│
├── Exact Cache
├── Semantic Cache
├── Request Analyzer
├── Provider Selector
├── Circuit Breaker
├── Retry Handler
├── LLM Provider
├── Metrics Collector
├── Distributed Tracing
└── Cost Tracker

# 📁 Project Structure

src/
│
├── cache/
├── config/
├── metrics/
├── observability/
├── providers/
├── queue/
├── resilience/
├── router/
├── settings.py
│
├── main.py → FastAPI Server
├── worker.py → Background worker
├── chat_ui.py → Streaming UI


---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/siddique0786/zunneko_llm_router.git
cd zunneko_llm_router

---

##2️⃣ Create Virtual Environment
Windows
```bash
python -m venv venv
venv\Scripts\activate

**Linux / Mac**
```bash
python3 -m venv venv
source venv/bin/activate


## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

##4️⃣ Setup Environment Variables
Create .env file:
```bash
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
REDIS_URL=redis://localhost:6379


🧰 Required Services
Redis
Windows

Use Docker or Redis Windows build.

Linux
```bash
sudo apt install redis-server


Mac
```bash
brew install redis

Run Redis:
```bash
redis-server


###------
## ▶ Running The Project
**Start Worker**:
```bash
python worker.py


**Start FastAPI Server**:
```bash
uvicorn src.main:app --reload

**Start Chat UI**:
```bash
python chat_ui.py


##🌐 API Endpoints
**Streaming Endpoint**:
```bash
GET /stream?prompt=YourQuestion

**Metrics Download**:
```bash
GET /metrics/download


##🧪 Example Usage

**Open in browser:**
```bash
http://localhost:8000/stream?prompt=Explain AI simply

## 📊 Example Metrics Output
```bash
{
  "total_tokens": 500,
  "total_cost": 0.0021,
  "provider_usage": {
    "GroqProvider": 4
  }
}

## 🔄 Routing Logic

**Provider selection depends on:**

    1 Prompt complexity

    2 Cache availability

    3 Circuit breaker state

    4 Retry success/failure