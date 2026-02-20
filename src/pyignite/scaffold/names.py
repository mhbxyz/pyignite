import re


def normalize_package_name(project_name: str) -> str:
    """Normalize a project name into a valid Python package name."""

    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", project_name.strip()).lower()
    normalized = re.sub(r"_+", "_", normalized).strip("_")

    if not normalized:
        return "app"
    if normalized[0].isdigit():
        return f"app_{normalized}"
    return normalized
