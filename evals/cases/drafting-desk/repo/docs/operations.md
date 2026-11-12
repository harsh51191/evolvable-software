# Operations

**Scaling.** Web instances keep no state of their own; everything is in PostgreSQL, so several can run behind a load balancer. Run one drafting worker: two workers have not been tried.

**Known limits.** After the June 2026 incident (one organisation with 2,000 rules made `/ask` slow for everyone), each organisation is capped at 500 rules and 1,000 answers (`desk/checks.py`). No other limit has been measured.

**Monitoring.** An external uptime monitor calls `/health` every minute and pages on-call after three failures. There are no other metrics or alerts.

**Backups.** `python deskctl.py backup /backups` runs `pg_dump`. To restore, run `pg_restore` into an empty database by hand. A restore has not been rehearsed.

**When the model is down.** Drafting jobs fail and are retried up to three times. Answering and routing do not use the model and keep working.
