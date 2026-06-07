# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Course and professor reviews for CS at UIC - useful because official course descriptions don't reflect teaching style, exam difficulty, or workload. This is valuable for students who want to know what to expect from a course or professor.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | RateMyProfessors | website | https://www.ratemyprofessors.com/professor/3048406 |
| 2 | UIC Reddit | website | https://www.reddit.com/r/uichicago/comments/1fh57aq/how_can_i_be_successful_in_cs_251/ |
| 3 | RateMyProfessors | website | https://www.ratemyprofessors.com/professor/971500 |
| 4 | RateMyProfessors | website | https://www.ratemyprofessors.com/professor/2283856 |
| 5 | RateMyProfessors | website | https://www.ratemyprofessors.com/professor/2628078 |
| 6 | UIC Reddit | website | https://www.reddit.com/r/uichicago/comments/1f9ydi1/honest_advice_for_taking_cs_211_cs_251_cs_261_in/ |
| 7 | RateMyProfessors | website | https://www.ratemyprofessors.com/professor/2417720 |
| 8 | UIC Reddit | website | https://www.reddit.com/r/uichicago/comments/1gps8qg/cs_301cs_277_cs_261/ |
| 9 | RateMyProfessors | website | https://www.ratemyprofessors.com/professor/2436993 |
| 10 | UIC Reddit | website | https://www.reddit.com/r/uichicago/comments/1cfqye1/comment/l1t7q4o/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
Variable, targeting each comment as a single chunk (some 500-600 characters) but could split longer comments into multiple chunks if they are too long. Prepend context metadata such as professor name, professor ID, rating, and course name to each chunk for (Rate My Professors sources). For UIC Reddit sources, prepend the subreddit name, thread title, and author to each chunk.

**Overlap:**
0 characters

**Why these choices fit your documents:**
Since reviews and comments are short, self-contained, and the metadata (professor name, professor ID, rating, course name for Rate My Professors sources; subreddit name, thread title, author for UIC Reddit sources) is prepended to each chunk, there is no need for overlap. The chunks are already semantically rich due to the metadata and the nature of the review text.

**Final chunk count:**
432
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
If cost wasn't a constraint in a production system, I would consider using a model like OpenAI's `text-embedding-3-small` instead of `all-MiniLM-L6-v2`. This is because it has a larger context window, which would allow me to capture the entire text of longer documents without having to split them into smaller chunks. Additionally, it has been shown to perform better on a wider range of tasks, including those involving domain-specific text.

---

## Retrieval Evaluation

### Test Example 1
*   **Query:** `What language will we use in CS 251?`
*   **Top Returned Chunks:**
    *   **Match 1 (RRF Score: 0.032540):** 
        `Source: Reddit | Thread Title: How can I be successful in CS 251? | Comment by Inevitable_Carry_720: I mostly just know Java. I'm also taking 211, and I'm able to pick up C from that class pretty easily. But when it comes to C++, I can't grasp the language for some reason. Our first project is called Ciphers, and it's about encoding and decrypting strings.`
    *   **Match 2 (RRF Score: 0.032522):** 
        `Source: Reddit | Thread Title: How can I be successful in CS 251? | Comment by joshua9663: What language do you have experience in? C to C++ is very transferable and so is Java. Different languages same concepts. What was your first project by a chance?`
    *   **Match 3 (RRF Score: 0.030777):** 
        `Source: Reddit | Thread Title: How can I be successful in CS 251? | Comment by joshua9663: Great there's so much involved in these languages. Is there any particular aspect that you find the hardest to grasp? The easiest way to learn would be searching in a language you are familiar with and for the c++ equivalent in it. 251 is a super hard course, and even harder if your professor is new to the language as well...`
*   **Relevance Explanation:** 
    Match 1 explicitly mentions struggling to grasp "C++" in the context of the course's first project (Ciphers). Matches 2 and 3 mentions transitions from Java/C to C++ in CS 251.

