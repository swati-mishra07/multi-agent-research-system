import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.tools import (
    search_arxiv,
    extract_text_from_pdf,
    summarize_text,
    build_knowledge_graph,
    evaluate_summary,
)
from src.semantic_search import semantic_search
from src.memory import save_memory, get_memory
from src.chat_engine import chat_with_paper

import matplotlib.pyplot as plt
import networkx as nx

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Research Assistant", layout="wide")

# -------- CUSTOM CSS (🔥 BEAUTIFUL UI) --------
st.markdown(
    """
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ffffff;
}
.stTextInput>div>div>input {
    border-radius: 10px;
}
.stButton>button {
    border-radius: 10px;
    background-color: #4CAF50;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------- TITLE --------
st.title("🧠 AI Research Assistant")
st.caption("Smart Research • Semantic Search • NLP Insights")

# -------- INPUT SECTION --------
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("🔍 Enter Research Topic")

with col2:
    pdf = st.file_uploader("📄 Upload PDF", type=["pdf"])

user_query = st.text_input("💬 Ask Question About Research")

# -------- BUTTON --------
if st.button("🚀 Generate Report"):

    with st.spinner("Analyzing research..."):

        # -------- DATA --------
        if pdf:
            os.makedirs("data", exist_ok=True)
            path = os.path.join("data", pdf.name)

            with open(path, "wb") as f:
                f.write(pdf.getbuffer())

            raw_text = extract_text_from_pdf(path)
            references = ["Uploaded PDF"]

        else:
            papers = search_arxiv(topic)
            raw_text = " ".join([p["summary"] for p in papers])
            references = [p["link"] for p in papers]

        # -------- SEMANTIC SEARCH --------
        filtered_text = raw_text
        if topic:
            chunks = semantic_search(topic, raw_text)
            filtered_text = " ".join(chunks)

        # -------- SUMMARY --------
        summary = summarize_text(filtered_text)

        # -------- MEMORY --------
        save_memory(summary)
        memory = get_memory()

        # -------- METRICS --------
        metrics = evaluate_summary(raw_text, summary)

        # -------- GRAPH --------
        kg = build_knowledge_graph(summary)

    # -------- OUTPUT SECTION --------
    st.markdown("---")

    col1, col2 = st.columns(2)

    # -------- LEFT: REPORT --------
    with col1:
        st.subheader("📄 Research Report")

        summary_formatted = summary.replace(". ", "\n- ")
        memory_formatted = str(memory).replace("[", "").replace("]", "")
        references_formatted = "\n".join(references)

        st.markdown(
            f"""
### 🔍 Topic
{topic if topic else "PDF Analysis"}

### 📊 Key Findings
- {summary_formatted}

### 🧠 Previous Context
{memory_formatted}

### 🔗 References
{references_formatted}
"""
        )

        st.download_button("📥 Download Report", summary)

    # -------- RIGHT: GRAPH + METRICS --------
    with col2:
        st.subheader("📊 Insights")

        # Graph
        if kg:
            plt.figure()
            nx.draw(kg, with_labels=True)
            st.pyplot(plt)

        # Metrics
        st.markdown("### 📈 Metrics")
        st.write(metrics)

    # -------- CHAT SECTION --------
    if user_query:
        st.markdown("---")
        st.subheader("💬 Answer")

        answer = chat_with_paper(user_query, raw_text)
        st.success(answer)
