import requests
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import networkx as nx
from src.logger import get_logger

logger = get_logger()

# -------- Ensure NLTK --------
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
    nltk.download("punkt_tab")


# -------- PDF Extraction --------
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        logger.info("PDF text extracted successfully")
        return text

    except Exception as e:
        logger.error(f"PDF Error: {e}")
        return ""


# -------- Arxiv API --------
def search_arxiv(topic, max_results=5):
    try:
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{topic}&start=0&max_results={max_results}"
        )
        response = requests.get(url).text

        entries = response.split("<entry>")
        results = []

        for entry in entries[1:]:
            title = entry.split("<title>")[1].split("</title>")[0]
            summary = entry.split("<summary>")[1].split("</summary>")[0]
            link = entry.split("<id>")[1].split("</id>")[0]

            results.append(
                {
                    "title": title.strip(),
                    "summary": summary.strip(),
                    "link": link.strip(),
                }
            )

        logger.info(f"Fetched {len(results)} papers from Arxiv")
        return results

    except Exception as e:
        logger.error(f"Arxiv Error: {e}")
        return []


# -------- NLP Summarization --------
def summarize_text(text, num_sentences=5):
    try:
        sentences = sent_tokenize(text)

        if len(sentences) <= num_sentences:
            return text

        vectorizer = TfidfVectorizer(stop_words="english")
        X = vectorizer.fit_transform(sentences)

        scores = np.array(X.sum(axis=1)).flatten()
        ranked_sentences = [sentences[i] for i in scores.argsort()[::-1]]

        summary = " ".join(ranked_sentences[:num_sentences])

        logger.info("Text summarized successfully")
        return summary

    except Exception as e:
        logger.error(f"Summarization Error: {e}")
        return text


# -------- Knowledge Graph --------
def build_knowledge_graph(text):
    try:
        words = list(set(text.split()[:15]))
        G = nx.Graph()

        for w1 in words:
            for w2 in words:
                if w1 != w2:
                    G.add_edge(w1, w2)

        logger.info("Knowledge graph created")
        return G

    except Exception as e:
        logger.error(f"Graph Error: {e}")
        return None


def evaluate_summary(original, summary):
    try:
        original_len = len(original.split())
        summary_len = len(summary.split())

        if original_len == 0:
            return {
                "Original Length": 0,
                "Summary Length": summary_len,
                "Compression Ratio": 0,
            }

        compression_ratio = summary_len / original_len

        return {
            "Original Length": original_len,
            "Summary Length": summary_len,
            "Compression Ratio": round(compression_ratio, 2),
        }

    except Exception as e:
        return {"error": str(e)}
