import json
import os
import sys
from bs4 import BeautifulSoup

# Ensure python console output supports UTF-8
sys.stdout.reconfigure(encoding='utf-8')

output_dir = r"c:\Users\thai0\OneDrive\Documents\Codepath\AI201\ai201-project1-unofficial-guide-starter\documents"

files_mapping = [
    {
        "input_path": r"C:\Users\thai0\.gemini\antigravity-ide\brain\5c6f8821-5c13-4467-ba01-e6d77f7e47e2\.system_generated\steps\112\content.md",
        "output_name": "reddit_1fh57aq_success_in_cs251.json"
    },
    {
        "input_path": r"C:\Users\thai0\.gemini\antigravity-ide\brain\5c6f8821-5c13-4467-ba01-e6d77f7e47e2\.system_generated\steps\128\content.md",
        "output_name": "reddit_1f9ydi1_advice_cs211_251_261.json"
    },
    {
        "input_path": r"C:\Users\thai0\.gemini\antigravity-ide\brain\5c6f8821-5c13-4467-ba01-e6d77f7e47e2\.system_generated\steps\130\content.md",
        "output_name": "reddit_1gps8qg_cs301_277_261.json"
    },
    {
        "input_path": r"C:\Users\thai0\.gemini\antigravity-ide\brain\5c6f8821-5c13-4467-ba01-e6d77f7e47e2\.system_generated\steps\132\content.md",
        "output_name": "reddit_1cfqye1_comment_thread.json"
    }
]

def parse_reddit_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Try to find post title and text from standard HTML tags if JSON-LD is missing
    post_title = ""
    title_tag = soup.find("title")
    if title_tag:
        post_title = title_tag.get_text().replace(" : r/uichicago", "").strip()
        
    # Find selftext (original post text)
    post_text = ""
    post_container = soup.find("div", slot="post-media-container") or soup.find("shreddit-post")
    if post_container:
        # Check for selftext div
        selftext_div = post_container.find("div", class_="md")
        if selftext_div:
            post_text = selftext_div.get_text(strip=True)
            
    comments = []
    seen_comments = set()
    
    def add_comment(author, text):
        if not text:
            return
        # Replace smart quotes with standard quotes
        text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').strip()
        # Create a unique key for deduplication
        key = (author.lower(), text[:100].lower())
        if key not in seen_comments:
            seen_comments.add(key)
            comments.append({
                "author": author,
                "text": text
            })

    # Method 1: Parse JSON-LD Schema
    scripts = soup.find_all("script", type="application/ld+json")
    for s in scripts:
        try:
            data = json.loads(s.string)
            items = data if isinstance(data, list) else [data]
            for item in items:
                if item.get("@type") in ["QAPage", "DiscussionForumPosting"]:
                    if item.get("@type") == "QAPage":
                        main = item.get("mainEntity", {})
                        if main.get("name"):
                            post_title = main.get("name", post_title)
                        if main.get("text"):
                            post_text = main.get("text", post_text)
                        
                        def traverse_ld_comments(comment_data):
                            if not comment_data:
                                return
                            if isinstance(comment_data, list):
                                for c in comment_data:
                                    traverse_ld_comments(c)
                            elif isinstance(comment_data, dict):
                                auth = comment_data.get("author", {}).get("name", "Unknown")
                                val = comment_data.get("text", "")
                                add_comment(auth, val)
                                if "comment" in comment_data:
                                    traverse_ld_comments(comment_data["comment"])
                                    
                        if "acceptedAnswer" in main:
                            traverse_ld_comments(main["acceptedAnswer"])
                        if "suggestedAnswer" in main:
                            traverse_ld_comments(main["suggestedAnswer"])
                        if "comment" in main:
                            traverse_ld_comments(main["comment"])
                    else:  # DiscussionForumPosting
                        if item.get("headline"):
                            post_title = item.get("headline", post_title)
                        if item.get("articleBody") or item.get("text"):
                            post_text = item.get("articleBody", item.get("text", post_text))
                        
                        def traverse_posting_comments(comment_data):
                            if not comment_data:
                                return
                            if isinstance(comment_data, list):
                                for c in comment_data:
                                    traverse_posting_comments(c)
                            elif isinstance(comment_data, dict):
                                auth = comment_data.get("author", {}).get("name", "Unknown")
                                val = comment_data.get("text", "")
                                add_comment(auth, val)
                                if "comment" in comment_data:
                                    traverse_posting_comments(comment_data["comment"])
                                    
                        if "comment" in item:
                            traverse_posting_comments(item["comment"])
        except Exception as e:
            pass

    # Method 2: Parse <shreddit-comment> tags directly from HTML
    shreddit_comments = soup.find_all("shreddit-comment")
    for c in shreddit_comments:
        author = c.get("author", "Unknown")
        # Try to find comment text inside slot="comment" or class="md" or get_text
        text_container = c.find("div", class_="md") or c.find("div", slot="comment")
        if text_container:
            text = text_container.get_text(strip=True)
        else:
            text = c.get_text(strip=True)
        add_comment(author, text)

    return {
        "title": post_title,
        "text": post_text,
        "comments": comments
    }

for item in files_mapping:
    if os.path.exists(item["input_path"]):
        parsed_data = parse_reddit_html(item["input_path"])
        output_path = os.path.join(output_dir, item["output_name"])
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        print(f"Parsed and saved {item['output_name']} with {len(parsed_data['comments'])} comments. Title: '{parsed_data['title']}'")
    else:
        print(f"Warning: file not found at {item['input_path']}")
