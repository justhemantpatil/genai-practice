import sys
import os
import threading
from tracing.logger import get_app_logger

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
logger = get_app_logger()

def trace_calls(frame, event, arg):
    if event != "call":
        return trace_calls

    file_path = frame.f_code.co_filename
    if not file_path.startswith(PROJECT_ROOT) or "tracing" in file_path or "venv" in file_path:
        return trace_calls

    file_name = os.path.basename(file_path)
    function_name = frame.f_code.co_name
    line_no = frame.f_code.co_firstlineno

    class_name = "-"
    if "self" in frame.f_locals:
        class_name = frame.f_locals["self"].__class__.__name__

    logger.info(f"File Name:- {file_name} |Class Name:- {class_name} |Function Name {function_name} | line={line_no}")
    return trace_calls

def enable_tracing():
    sys.settrace(trace_calls)
    threading.settrace(trace_calls)
