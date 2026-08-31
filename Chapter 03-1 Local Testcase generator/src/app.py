"""Local Test Case Generator - Streamlit app.

Two panels (per the wireframe):
    Left  - chat: type "create test cases for QA-102" and press Send
    Right - settings: shows .env values (masked), provider selector,
            connection test buttons

Run with:  streamlit run src/app.py
"""

import re
from pathlib import Path

import streamlit as st

import config_store
import jira_client
import llm_client

# <chapter root>/src/app.py -> chapter root is parent.parent
CHAPTER_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = CHAPTER_DIR / "Templates"

JIRA_KEY_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def load_template(name: str) -> str:
    """Read a template file from the Templates folder."""
    path = TEMPLATES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {name}")
    return path.read_text(encoding="utf-8")


def list_templates() -> list[str]:
    """Names of all .md template files in the Templates folder."""
    if not TEMPLATES_DIR.exists():
        return []
    return sorted(p.name for p in TEMPLATES_DIR.glob("*.md"))


def build_prompt(template: str, ticket: dict) -> str:
    """Merge the ticket content into the selected template."""
    requirements = (
        f"Ticket: {ticket['key']} - {ticket['summary']}\n\n"
        f"DESCRIPTION:\n{ticket['description']}\n\n"
        f"ACCEPTANCE CRITERIA:\n{ticket['acceptance_criteria']}"
    )
    prompt = template.replace("[PASTE REQUIREMENTS HERE]", requirements)
    prompt = prompt.replace("[FEATURE]", ticket["summary"] or ticket["key"])
    return prompt


def render_message(role: str, content: str) -> None:
    """Render a message in the chat pane and persist it to history."""
    st.session_state["messages"].append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)


def process_user_message(text: str, template_name: str) -> None:
    """Full pipeline: parse key -> fetch ticket -> prompt -> LLM -> render."""
    settings = config_store.load_settings()

    match = JIRA_KEY_PATTERN.search(text)
    if not match:
        render_message(
            "assistant",
            "I couldn't find a Jira ticket key in your message. "
            "Try something like: `create test cases for QA-102`",
        )
        return

    key = match.group(1)

    if not settings.get("JIRA_URL") or not settings.get("JIRA_EMAIL") \
            or not settings.get("JIRA_TOKEN"):
        render_message(
            "assistant",
            "Jira credentials are missing. Add JIRA_URL, JIRA_EMAIL and "
            "JIRA_TOKEN to the `.env` file (copy `.env.example`).",
        )
        return

    try:
        client = jira_client.JiraClient(
            settings["JIRA_URL"],
            settings["JIRA_EMAIL"],
            settings["JIRA_TOKEN"],
        )
        ticket = client.fetch_issue(key)
    except jira_client.JiraError as exc:
        render_message("assistant", f":red[**Jira error**] {exc}")
        return

    template = load_template(template_name)
    prompt = build_prompt(template, ticket)

    with st.spinner(
        f"Generating test cases for {key} "
        f"(provider: {settings['LLM_PROVIDER']})..."
    ):
        try:
            result, provider_used = llm_client.generate_test_cases(
                prompt, settings
            )
        except llm_client.LLMError as exc:
            render_message("assistant", f":red[**LLM error**] {exc}")
            return

    clean_result = llm_client.extract_markdown_table(result)
    render_message(
        "assistant",
        f"*Generated with {provider_used}*\n\n{clean_result}",
    )


# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------

