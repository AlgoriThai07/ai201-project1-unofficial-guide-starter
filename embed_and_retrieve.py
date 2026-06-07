import os
import json
import string
import re
import sys
from sentence_transformers import SentenceTransformer
import chromadb

# Ensure output prints UTF-8 cleanly
sys.stdout.reconfigure(encoding='utf-8')

CHUNKS_FILE = r"c:\Users\thai0\OneDrive\Documents\Codepath\AI201\ai201-project1-unofficial-guide-starter\chunks.json"
CHROMA_PATH = r"c:\Users\thai0\OneDrive\Documents\Codepath\AI201\ai201-project1-unofficial-guide-starter\chroma_db"

print("Loading chunks.json...")
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks.")

print("Initializing SentenceTransformer('all-MiniLM-L6-v2')...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Setting up ChromaDB PersistentClient...")
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Use cosine similarity space
collection = client.get_or_create_collection(
    name="unofficial_guide",
    metadata={"hnsw:space": "cosine"}
)

# Populate collection if empty
if collection.count() == 0:
    print("Embedding chunks and loading into ChromaDB (this may take a minute)...")
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    # Generate embeddings in batches of 64
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True).tolist()
    
    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully loaded {collection.count()} vectors into ChromaDB.")
else:
    print(f"ChromaDB collection already contains {collection.count()} vectors.")

# ----------------- Hybrid Search Components -----------------

def keyword_search(query, top_n=20):
    """
    Computes a keyword frequency score for each chunk.
    Gives bonus weights for exact matches of key identifiers like course codes (e.g. CS 251).
    """
    # Tokenize the query
    raw_words = [w.lower().strip(string.punctuation) for w in query.split()]
    
    # Common stop words & metadata tokens to ignore so they don't pollute search relevance
    stop_words = {
        "what", "is", "like", "how", "do", "about", "feel", "will", "we", "use", "in", 
        "professor", "reddit", "uichicago", "chicago", "source", "course", "department", 
        "school", "thread", "title", "comment", "by", "reviewer", "rating", "difficulty",
        "grade", "post", "original", "are", "you", "they", "them", "for", "with", "and", 
        "the", "this", "but"
    }
    
    # Filter short words and stop words
    query_words = [w for w in raw_words if (len(w) > 2 or w.isdigit()) and w not in stop_words]
    
    scored_results = []
    for idx, chunk in enumerate(chunks):
        text = chunk["text"].lower()
        score = 0.0
        for word in query_words:
            if word in text:
                score += 1.0
                # Give a huge boost for matching exact word boundaries (especially alphanumeric course codes/names)
                if re.search(r'\b' + re.escape(word) + r'\b', text):
                    score += 1.5
        if score > 0:
            scored_results.append((score, chunk, idx))
            
    # Sort descending by score
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return scored_results[:top_n]

def retrieve(query, k=5):
    """
    Implements Hybrid Search (Vector Search + Keyword Search) using Reciprocal Rank Fusion (RRF).
    """
    # 1. Vector Search
    query_embedding = model.encode([query]).tolist()
    vector_results = collection.query(
        query_embeddings=query_embedding,
        n_results=20
    )
    
    vector_ranked = []
    if vector_results["documents"] and vector_results["documents"][0]:
        for idx in range(len(vector_results["documents"][0])):
            doc = vector_results["documents"][0][idx]
            meta = vector_results["metadatas"][0][idx]
            dist = vector_results["distances"][0][idx]
            vector_ranked.append({
                "text": doc,
                "metadata": meta,
                "distance": dist
            })
            
    # 2. Keyword Search
    keyword_ranked = keyword_search(query, top_n=20)
    
    # 3. Reciprocal Rank Fusion (RRF)
    # Score(d) = sum_{m in models} 1 / (60 + rank_m(d))
    rrf_scores = {}
    doc_details = {}
    
    # Process vector ranks
    for rank, item in enumerate(vector_ranked):
        text = item["text"]
        doc_details[text] = item
        rrf_scores[text] = rrf_scores.get(text, 0.0) + (1.0 / (60.0 + rank))
        
    # Process keyword ranks
    for rank, (score, chunk, idx) in enumerate(keyword_ranked):
        text = chunk["text"]
        if text not in doc_details:
            doc_details[text] = {
                "text": text,
                "metadata": chunk["metadata"],
                "distance": 1.0 # default distance if vector search missed it
            }
        rrf_scores[text] = rrf_scores.get(text, 0.0) + (1.0 / (60.0 + rank))
        
    # Sort by RRF score descending
    merged = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Extract top k results
    top_k_results = []
    for text, score in merged[:k]:
        details = doc_details[text]
        top_k_results.append({
            "text": text,
            "metadata": details["metadata"],
            "distance": details["distance"],
            "rrf_score": score
        })
        
    return top_k_results

# ----------------- Evaluation Test -----------------

test_queries = [
    "What language will we use in CS 251?",
    "What is professor Ayala like?",
    "How do students feel about professor McCarty?"
]

print("\n" + "="*50)
print("RUNNING RETRIEVAL EVALUATION TESTS")
print("="*50)

for q_idx, query in enumerate(test_queries):
    print(f"\nQuery #{q_idx+1}: '{query}'")
    results = retrieve(query, k=3)
    
    for r_idx, res in enumerate(results):
        print(f"\n  Match {r_idx+1}:")
        print(f"    Source: {res['metadata'].get('source', 'Unknown')}")
        print(f"    Type: {res['metadata'].get('type', 'Unknown')}")
        print(f"    Cosine Distance: {res['distance']:.4f}")
        print(f"    RRF Score: {res['rrf_score']:.6f}")
        print(f"    Content:\n      {res['text']}")
        print("    " + "-"*30)
