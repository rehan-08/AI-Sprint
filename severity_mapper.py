SEVERITY_LEVELS = {
    "Major": {"color": "red", "advice": "Avoid combination. Seek medical attention."},
    "Moderate": {"color": "orange", "advice": "Use with caution. Consult your doctor."},
    "Minor": {"color": "yellow", "advice": "Minimal clinical significance. Monitor if needed."}
}

def get_severity_info(severity: str) -> dict:
    return SEVERITY_LEVELS.get(severity, {"color": "gray", "advice": "No specific advice."})