import requests
import base64
import json
import os

legacy_ids = [3048406, 971500, 2283856, 2628078, 2417720, 2436993]
output_dir = r"c:\Users\thai0\OneDrive\Documents\Codepath\AI201\ai201-project1-unofficial-guide-starter\documents"

os.makedirs(output_dir, exist_ok=True)

def get_professor_id(legacy_id):
    plain = f"Teacher-{legacy_id}"
    return base64.b64encode(plain.encode('utf-8')).decode('utf-8')

def fetch_and_save(legacy_id):
    url = "https://www.ratemyprofessors.com/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Authorization": "Basic dGVzdDp0ZXN0",
        "Content-Type": "application/json",
        "Referer": f"https://www.ratemyprofessors.com/professor/{legacy_id}"
    }
    
    prof_id = get_professor_id(legacy_id)
    
    query = """
    query TeacherRatings($id: ID!, $count: Int!) {
      node(id: $id) {
        ... on Teacher {
          firstName
          lastName
          department
          school {
            name
          }
          avgRating
          avgDifficulty
          numRatings
          ratings(first: $count) {
            edges {
              node {
                comment
                class
                date
                difficultyRating
                helpfulRating
                clarityRating
                grade
              }
            }
          }
        }
      }
    }
    """
    
    payload = {
        "query": query,
        "variables": {
            "id": prof_id,
            "count": 100 # Fetch up to 100 ratings
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"].get("node"):
            prof = data["data"]["node"]
            filename = f"professor_{legacy_id}_{prof['firstName']}_{prof['lastName']}.json".replace(" ", "_")
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(prof, f, indent=2, ensure_ascii=False)
            print(f"Saved {prof['firstName']} {prof['lastName']} to {filename}")
        else:
            print(f"Failed to parse node for legacy_id {legacy_id}. Response: {data}")
    else:
        print(f"Failed to fetch legacy_id {legacy_id}. Status: {response.status_code}")

for lid in legacy_ids:
    fetch_and_save(lid)