st.set_page_config(
    page_title="Local Test Case Generator",
    page_icon="🧪",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state["messages"] = []


# ----------------------------------------------------------------------
# Layout: chat (left) + settings (right)
# ----------------------------------------------------------------------

chat_col, settings_col = st.columns([2, 1], gap="large")

# ---------------------------- Chat panel ------------------------------
with chat_col:
    st.title("🧪 Test Case Generator")

    template_names = list_templates()
    if template_names:
        selected_template = st.selectbox(
            "Test case template",
            template_names,
            key="template_select",
        )
    else:
        st.warning("No templates found in the Templates/ folder.")
        selected_template = None

    chat_box = st.container(border=True, height=560)
    with chat_box:
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    input_col, button_col = st.columns([5, 1])
    with input_col:
        user_text = st.text_input(
            "Message",
            placeholder="create test cases for QA-102",
            label_visibility="collapsed",
            key="chat_input",
        )
    with button_col:
        send = st.button("Send", type="primary", use_container_width=True)

    if send and user_text.strip():
        if selected_template is None:
            render_message(
                "assistant",
                "No template is available. Add a .md template to the "
                "Templates/ folder first.",
            )
        else:
            render_message("user", user_text.strip())
            process_user_message(user_text.strip(), selected_template)
        st.rerun()

# -------------------------- Settings panel ----------------------------
with settings_col:
    st.subheader("⚙️ Settings")

    settings = config_store.load_settings()

    st.markdown("**Jira**")
    st.text_input(
        "Jira URL", value=settings["JIRA_URL"], disabled=True, key="s_url"
    )
    st.text_input(
        "Jira Email", value=settings["JIRA_EMAIL"], disabled=True, key="s_email"
    )
    token = settings["JIRA_TOKEN"]
    st.text_input(
        "Jira Token",
        value="••••••••" if token else "(not set)",
        disabled=True,
        key="s_token",
    )

    st.markdown("**LLM**")
    provider_index = config_store.VALID_PROVIDERS.index(
        settings["LLM_PROVIDER"]
    ) if settings["LLM_PROVIDER"] in config_store.VALID_PROVIDERS else 0
    provider = st.selectbox(
        "Provider",
        config_store.VALID_PROVIDERS,
        index=provider_index,
        key="s_provider",
        help="auto = Ollama first, Groq fallback. ollama/groq = that provider only.",
    )

    if provider != settings["LLM_PROVIDER"]:
        config_store.save_provider(provider)
        st.success(f"Provider saved: {provider}")

    st.text_input(
        "Ollama URL", value=settings["OLLAMA_URL"], disabled=True, key="s_ollama_url"
    )
    st.text_input(
        "Ollama Model", value=settings["OLLAMA_MODEL"], disabled=True, key="s_ollama_model"
    )
    st.text_input(
        "Groq Model", value=settings["GROQ_MODEL"], disabled=True, key="s_groq_model"
    )
    groq_key = settings["GROQ_API_KEY"]
    st.text_input(
        "Groq API Key",
        value="••••••••" if groq_key else "(not set)",
        disabled=True,
        key="s_groq_key",
    )

    if not config_store.env_exists():
        st.warning(
            "No `.env` file found. Add one at the chapter root with your "
            "Jira and Groq credentials."
        )

    st.divider()
    st.markdown("**Connection tests**")

    if st.button("Test Jira connection", use_container_width=True):
        if not settings["JIRA_URL"] or not settings["JIRA_TOKEN"]:
            st.error("Set JIRA_URL and JIRA_TOKEN in .env first.")
        else:
            try:
                client = jira_client.JiraClient(
                    settings["JIRA_URL"],
                    settings["JIRA_EMAIL"],
                    settings["JIRA_TOKEN"],
                )
                client._get_json(
                    f"{settings['JIRA_URL'].rstrip('/')}/rest/api/3/myself"
                )
                st.success("Jira connection OK.")
            except jira_client.JiraError as exc:
                st.error(str(exc))

    if st.button("Test LLM connection", use_container_width=True):
        try:
            with st.spinner("Testing LLM..."):
                result, provider_used = llm_client.generate_test_cases(
                    "Reply with exactly: OK", settings
                )
            st.success(f"LLM OK via {provider_used}: {result[:80]}")
        except llm_client.LLMError as exc:
            st.error(str(exc))
