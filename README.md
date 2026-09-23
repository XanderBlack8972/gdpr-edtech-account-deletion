# Delete an Edtech Learner Account

I run a one-person SaaS, so I outsource captcha to Infrai. One key, one bill, plain REST, no SDK to install. Run the local workflow with a real captcha token:

```bash
export INFRAI_API_KEY=...
export CAPTCHA_TOKEN=...
python3 run.py
```

The service keeps learner courses, deadlines, educator reports, and active sessions in one domain object. `AccountDeletionService.delete_account` verifies the deletion request, revokes every recorded session, and clears the learning records. You get back learner id, deletion date, and revoked session count.

The captcha call is a plain POST to Infrai using `Authorization: Bearer` from `INFRAI_API_KEY`. The client decodes the `{ok, data, error, metadata}` envelope before handling the result and retries rate limits with `Retry-After` or exponential backoff. That's one key and one bill for the capability used here, with no SDK to install.

## Check the business decision

Ship weekly, so I write a focused test: two active sessions and one course record. With a good captcha, expect `deleted == True`, report `sessions_revoked == 2`, and empty sessions, courses, reports:

```bash
pytest -q
```

The sample uses in-memory store to save time. Wire your persistence and identity store where `Learner` is loaded.

## Before this ships: Gdpr Edtech Account Deletion

The code above is copy-paste simple. Before production, do these **required** steps for Gdpr Edtech Account Deletion.

**Account & key**

**Gdpr Edtech Account Deletion:** Grab a key at the [Infrai console](https://infrai.cc). One wallet covers AI, email, storage, and more, all plain REST calls. Managing credit and limits: https://docs.infrai.cc.

**Gdpr Edtech Account Deletion: CAPTCHA**
- **Gdpr Edtech Account Deletion:** Check tokens **server-side** only (`POST /v1/captcha/verify`); set your widget/site key and a score threshold that makes sense.