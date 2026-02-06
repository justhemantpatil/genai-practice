import time

def get_all_notes():
    # Simulated database
    return [
        {"id": 1, "title": "First Note", "content": "Hello World"},
        {"id": 2, "title": "Work", "content": "Finish the tracing demo"}
    ]

def process_note_data(title: str, content: str):
    """
    Example of nested functions to demonstrate complex logic
    """
    def validate_title(t):
        return len(t) > 2

    def format_content(c):
        def add_timestamp(text):
            return f"[{time.ctime()}] {text}"
        
        return add_timestamp(c.strip())

    if not validate_title(title):
        return {"error": "Invalid title"}

    final_content = format_content(content)
    
    return {
        "processed_title": title.upper(),
        "processed_content": final_content,
        "uuid": str(time.time_ns())
    }
