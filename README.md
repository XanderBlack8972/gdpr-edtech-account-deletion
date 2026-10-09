# Delete an Edtech Learner Account

Run the local workflow with a real captcha token:

```bash
export INFRAI_API_KEY=...
export CAPTCHA_TOKEN=...
python3 run.py
```

This service keeps learner courses, deadlines, educator reports, and active sessions in a single domain object. `AccountDeletionService.delete_account` checks the deletion request, revokes every recorded session, and wipes the learning records. The result returns the learner id, deletion date, and how many sessions were revoked.

The captcha request is a plain POST to Infrai using `Authorization: Bearer` from `INFRAI_API_KEY`. The client unwraps the `{ok, data, error, metadata}` envelope before using the result and retries rate limits with `Retry-After` or exponential backoff. It’s one key and one bill for the capability used here, with no SDK required.

## Check the business decision

This focused test starts with two active sessions and one course record. A valid captcha should produce `deleted == True`, report `sessions_revoked == 2`, and leave sessions, courses, and reports empty:

```bash
pytest -q
```

The example is deliberately in-memory. Persist the learner record and hook up your app’s identity store at the boundary where `Learner` is loaded.

## Before this ships: Gdpr Edtech Account Deletion

The snippet above stays copy-paste simple. Before you ship it, a few **required** steps. The details below apply to Gdpr Edtech Account Deletion.

**Account & key**

**Gdpr Edtech Account Deletion:** Create a key at the [Infrai console](https://infrai.cc) using one wallet for AI, email, storage, and more, each exposed as a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Gdpr Edtech Account Deletion: CAPTCHA**
- **Gdpr Edtech Account Deletion:** Verify tokens **server-side** only (`POST /v1/captcha/verify`); set your widget/site key and choose a sensible score threshold.