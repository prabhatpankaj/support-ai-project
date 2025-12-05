from tools.tickets import get_all_tickets
from tools.sentiment import get_sentiment
from tools.topics import extract_topics
from tools.report import save_report

SAFE_GLOBALS = {
    "get_all_tickets": get_all_tickets,
    "get_sentiment": get_sentiment,
    "extract_topics": extract_topics,
    "save_report": save_report,
}

def run_python(code: str):
    """
    Execute Python code in a controlled environment with access to tools.
    """
    env = {
        "__builtins__": {
            "len": len,
            "range": range,
            "print": print,
            "str": str,
            "int": int,
            "float": float,
            "dict": dict,
            "list": list,
            "tuple": tuple,
            "set": set,
            "sum": sum,
            "max": max,
            "min": min,
            "sorted": sorted,
            "round": round,
            "enumerate": enumerate,
            "zip": zip,
            "abs": abs,
            "all": all,
            "any": any,
        }
    }
    env.update(SAFE_GLOBALS)
    
    try:
        exec(code, env)
        return env.get("result", "Code executed successfully")
    except Exception as e:
        return f"Error executing code: {str(e)}"