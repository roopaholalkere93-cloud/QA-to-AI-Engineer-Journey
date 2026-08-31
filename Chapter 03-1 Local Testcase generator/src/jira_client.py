"""Jira Cloud REST API client (API v3).

Fetches a single ticket and normalises it into a small dict:
    {key, summary, description, acceptance_criteria}

Uses Basic auth with the account email + API token. Errors are raised
as JiraError with a message safe to show in the chat pane.
"""

import base64
import re

import requests


class JiraError(Exception):
    """Raised for any Jira request failure, with a user-safe message."""


class JiraClient:
    """Thin wrapper around the Jira Cloud REST API v3."""

    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        credentials = base64.b64encode(f"{email}:{api_token}".encode()).decode()
        self._session.headers.update(
            {
                "Authorization": f"Basic {credentials}",
                "Accept": "application/json",
            }
        )
        self._fields_cache = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fetch_issue(self, key: str) -> dict:
        """Return normalised ticket data for the given issue key."""
        url = f"{self.base_url}/rest/api/3/issue/{key}"
        data = self._get_json(url)
        fields = data.get("fields", {})

        summary = fields.get("summary", "") or ""
        description = self._adf_to_text(fields.get("description"))
        acceptance = self._extract_acceptance_criteria(fields, description)

        return {
            "key": data.get("key", key),
            "summary": summary,
            "description": description,
            "acceptance_criteria": acceptance,
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _get_json(self, url: str) -> dict:
        try:
            response = self._session.get(url, timeout=30)
        except requests.RequestException as exc:
            raise JiraError(
                f"Could not reach Jira at {self.base_url}. "
                f"Check the URL and your network connection."
            ) from exc

        if response.status_code == 401:
            raise JiraError(
                "Jira rejected the credentials (HTTP 401). "
                "Check JIRA_EMAIL and JIRA_TOKEN in .env."
            )
        if response.status_code == 403:
            raise JiraError(
                "Jira denied access (HTTP 403). "
                "The account may not have permission to view this issue."
            )
        if response.status_code == 404:
            raise JiraError(
                "Jira returned HTTP 404 - the issue key does not exist "
                "or is not visible to this account."
            )
        if response.status_code >= 400:
            raise JiraError(
                f"Jira request failed with HTTP {response.status_code}."
            )

        return response.json()

    def _fields(self) -> dict:
        """Map of field id -> name, cached after the first call."""
        if self._fields_cache is None:
            self._fields_cache = {
                item.get("id"): item.get("name", "")
                for item in self._get_json(f"{self.base_url}/rest/api/3/field")
            }
        return self._fields_cache

    def _extract_acceptance_criteria(self, fields: dict, description: str) -> str:
        """Look for an Acceptance Criteria field, then fall back to a
        section of that name parsed from the description."""
        try:
            names = self._fields()
            for field_id, field_name in names.items():
                if "acceptance" in field_name.lower() and field_id in fields:
                    value = fields[field_id]
                    if isinstance(value, list):
                        parts = [
                            self._adf_to_text(item.get("value"))
                            for item in value
                        ]
                        text = "\n".join(p for p in parts if p)
                    else:
                        text = self._adf_to_text(value)
                    if text.strip():
                        return text.strip()
        except JiraError:
            pass  # field metadata fetch failed - fall through to description

        match = re.search(
            r"(?i)(acceptance\s*criteria)\s*(.*?)(?=\n\s*[A-Z][A-Za-z\s]{3,}:|\Z)",
            description,
            re.DOTALL,
        )
        if match:
            section = match.group(2).strip()
            if section:
                return section

        return "Not specified"

    @staticmethod
    def _adf_to_text(value) -> str:
        """Convert an Atlassian Document Format payload into plain text."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value

        paragraphs = []

        def walk(node):
            node_type = node.get("type")
            content = node.get("content", [])
            text = "".join(child.get("text", "") for child in content
                           if child.get("type") == "text")

            if node_type == "paragraph":
                if text.strip():
                    paragraphs.append(text)
            elif node_type == "heading":
                paragraphs.append(f"**{text}**")
            elif node_type in ("bulletList", "orderedList"):
                for item in content:
                    walk(item)
            elif node_type == "listItem":
                inner = " ".join(
                    child.get("text", "")
                    for child in content
                    if child.get("type") == "text"
                )
                if inner.strip():
                    paragraphs.append(f"- {inner}")
            elif node_type in ("codeBlock", "blockquote"):
                if text.strip():
                    paragraphs.append(text)

            for child in content:
                if child.get("type") != "text":
                    walk(child)

        if isinstance(value, dict):
            walk(value)

        return "\n".join(paragraphs).strip()
