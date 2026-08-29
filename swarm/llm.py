"""Optional chat backend. Offline heuristic path is the default."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from swarm.config import Settings, load_settings


class LLMError(RuntimeError):
    pass


def complete(prompt: str, *, system: str = "", temperature: float = 0.4, settings: Settings | None = None) -> str:
    settings = settings or load_settings()
    if settings.xai_api_key:
        return _openai_compat(
            url=f"{settings.xai_base_url.rstrip('/')}/chat/completions",
            key=settings.xai_api_key,
            model=settings.xai_model,
            prompt=prompt,
            system=system,
            temperature=temperature,
        )
    if settings.openai_api_key:
        base = settings.openai_base_url or "https://api.openai.com/v1"
        return _openai_compat(
            url=f"{base.rstrip('/')}/chat/completions",
            key=settings.openai_api_key,
            model=settings.openai_model,
            prompt=prompt,
            system=system,
            temperature=temperature,
        )
    raise LLMError("No XAI_API_KEY or OPENAI_API_KEY set; use the offline heuristic path.")


def _openai_compat(*, url: str, key: str, model: str, prompt: str, system: str, temperature: float) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = json.dumps(
        {"model": model, "messages": messages, "temperature": temperature}
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        raise LLMError(str(exc)) from exc
    return payload["choices"][0]["message"]["content"]
