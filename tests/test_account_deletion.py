from src.account_deletion_service import AccountDeletionService, Learner


class PassingCaptcha:
    def verify(self, token, ip):
        return {"ok": True, "data": {"passed": True}}


def test_deletion_revokes_sessions_and_clears_learning_records():
    learner = Learner("u-7", "learner@example.edu", ["s1", "s2"], ["course-1"], [{"deadline": "2026-09-30"}])
    result = AccountDeletionService(PassingCaptcha()).delete_account(learner, "captcha-token", "192.0.2.4")
    assert result["deleted"] is True
    assert result["sessions_revoked"] == 2
    assert learner.sessions == []
    assert learner.courses == []
    assert learner.reports == []
