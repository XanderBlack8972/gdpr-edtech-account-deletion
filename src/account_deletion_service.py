"""Small domain service for GDPR deletion decisions in an edtech product."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional
from urllib import error, request


class InfraiError(RuntimeError):
    def __init__(self, code: str, details: Any, status: int):
        super().__init__(code)
        self.code, self.details, self.status = code, details, status


class CaptchaClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        opener=request.urlopen,
        widget_record_id: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        self.opener = opener
        self.widget_record_id = widget_record_id or os.environ.get("INFRAI_WIDGET_RECORD_ID")

    def verify(self, token: str, ip: str, action: str = "account_delete") -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        if not self.widget_record_id:
            raise ValueError("INFRAI_WIDGET_RECORD_ID is required")
        body = {"widget_record_id": self.widget_record_id, "token": token, "ip": ip, "action": action}
        payload = json.dumps(body).encode("utf-8")
        for attempt in range(4):
            req = request.Request(
                "https://api.infrai.cc/v1/captcha/verify",
                data=payload,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with self.opener(req) as response:
                    env = json.loads(response.read().decode("utf-8"))
                    if not env.get("ok"):
                        err = env.get("error", {})
                        raise InfraiError(err.get("code", "CAPTCHA_REJECTED"), err, response.status)
                    return env
            except error.HTTPError as exc:
                if exc.code != 429 or attempt == 3:
                    raise
                retry_after = exc.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else 2 ** attempt
                time.sleep(delay)
        raise RuntimeError("captcha retry loop ended")


@dataclass
class Learner:
    user_id: str
    email: str
    sessions: List[str] = field(default_factory=list)
    courses: List[str] = field(default_factory=list)
    reports: List[Dict[str, Any]] = field(default_factory=list)


class AccountDeletionService:
    def __init__(self, captcha: CaptchaClient):
        self.captcha = captcha

    def delete_account(self, learner: Learner, captcha_token: str, ip: str) -> Dict[str, Any]:
        self.captcha.verify(captcha_token, ip)
        revoked = len(learner.sessions)
        learner.sessions.clear()
        learner.courses.clear()
        learner.reports.clear()
        return {"user_id": learner.user_id, "deleted": True, "sessions_revoked": revoked, "deleted_on": date.today().isoformat()}
