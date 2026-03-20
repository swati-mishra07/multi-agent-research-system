from src.semantic_search import semantic_search
from src.tools import summarize_text


def detect_question_type(query):
    query = query.lower()

    if "what" in query:
        return "definition"
    elif "how" in query:
        return "process"
    elif "why" in query:
        return "reason"
    elif "advantage" in query or "benefit" in query:
        return "advantages"
    elif "challenge" in query or "limitation" in query:
        return "challenges"
    else:
        return "general"


def format_answer(answer, qtype):
    if qtype == "definition":
        return f"📌 **Explanation:**\n{answer}"

    elif qtype == "process":
        steps = answer.split(". ")
        formatted = "\n".join([f"- {s}" for s in steps if s])
        return f"⚙️ **Process:**\n{formatted}"

    elif qtype == "advantages":
        points = answer.split(". ")
        formatted = "\n".join([f"✅ {p}" for p in points if p])
        return f"🚀 **Advantages:**\n{formatted}"

    elif qtype == "challenges":
        points = answer.split(". ")
        formatted = "\n".join([f"⚠️ {p}" for p in points if p])
        return f"⚠️ **Challenges:**\n{formatted}"

    elif qtype == "reason":
        return f"❓ **Reason:**\n{answer}"

    else:
        return f"💡 **Answer:**\n{answer}"


def chat_with_paper(query, text):
    try:
        # Step 1: Find relevant chunks
        chunks = semantic_search(query, text)

        # Step 2: Combine context
        context = " ".join(chunks)

        # Step 3: Generate summary
        raw_answer = summarize_text(context)

        # Step 4: Detect type
        qtype = detect_question_type(query)

        # Step 5: Format output
        final_answer = format_answer(raw_answer, qtype)

        return final_answer

    except Exception as e:
        return f"Error: {str(e)}"
