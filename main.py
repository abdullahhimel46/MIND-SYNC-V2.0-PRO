import os
import numpy as np
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Load env
load_dotenv()

# OpenRouter client setup
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

app = FastAPI()

# ----------- Load Documents -----------
with open("documents.txt", "r", encoding="utf-8") as f:
    docs = [d.strip() for d in f.readlines() if d.strip()]

# ----------- Embedding Function -----------
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",  # OpenRouter supports OpenAI-compatible embeddings
        input=text
    )
    return np.array(response.data[0].embedding)

# Create embeddings
doc_embeddings = np.array([get_embedding(doc) for doc in docs]).astype("float32")

# ----------- FAISS Index -----------
dim = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(doc_embeddings)

# ----------- Request Schema -----------
class Query(BaseModel):
    query: str

class DocumentUpload(BaseModel):
    text: str

# ----------- Upload Endpoint -----------
@app.post("/upload")
def upload_document(data: DocumentUpload):
    global docs, index
    # Split by newlines and filter out short lines
    new_docs = [s.strip() for s in data.text.split("\n") if len(s.strip()) > 20]
    
    if not new_docs:
        return {"message": "No significant text found to index."}
    
    # Generate embeddings and add to index
    new_embeddings = np.array([get_embedding(d) for d in new_docs]).astype("float32")
    docs.extend(new_docs)
    index.add(new_embeddings)
    
    return {"message": f"Successfully indexed {len(new_docs)} new segments."}

# ----------- Chat Endpoint -----------
@app.post("/chat")
def chat(q: Query):
    query_embedding = get_embedding(q.query).astype("float32")

    _, I = index.search(np.array([query_embedding]), k=2)

    context = "\n".join([docs[i] for i in I[0]])

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.
If the answer is not found, say "I couldn't find relevant information in the provided documents."

Context:
{context}

Question:
{q.query}
"""

    models = ["openai/gpt-3.5-turbo", "openai/gpt-4o-mini"]
    
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return {
                "answer": response.choices[0].message.content,
                "model_used": model,
                "context": context  # Return context for frontend sources
            }
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue # Try next model
            
    return {"error": "All models failed or are busy."}
