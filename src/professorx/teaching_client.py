"""Public no-login, student-side client for ProfessorX limited teaching plans.

The original policy and instructor's Drive credentials remain server-side.
A public gateway URL is NOT an authentication secret. Anyone who knows it can
request approved plan fields; no student identity is collected by ProfessorX.
"""
from __future__ import annotations

import os
import time
from urllib.parse import urlsplit

import httpx

SUBJECTS = frozenset({"ESD", "PAD", "SES", "RTES"})
MODES = frozenset({"LEARN", "EXAM", "SOLVE", "COMPARE", "QUIZ", "REVISION", "PREVIOUS_PAPER"})
_PLAN_CACHE: dict[tuple[str, str], tuple[float, dict]] = {}


def _endpoint() -> str:
    url = os.environ.get("PROFESSORX_APPS_SCRIPT_URL", "").strip()
    parsed = urlsplit(url)
    parts = parsed.path.split("/")
    if (parsed.scheme != "https" or parsed.hostname != "script.google.com"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None or parsed.query or parsed.fragment
            or len(parts) != 5 or parts[:3] != ["", "macros", "s"]
            or not parts[3] or parts[4] != "exec"):
        raise RuntimeError("PROFESSORX_APPS_SCRIPT_URL must be an HTTPS script.google.com/macros/s/.../exec URL")
    return url


def request_teaching_plan(subject: str, mode: str = "LEARN", force_refresh: bool = False) -> dict:
    subject = subject.strip().upper()
    mode = mode.strip().upper()
    if subject not in SUBJECTS or mode not in MODES:
        raise ValueError("Subject must be ESD/PAD/SES/RTES; mode must be a supported study mode")
    cache_key = (subject, mode)
    now = time.monotonic()
    if not force_refresh and cache_key in _PLAN_CACHE:
        expires_at, cached = _PLAN_CACHE[cache_key]
        if now < expires_at:
            return cached

    payload = {"action": "teaching_plan", "subject": subject, "mode": mode}
    # Apps Script ContentService redirects responses to a Google content host.
    # Follow redirect with GET only and only to the known Google host.
    with httpx.Client(timeout=20, follow_redirects=False) as client:
        response = client.post(_endpoint(), json=payload, headers={"Content-Type": "application/json"})
        if response.status_code in (301, 302, 303):
            redirect = response.headers.get("location", "")
            parsed = urlsplit(redirect)
            if (parsed.scheme != "https" or parsed.hostname != "script.googleusercontent.com"
                    or parsed.username or parsed.password):
                raise RuntimeError("Unexpected redirect from the ProfessorX teaching gateway")
            response = client.get(redirect)
        elif response.status_code in (307, 308):
            raise RuntimeError("Unsafe redirect from the ProfessorX teaching gateway")
        response.raise_for_status()
        result = response.json()
    if not isinstance(result, dict) or result.get("ok") is not True:
        code = result.get("error", "UNKNOWN_ERROR") if isinstance(result, dict) else "BAD_RESPONSE"
        raise RuntimeError("ProfessorX teaching gateway rejected the request: " + str(code))
    if (result.get("subject") != subject or result.get("mode") != mode
            or not isinstance(result.get("plan"), dict)):
        raise RuntimeError("Unexpected teaching-plan response")
    # Defensive client-side allowlist: ignore any unexpected gateway fields.
    plan = result["plan"]
    allowed = {}
    for key in ("sections", "checks", "source_guidance", "interaction"):
        values = plan.get(key, [])
        if not isinstance(values, list) or len(values) > 12 or any(
            not isinstance(v, str) or len(v) > 260 for v in values
        ):
            raise RuntimeError("Unexpected teaching-plan field: " + key)
        allowed[key] = values
    ttl = min(max(int(result.get("cache_seconds", 900)), 0), 900)
    limited = {"ok": True, "subject": subject, "mode": mode,
               "cache_seconds": ttl, "plan": allowed}
    _PLAN_CACHE[cache_key] = (time.monotonic() + ttl, limited)
    return limited
