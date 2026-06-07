import os
import json
import random
import re

documents_dir = r"c:\Users\thai0\OneDrive\Documents\Codepath\AI201\ai201-project1-unofficial-guide-starter\documents"
output_file = r"c:\Users\thai0\OneDrive\Documents\Codepath\AI201\ai201-project1-unofficial-guide-starter\chunks.json"

chunks = []

def clean_text(text):
    if not text:
        return ""
    # Remove excessive whitespace, newlines, and unicode spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# 1. Process RateMyProfessors documents
def process_professor_file(filepath, filename):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    first_name = data.get("firstName", "Unknown")
    last_name = data.get("lastName", "Unknown")
    prof_name = f"{first_name} {last_name}".strip()
    dept = data.get("department", "Unknown")
    school = data.get("school", {}).get("name", "University of Illinois Chicago")
    avg_rating = data.get("avgRating", "N/A")
    avg_diff = data.get("avgDifficulty", "N/A")
    
    ratings_edges = data.get("ratings", {}).get("edges", [])
    file_chunks_count = 0
    
    for edge in ratings_edges:
        node = edge.get("node", {})
        comment = clean_text(node.get("comment", ""))
        course = clean_text(node.get("class", "Unknown"))
        grade = clean_text(node.get("grade", "N/A"))
        diff = node.get("difficultyRating", "N/A")
        rating = node.get("helpfulRating", "N/A")
        
        # Skip empty comments
        if not comment or len(comment) < 10:
            continue
            
        # Build structured chunk content
        chunk_text = (
            f"Professor: {prof_name} | Department: {dept} | School: {school} | "
            f"Course: {course} | Course Grade: {grade} | Reviewer Difficulty Rating: {diff}/5 | "
            f"Reviewer Rating: {rating}/5 | Review: {comment}"
        )
        
        metadata = {
            "source": filename,
            "type": "rate_my_professors",
            "professor_name": prof_name,
            "course": course,
            "grade": grade,
            "average_difficulty": avg_diff,
            "average_rating": avg_rating
        }
        
        chunks.append({
            "text": chunk_text,
            "metadata": metadata
        })
        file_chunks_count += 1
        
    print(f"Processed RMP file: {filename} -> Generated {file_chunks_count} chunks.")

# 2. Process Reddit documents
def process_reddit_file(filepath, filename):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    title = clean_text(data.get("title", "Unknown Thread"))
    post_body = clean_text(data.get("text", ""))
    reddit_comments = data.get("comments", [])
    
    file_chunks_count = 0
    
    # Chunk 1: The original post body (if not empty)
    if post_body and len(post_body) > 15:
        post_chunk = f"Source: Reddit | Thread Title: {title} | Original Post: {post_body}"
        chunks.append({
            "text": post_chunk,
            "metadata": {
                "source": filename,
                "type": "reddit_post",
                "thread_title": title,
                "author": "OP"
            }
        })
        file_chunks_count += 1
        
    # Chunk 2+: Individual comments
    for c in reddit_comments:
        author = c.get("author", "Unknown")
        comment_text = clean_text(c.get("text", ""))
        
        # Skip short/empty/deleted comments
        if not comment_text or len(comment_text) < 15 or author.lower() in ["deleted", "auto-moderator"]:
            continue
            
        comment_chunk = f"Source: Reddit | Thread Title: {title} | Comment by {author}: {comment_text}"
        chunks.append({
            "text": comment_chunk,
            "metadata": {
                "source": filename,
                "type": "reddit_comment",
                "thread_title": title,
                "author": author
            }
        })
        file_chunks_count += 1
        
    print(f"Processed Reddit file: {filename} -> Generated {file_chunks_count} chunks.")

# Iterate over all files in documents/ directory
for filename in os.listdir(documents_dir):
    filepath = os.path.join(documents_dir, filename)
    if not filename.endswith(".json"):
        continue
    if filename.startswith("professor_"):
        process_professor_file(filepath, filename)
    elif filename.startswith("reddit_"):
        process_reddit_file(filepath, filename)

# Save generated chunks to file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print("\n" + "="*50)
print(f"Total chunks generated: {len(chunks)}")
print("="*50 + "\n")

# Print 5 random chunks for inspection
if chunks:
    print("--- 5 RANDOM CHUNKS FOR INSPECTION ---")
    sample_chunks = random.sample(chunks, min(5, len(chunks)))
    for idx, c in enumerate(sample_chunks):
        print(f"\nChunk #{idx+1}:")
        print(f"Metadata: {c['metadata']}")
        print(f"Text Content:\n{c['text']}")
        print("-" * 40)
