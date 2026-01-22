import threading

trace_context = threading.local()

def set_trace_context(trace_id: str, test_case: str):
    trace_context.trace_id = trace_id
    trace_context.test_case = test_case

def get_trace_id():
    return getattr(trace_context, "trace_id", None)

def get_test_case():
    return getattr(trace_context, "test_case", None)