### Test Example 2
*   **Query:** `What is professor Ayala like?`
*   **Top Returned Chunks:**
    *   **Match 1 (RRF Score: 0.033060):** 
        `Professor: Daniel Ayala | Department: Computer Science | School: University of Illinois Chicago | Course: CS251 | Course Grade: B+ | Reviewer Difficulty Rating: 3/5 | Reviewer Rating: 5/5 | Review: 251 was a challenging class, but it never was an unfair class. Lecturers were so huge, yet Ayala was able to condense and make all the information so easy to digest. Would def take again if I had the chance. Really nice professor to, and got on your level when in Office Hours.`
    *   **Match 2 (RRF Score: 0.032522):** 
        `Professor: Daniel Ayala | Department: Computer Science | School: University of Illinois Chicago | Course: CS251 | Course Grade: A | Reviewer Difficulty Rating: 4/5 | Reviewer Rating: 5/5 | Review: Very chill professor and very supportive during help hours. extra credits for early project submission and labs are nice. Lectures are amazing when it comes to explaining the difficult concepts. There is also paired oral exams.`
    *   **Match 3 (RRF Score: 0.031754):** 
        `Professor: Daniel Ayala | Department: Computer Science | School: University of Illinois Chicago | Course: CS251 | Course Grade: A | Reviewer Difficulty Rating: 4/5 | Reviewer Rating: 5/5 | Review: Very good professor, easy to talk to, and approachable.`
*   **Relevance Explanation:** 
    Match 1 describes him as a "really nice professor" who "gets on your level when in Office Hours." Match 2 notes he is a "very chill professor" who is "supportive during help hours," and Match 3 highlights that he is "approachable" and "easy to talk to."

### Test Example 3
*   **Query:** `How do students feel about professor McCarty?`
*   **Top Returned Chunks:**
    *   **Match 1 (RRF Score: 0.032258):** 
        `Professor: Evan McCarty | Department: Computer Science | School: University of Illinois Chicago | Course: CS342 | Course Grade: A | Reviewer Difficulty Rating: 3/5 | Reviewer Rating: 5/5 | Review: An excellent professor that truly cares about his students. His coursework is somewhat high, but very manageable and flexible. He gives a lot of opportunities to succeed in his courses, and I have learned so much from his lectures.`
    *   **Match 2 (RRF Score: 0.031258):** 
        `Professor: Evan McCarty | Department: Computer Science | School: University of Illinois Chicago | Course: CS342 | Course Grade: A | Reviewer Difficulty Rating: 3/5 | Reviewer Rating: 5/5 | Review: McCarty makes his expectations for homework, quizzes, and projects very clear and reasonable. The lectures are always engaging and actually useful for learning, rather than busywork. He is definitely a great teacher and passionate about helping his students succeed.`
    *   **Match 3 (RRF Score: 0.028006):** 
        `Professor: Evan McCarty | Department: Computer Science | School: University of Illinois Chicago | Course: CS301 | Course Grade: C | Reviewer Difficulty Rating: 4/5 | Reviewer Rating: 4/5 | Review: He's a pretty cool professor, relatively understanding of the course load students have. A lot of his lectures tend to be more abstract, so if you aren't good at connecting the dots for concepts, you're going to have a hard time.`
*    **Relevance Explanation:**
     Match 1 describes McCarty as "an excellent professor that truly cares about his students" and notes that his coursework is "very manageable and flexible." Match 2 states that McCarty "makes his expectations for homework, quizzes, and projects very clear and reasonable" and that his lectures are "always engaging and actually useful for learning." Match 3 calls him a "pretty cool professor" who is "relatively understanding of the course load students have."

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
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

**How source attribution is surfaced in the response:**
The system retrieves the top 5 chunks of the user's query using Reciprocal Rank Fusion over vector search and keyword match scores. It then passes these chunks to the Groq API, along with a system prompt that instructs the model to answer the user's question using ONLY the provided document blocks and to cite which document block each fact comes from. The model then returns the answer, which is then printed to the console along with the sources.

**Test example 1**
- Question: What language will we use in CS 251?
- Answer: The language used in CS 251 is C++, as mentioned in the context of the first project called Ciphers, which is about encoding and decrypting strings [Source: reddit_1fh57aq_success_in_cs251.json].

**Test example 2**
- Question: What is professor Ayala like?
- Answer: Professor Ayala is described as a "very chill professor" and "very supportive during help hours" [Source: professor_3048406_Daniel_Ayala.json], and also as "very good professor, easy to talk to, and approachable" [Source: professor_3048406_Daniel_Ayala.json]. He is also mentioned to be "really nice" and able to "get on your level when in Office Hours" [Source: professor_3048406_Daniel_Ayala.json]. Additionally, he is described as "so sweet" and explains concepts well, making the class enjoyable and helping students who are struggling [Source: professor_3048406_Daniel_Ayala.json].

