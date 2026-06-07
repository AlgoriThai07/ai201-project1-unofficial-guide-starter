import os
import sys
from dotenv import load_dotenv
from groq import Groq
from embed_and_retrieve import retrieve

# Load environment variables (.env)
load_dotenv()

# Ensure standard output uses UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 3. Grounded Generation
def ask(question):
    # Retrieve relevant documents
    retrieved = retrieve(question, k=5)
    
    # Compile context strings and identify source filenames
    context_parts = []
    sources = []
    
    for idx, item in enumerate(retrieved):
        source_name = item["metadata"].get("source", "Unknown Source")
        if source_name not in sources:
            sources.append(source_name)
            
        context_parts.append(
            f"Document Block #{idx+1} [Source: {source_name}]\n"
            f"Content: {item['text']}\n"
            f"---"
        )
        
    context_text = "\n".join(context_parts)
    
    # Grounding System Prompt
    system_prompt = (
        "You are an assistant providing an Unofficial Guide for computer science courses "
        "and professors at the University of Illinois Chicago (UIC).\n\n"
        "INSTRUCTIONS:\n"
        "1. Answer the user's question using ONLY the provided Document Blocks.\n"
        "2. Do NOT use any external or general knowledge about UIC, computer science, or general topics.\n"
        "3. For every claim, fact, or opinion you express, you MUST cite which document block "
        "it came from at the end of the sentence or paragraph (e.g., [Source: filename.json]).\n"
        "4. If the provided document blocks DO NOT contain the answer, you must respond EXACTLY with:\n"
        "\"I don't have enough information on that.\"\n"
        "5. Keep your answer factual, direct, and grounded strictly in the provided text."
    )
    
    user_prompt = f"Retrieved Context:\n{context_text}\n\nUser Question: {question}"
    
    try:
        # Call Groq API
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0  # Keep temperature 0 for strict determinism and grounding
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error during generation: {str(e)}"
        
    return {
        "answer": answer,
        "sources": sources
    }

# Quick Console Evaluation Test
if __name__ == "__main__":
    test_queries = [
        "What language will we use in CS 251?",
        "What is professor Ayala like?",
        "How do students feel about professor McCarty?",
        "What is the best restaurant to eat at near UIC?" # Off-topic to check grounding failure prevention
    ]
    
    print("="*60)
    print("TESTING END-TO-END GROUNDED GENERATION")
    print("="*60)
    
    for idx, q in enumerate(test_queries):
        print(f"\n[Question {idx+1}]: {q}")
        res = ask(q)
        print(f"[Answer]:\n{res['answer']}")
        print(f"[Sources]: {res['sources']}")
        print("-" * 50)
