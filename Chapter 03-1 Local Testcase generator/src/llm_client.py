"""LLM client - calls Ollama (local, default) or Groq (hosted fallback).

Provider selection:
    auto    try Ollama first, fall back to Groq when Ollama is down
    ollama  Ollama only (raises LLMError if unavailable)
    groq    Groq only

generate_test_cases() returns (text, provider_used) so the UI can show
which backend produced the result.
"""

import requests

try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None


class LLMError(Exception):
    """Raised when the selected provider cannot produce a result."""


class OllamaUnavailable(LLMError):
    """Ollama server is not reachable or rejected the request."""


SYSTEM_PROMPT = (
    "You are a Senior QA Engineer with 7+ years of manual testing "
    "experience. Follow the provided instructions strictly. Use ONLY "
    "information explicitly provided in the requirements. Do NOT invent "
    "or assume undocumented behavior. If information is missing, state "
    "'Not specified'."
)


def extract_markdown_table(text: str) -> str:
    """Return only the markdown table from an LLM response.

    The LLM sometimes wraps the table in commentary. This finds the
    first block of consecutive lines that look like a markdown table
    (lines starting with '|') and returns it, or the original text
    if no table is found.
    """
    lines = text.splitlines()
    table_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            in_table = True
            table_lines.append(stripped)
        elif in_table and stripped == "":
            break
        elif in_table:
            # Stop at the first non-empty, non-table line after the table
            break

    if len(table_lines) >= 3:  # header + separator + at least one row
        return "\n".join(table_lines)
    return text.strip()


def generate_test_cases(prompt: str, settings: dict) -> tuple[str, str]:
    """Generate test cases for the given prompt.

    Returns (markdown_text, provider_used). provider_used is
    'ollama', 'groq', or 'groq (fallback)'.
    """
    provider = settings.get("LLM_PROVIDER", "auto").lower()

    if provider == "groq":
        return _call_groq(prompt, settings), "groq"

    if provider == "ollama":
        return _call_ollama(prompt, settings), "ollama"

    # auto - default behaviour
    try:
        return _call_ollama(prompt, settings), "ollama"
    except OllamaUnavailable:
        return _call_groq(prompt, settings), "groq (fallback)"


# ----------------------------------------------------------------------
# Ollama
# ----------------------------------------------------------------------

def _call_ollama(prompt: str, settings: dict) -> str:
    url = settings.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
    model = settings.get("OLLAMA_MODEL", "gemma3:1b")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    try:
        response = requests.post(f"{url}/api/chat", json=payload, timeout=120)
    except requests.RequestException as exc:
        raise OllamaUnavailable(
            f"Ollama at {url} is not reachable. Make sure the server is "
            f"running (ollama serve)."
        ) from exc

    if response.status_code != 200:
        raise OllamaUnavailable(
            f"Ollama returned HTTP {response.status_code}: "
            f"{response.text[:300]}"
        )

    try:
        data = response.json()
        return data["message"]["content"].strip()
    except (ValueError, KeyError) as exc:
        raise OllamaUnavailable(
            "Ollama returned an unexpected response."
        ) from exc


# ----------------------------------------------------------------------
# Groq
# ----------------------------------------------------------------------

def _call_groq(prompt: str, settings: dict) -> str:
    api_key = settings.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise LLMError(
            "GROQ_API_KEY is missing from .env. Add it or switch the "
            "provider to 'ollama'."
        )
    if Groq is None:
        raise LLMError(
            "The 'groq' package is not installed. Run "
            "pip install -r requirements.txt"
        )

    model = settings.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_completion_tokens=8192,
        )
        return completion.choices[0].message.content.strip()
    except Exception as exc:
        raise LLMError(f"Groq request failed: {exc}") from exc
