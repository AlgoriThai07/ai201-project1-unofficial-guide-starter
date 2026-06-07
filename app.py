import gradio as gr
from query import ask

# Custom premium CSS for glassmorphism, gradients, and modern typography
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

html, body, .gradio-container {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #0b0f19 !important;
}

/* Restrict container width and center it */
.gradio-container {
    max-width: 850px !important;
    margin: 40px auto !important;
    padding: 0 20px !important;
}

/* Header Area */
.header-container {
    text-align: center;
    margin-bottom: 32px;
}

.main-title {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 36px !important;
    background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
    text-align: center;
}

.sub-title {
    font-size: 16px;
    color: #94a3b8;
    margin-top: 0px;
    text-align: center;
}

/* Unified Card Styling */
.search-box, .response-box {
    background: rgba(17, 25, 40, 0.5) !important;
    -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
}

/* Inputs & Outputs Style */
.gr-box, .gr-input, .gr-output, textarea, input[type="text"] {
    background-color: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
    transition: all 0.3s ease;
}

.gr-input:focus, textarea:focus, input[type="text"]:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25) !important;
}

/* Centered Ask Button Styling */
.primary-btn {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4) !important;
    transition: all 0.3s ease !important;
    margin: 16px auto 0 auto !important;
    display: block !important;
    max-width: 200px !important;
    width: 100% !important;
}

.primary-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6) !important;
    filter: brightness(1.1);
}

label span {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

.sources-box {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border-radius: 12px;
}
"""

def handle_query(question):
    if not question.strip():
        return "Please enter a valid question.", "No sources retrieved."
    
    result = ask(question)
    
    # Format the programmatic sources list cleanly
    formatted_sources = []
    for s in result["sources"]:
        # Extract clean names from filenames (e.g. professor_3048406_Daniel_Ayala.json -> Daniel Ayala (RMP))
        if s.startswith("professor_"):
            parts = s.split("_")
            # Usually parts: ['professor', 'ID', 'First', 'Last.json']
            first = parts[2]
            last = parts[3].replace(".json", "")
            formatted_sources.append(f"• RateMyProfessors: {first} {last}")
        elif s.startswith("reddit_"):
            # e.g. reddit_1fh57aq_success_in_cs251.json
            topic = s.split("_", 2)[2].replace(".json", "").replace("_", " ").title()
            formatted_sources.append(f"• UIC Reddit: \"{topic}\"")
        else:
            formatted_sources.append(f"• {s}")
            
    sources_text = "\n".join(formatted_sources) if formatted_sources else "No sources found."
    return result["answer"], sources_text

# Create UI with gr.Blocks using the Ocean theme and custom CSS overrides
theme = gr.themes.Ocean(
    primary_hue="blue",
    secondary_hue="violet",
    neutral_hue="slate"
)

with gr.Blocks() as demo:
    # Header Section
    gr.HTML("<h1 class='main-title'>The Unofficial UIC CS Guide</h1>")
    gr.Markdown(
        "Ask questions about UIC Computer Science courses and professors. "
        "Answers are strictly grounded in student reviews and Reddit course threads with full source citation.",
        elem_classes="sub-title"
    )
        
    # Search Section
    with gr.Group(elem_classes="search-box"):
        inp = gr.Textbox(
            label="What would you like to know?",
            placeholder="e.g., How should I prepare for CS 251? or What is professor McCarty like?",
            lines=1
        )
        btn = gr.Button("Ask Engine", elem_classes="primary-btn")
        
    # Response Section
    with gr.Group(elem_classes="response-box"):
        answer = gr.Textbox(
            label="Grounded Answer",
            placeholder="The answer will appear here...",
            lines=8,
            interactive=False
        )
        sources = gr.Textbox(
            label="Verified Source Documents",
            placeholder="Source citations will appear here...",
            lines=3,
            interactive=False,
            elem_classes="sources-box"
        )
        
    # Examples/Shortcuts
    gr.Examples(
        examples=[
            ["What language will we use in CS 251?"],
            ["What is professor Ayala like?"],
            ["How do students feel about professor McCarty?"],
            ["What is the best restaurant to eat at near UIC?"]
        ],
        inputs=inp,
        label="Example Questions to Try"
    )
    
    # Link submission events
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme=theme, css=CUSTOM_CSS)
