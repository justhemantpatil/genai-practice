import sys
import os
import threading
import csv
from datetime import datetime
import uuid


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CSV_LOG_FILE = "function_calls.csv"

thread_local = threading.local()

# ---------- Function ID Registry ----------
FUNCTION_ID_MAP = {}
FUNCTION_ID_LOCK = threading.Lock()


def get_function_docstring(frame):
    """
    Safely extracts docstring of the function being executed.
    Returns None if not found.
    """
    try:
        func_name = frame.f_code.co_name
        func_obj = frame.f_globals.get(func_name)
        if func_obj and hasattr(func_obj, "__doc__"):
            return func_obj.__doc__
    except Exception:
        pass

    return None


def get_function_id(function_name):
    """
    Returns a stable UUID for each function name.
    Same function -> same UUID.
    """
    if function_name is None:
        return None

    with FUNCTION_ID_LOCK:
        if function_name not in FUNCTION_ID_MAP:
            FUNCTION_ID_MAP[function_name] = str(uuid.uuid4())
        return FUNCTION_ID_MAP[function_name]

# ----------------------------------------

def get_function_parameter_keys(frame):
    try:
        arg_count = frame.f_code.co_argcount
        return list(frame.f_code.co_varnames[:arg_count]) or None
    except Exception:
        return None


def init_stack():
    if not hasattr(thread_local, "call_stack"):
        thread_local.call_stack = []

def write_csv_row(row):
    file_exists = os.path.isfile(CSV_LOG_FILE)

    with open(CSV_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "trace_id",
                "file",
                "caller_function",
                "caller_function_id",
                "callee_function",
                "callee_function_id",
                "callee_function_doc",
                "callee_function_params",
                "call_depth",
                "line",
                "test_case",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

def trace_calls(frame, event, arg):
    if event != "call":
        return trace_calls

    file_path = frame.f_code.co_filename
    if (
        not file_path.startswith(PROJECT_ROOT)
        or "tracing" in file_path
        or "venv" in file_path
    ):
        return trace_calls

    init_stack()

    file_name = os.path.basename(file_path)
    function_name = frame.f_code.co_name
    line_no = frame.f_code.co_firstlineno

    call_stack = thread_local.call_stack
    caller_function = call_stack[-1] if call_stack else None

    callee_function_id = get_function_id(function_name)
    callee_function_doc = get_function_docstring(frame)
    callee_function_params = get_function_parameter_keys(frame)
    caller_function_id = (
        get_function_id(caller_function) if caller_function else None
    )

    call_stack.append(function_name)

    log_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "trace_id": "test_case_id_1",
        "file": file_name,
        "caller_function": caller_function,
        "caller_function_id": caller_function_id,
        "callee_function": function_name,
        "callee_function_id": callee_function_id,
        "callee_function_doc":callee_function_doc,
        "callee_function_params": callee_function_params,
        "call_depth": len(call_stack),
        "line": line_no,
        "test_case": "test_case_1",
    }

    write_csv_row(log_row)

    def trace_returns(frame, event, arg):
        if event == "return":
            call_stack.pop()
        return trace_returns

    return trace_returns

def enable_tracing():
    sys.settrace(trace_calls)
    threading.settrace(trace_calls)
