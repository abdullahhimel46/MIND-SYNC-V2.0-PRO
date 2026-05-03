# 🧠 MIND SYNC V2.0 PRO

### 🌍 Real-Life Problem & Solution
**The Problem:** Standard AI models (like ChatGPT) are brilliant but "blind" to your private data. Whether it's your company's internal policies, a 500-page research paper, or your personal study notes, a general AI cannot answer specific questions about them without you manually copying and pasting huge amounts of text—which is tedious and often impossible due to context limits.

**The Solution:** **MIND SYNC** provides a high-performance **RAG (Retrieval-Augmented Generation)** pipeline. It allows you to "sync" your private documents (PDF, DOCX, TXT) into a local vector memory. Once synced, the AI gains "instant expertise" on your specific data, providing accurate, grounded answers through a premium, minimalist interface.

---

### 🚀 Core Features
*   **Dynamic Neural Indexing**: Upload and sync documents in real-time without restarting the server.
*   **Hybrid LLM Intelligence**: Implements a dual-model failover (GPT-3.5 Turbo + GPT-4o-mini) for maximum uptime.
*   **Multi-Format Support**: Native parsing for `.pdf`, `.docx`, and `.txt` files.
*   **Premium Glassmorphism UI**: A custom-styled Streamlit interface featuring radial gradients and fluid micro-animations.
*   **Source Transparency**: Every response reveals exactly which document snippets were used as context.
*   **Professional Refusal Protocol**: Specifically tuned to avoid hallucinations when information is missing from your documents.

---

### 🏗️ System Architecture

```text
                ┌──────────────────────────────┐
                │          USER (UI)           │
                │   (Streamlit / Web UI)       │
                └─────────────┬────────────────┘
                              │
                              ▼
                ┌──────────────────────────────┐
                │        FastAPI Backend       │
                │  (Query Handling + Routing)  │
                └─────────────┬────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼

     ┌──────────────────────┐     ┌────────────────────────┐
     │  Query Embedding     │     │   Document Ingestion    │
     │ (OpenRouter/OpenAI)  │     │ (PDF/DOCX/TXT Upload)   │
     └─────────┬────────────┘     └──────────┬─────────────┘
               │                             │
               ▼                             ▼
     ┌──────────────────────┐     ┌────────────────────────┐
     │     FAISS Vector     │◄────┤  Chunk + Embed Docs     │
     │       Database       │     │ (Real-time Indexing)    │
     └─────────┬────────────┘     └────────────────────────┘
               │
               ▼
     ┌──────────────────────┐
     │  Similarity Search   │
     │   (Top-K Context)    │
     └─────────┬────────────┘
               │
               ▼
     ┌──────────────────────────────┐
     │   Prompt Construction Layer  │
     │ (Context + User Query)       │
     └─────────────┬────────────────┘
                   │
                   ▼
     ┌──────────────────────────────┐
     │   LLM (OpenRouter Models)    │
     │  - Primary (GPT-3.5)         │
     │  - Fallback (GPT-4o-mini)    │
     └─────────────┬────────────────┘
                   │
                   ▼
     ┌──────────────────────────────┐
     │      Final Response          │
     │ + Source Audit (Context)     │
     └─────────────┬────────────────┘
                   │
                   ▼
         ┌──────────────────────┐
         │     UI Response      │
         │ (Chat Display)       │
         └──────────────────────┘
```

---

### 🛠️ Tech Stack
*   **Backend**: FastAPI (Asynchronous Python API)
*   **Frontend**: Streamlit (Custom CSS/Glassmorphism)
*   **Vector Engine**: FAISS (Facebook AI Similarity Search)
*   **Embeddings**: OpenAI `text-embedding-3-small`
*   **LLM Orchestration**: OpenRouter API
*   **Data Parsing**: PyPDF2, python-docx

---

### 📥 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd SimpleChatBOT
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory and add your OpenRouter API Key:
   ```env
   OPENROUTER_API_KEY=your_actual_key_here
   ```

---

### ▶️ Running the Application

This project requires two terminals to run simultaneously:

**Terminal 1: Start the Backend (Brain)**
```bash
uvicorn main:app --reload
```

**Terminal 2: Start the Frontend (Body)**
```bash
streamlit run app.py
```

---

### 📁 Project Structure
```plaintext
SimpleChatBOT/
├── main.py            # FastAPI Backend & RAG Logic
├── app.py             # Streamlit Frontend & Custom Styling
├── documents.txt      # Initial Knowledge Base
├── requirements.txt   # Project Dependencies
├── .env               # API Configuration (Secret)
└── README.md          # Documentation
```

---

### ⚖️ License
© 2026 ALL RIGHTS RESERVED • **DEV ABDULLAH**
