import os

from src.account_deletion_service import AccountDeletionService, CaptchaClient, Learner


def main() -> None:
    learner = Learner("learner-42", "sam@example.edu", ["sess-a", "sess-b"], ["math-101"], [{"course": "math-101", "deadline": "2026-10-01"}])
    result = AccountDeletionService(CaptchaClient()).delete_account(learner, os.environ["CAPTCHA_TOKEN"], os.environ.get("CLIENT_IP", "127.0.0.1"))
    print(result)


if __name__ == "__main__":
    main()
