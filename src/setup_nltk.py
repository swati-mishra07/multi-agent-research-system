# Simple in-memory storage (can upgrade to DB later)

memory_store = []


def save_memory(data):
    if data:
        memory_store.append(data)


def get_memory():
    return memory_store[-3:]  # return last 3 for context