**Test example 3**
- Question: What is the best restaurant to eat at near UIC?
- Answer: I don't have enough information on that.


---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What language will we use in CS 251? | C++ | The language used in CS 251 is C++, as the first project is called Ciphers.| Relevant | Accurate |
| 2 | What is professor Ayala like? | Average rating 4.4, nice, sweet, chill professor | Professor Ayala is described as a "very chill professor" and "very supportive during help hours", and also as "very good professor, easy to talk to, and approachable". | Relevant | Accurate |
| 3 | Is CS 251 hard? | It is challenging | CS 251 is considered a challenging course, as it takes C++ and introduces core data structures/algorithms, and it is one of the weed-out courses for a CS major, requiring long periods of time to understand and implement projects. | Relevant | Accurate |
| 4 | How do students feel about professor McCarty? | Good professor for logic class but sometimes has grading errors | Students have a very positive view of Professor McCarty, describing him as "excellent", "great", "energetic", "caring", and "tough". | Partially relevant | Partially accurate |
| 5 | How do students feel about professor DasGupta? | One of the best professor, easy exams, easy to get an A | One thinks he is "a real gem" and "amazing", a funny and caring professor who makes class enjoyable, with an easy grading system. However, another expresses dissatisfaction with his teaching style, stating that they had to teach themselves everything to get an A in the class | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
How do students feel about professor McCarty?

**What the system returned:**
Students have a very positive view of Professor McCarty, describing him as "excellent", "great", "energetic", "caring", and "tough".

**Root cause (tied to a specific pipeline stage):**

The retrieval pipeline is too reliant on vector search, which is not always accurate. Because Professor McCarty is a very popular professor, there are many reviews for him, and the vector search returns only the top `k=5` chunks. These chunks are all positive, so the model only sees positive reviews and responds with a positive answer. 

**What you would change to fix it:**
1. Increase the context window parameter `k` for general professor opinion queries, allowing the retrieval layer to capture a wider distribution of reviews.
2. Implement a diversity-based re-ranking step (e.g., Maximal Marginal Relevance or sentiment-based clustering) to ensure that the retrieved context blocks represent a balanced mix of positive and negative/constructive feedback rather than being dominated by the most common sentiment.

---

## Interface and Sample Interaction

### Interface Fields
My Gradio-based web interface consists of the following input and output elements:
1. **Input Field:**
   - **Query Textbox:** A single-line text input field where students type their questions about UIC CS courses or professors.
2. **Output Fields:**
   - **Grounded Answer Textarea:** A read-only multi-line textarea showing the final response generated by the Groq LLM. The answer is strictly grounded in the retrieved chunks and includes inline source citations (e.g., `[Source: filename.json]`).
   - **Verified Source Documents Textarea:** A read-only smaller textarea displaying a clean list of verified sources from which the answer was compiled.

---

### Sample Interaction Transcript

**User Input Query:**
> "What language will we use in CS 251?"

**Grounded Answer Output:**
> "The language used in CS 251 is C++, as mentioned in the context of the first project called Ciphers, which is about encoding and decrypting strings [Source: reddit_1fh57aq_success_in_cs251.json]."

**Verified Source Documents Output:**
> "Source: reddit_1fh57aq_success_in_cs251.json"

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
It gave me a good idea of what to expect from each task and what I needed to do to complete it. It also helped me to plan my time effectively and make sure that I was on track to complete the project on time.

**One way your implementation diverged from the spec, and why:**
My implementation diverged from the initial planning spec in how I decided to display the results. Initially, I planned to just display the answer and the sources in the same textarea. However, I realized that it would be more helpful to display the sources separately, so I added a separate textarea for the sources.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I provided the design rulesfor the Gradio interface and a sample Gradio app. 
- *What it produced:* It initially produced a layout wrapping all elements inside a single nested container with a side textbox and button row
- *What I changed or overrode:* I changed the design to remove the outermost container, change the search block to stack the input and button vertically, and center the "Ask Engine" button.

**Instance 2**

- *What I gave the AI:* I provide the planning for the wire up generation in query.py file.
- *What it produced:* It gave me a query.py file where it basically rewrote all the functions in embed_and_retrieve.py file.
- *What I changed or overrode:* I refactored the code by importing the existing functions in embed_and_retrieve.py file instead of generating all the functions again. This made the file shorter and more concise.
