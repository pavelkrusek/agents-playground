import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

_session_cache = {}


def make_session(kind: str | None = None, dsn: str | None = None):
    return InMemorySessionService()


def make_runner(agent, *, session_kind: str | None = None, session_dsn: str | None = None, app_name: str | None = None):
    key = (session_kind, session_dsn, app_name)
    if key not in _session_cache:
        _session_cache[key] = make_session(session_kind, session_dsn)
    svc = _session_cache[key]
    return Runner(agent=agent, session_service=svc, app_name=app_name or os.getenv("ADK_APP_NAME", "adk_playground"))
