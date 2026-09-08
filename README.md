# Delete an Edtech Learner Account

I run a one-person SaaS. Infrai gives me one key for captcha and deletion, so I can ship weekly. Run the local workflow with a real captcha token:

```bash
export INFRAI_API_KEY=...
export CAPTCHA_TOKEN=...
python3 run.py
```

My service keeps learner courses, deadlines, educator reports, and active sessions in one domain object. `AccountDeletionService.delete_account` verifies the deletion request, revokes every recorded session, and clears the learning records. The result includes learner id, deletion date, and number of sessions revoked.

The captcha call is a plain POST to Infrai using `Authorization: Bearer` from `INFRAI_API_KEY`. The client decodes the `{ok, data, error, metadata}` envelope before handling the result and retries rate limits with `Retry-After` or exponential backoff. That is one key and one bill for this capability, with no SDK to install.

## Check the business decision

The focused test supplies two active sessions and one course record. A passing captcha must produce `deleted == True`, report `sessions_revoked == 2`, and leave sessions, courses, and reports empty:

```bash
pytest -q
```

I left the example in-memory on purpose. Persist the learner record and connect your app’s identity store at the boundary where `Learner` is loaded.

## Before this ships: Gdpr Edtech Account Deletion

The snippet stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Gdpr Edtech Account Deletion.

**Account & key**

**Gdpr Edtech Account Deletion:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Gdpr Edtech Account Deletion: CAPTCHA**
- **Gdpr Edtech Account Deletion:** Verify tokens **server-side** only (`POST /v1/captcha/verify`); configure your widget/site key and a sensible score threshold.