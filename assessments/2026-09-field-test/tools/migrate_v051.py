#!/usr/bin/env python3
"""One-off: add the v0.5.1 scheduled-work surface to the ARC-09 inventories.

Only the four products with an ARC-09 inventory need it (an inventory is required at 3 or more).
Evidence read at the same tips as the rest of the field test. Provisional, single rater.
The script refuses to run twice.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ["frappe", "directus", "discourse", "posthog", "n8n", "dify", "librechat",
           "hermes-agent", "openclaw", "opencode", "openhands"]

SCHEDULES = {
 "discourse": (2, " Scheduled work: restore pauses Sidekiq, clears its queues and limits email to staff "
               "(lib/backup_restore/restorer.rb:55-59, 132-135), and topic timers re-check the scheduling "
               "user's current permissions when they run (app/jobs/regular/close_topic.rb:14, "
               "publish_topic_to_category.rb:7-13). No view lists upcoming timers and the user each runs as, "
               "so scheduled work stays at 2 and the criterion reads 2."),
 "frappe": (2, " Scheduled work: scheduled job records and server-script scheduler events restore with the "
            "database and resume with the scheduler; no check of each job's identity, permissions or "
            "credentials before it runs was found (frappe/utils/scheduler.py), so scheduled work is 2."),
 "hermes-agent": (3, " Scheduled work: cron/jobs.json is in every backup and jobs lost during an update are "
                  "restored automatically (hermes_cli/backup.py:1059, 1600-1665); hermes cron list shows each "
                  "job's next run (hermes_cli/cron.py:125); jobs run under their own profile (cron/jobs.py:64-68); "
                  "a pre-run check, on by default, blocks and alerts on jobs whose provider key, delivery "
                  "target or skills no longer resolve (cron/scheduler_preflight.py:80-90, 387), with tests "
                  "(tests/cron/test_preflight_credential_verdict_names_home.py)."),
 "openclaw": (3, " Scheduled work: cron jobs live in the state database the backup covers; openclaw cron list "
              "shows each job's next run and agent (src/cli/cron-cli/shared.ts:498-503); jobs keep their owner "
              "and grant generation, and scheduled runs require account provenance to match the persisted owner, "
              "so jobs whose owner no longer resolves do not run (src/cron/scheduled-tool-policy.test.ts:44, "
              "service.unresolved-owner.test.ts, service.grant-generation.test.ts); interrupted recurring jobs "
              "are marked failed rather than replayed after a restart (service.restart-catchup.test.ts:168)."),
}


def migrate(system):
    path = os.path.join(ROOT, system, "assessment.json")
    with open(path) as handle:
        data = json.load(handle)
    if data.get("framework_version") == "0.5.1":
        sys.exit(f"{system}: already migrated")
    if system in SCHEDULES:
        level, note = SCHEDULES[system]
        entry = data["scores"]["ARC-09"]
        entry["inventory"]["schedules"] = level
        entry["evidence"] += note
        floor = min(v for v in entry["inventory"].values() if isinstance(v, int))
        entry["score"] = min(entry["score"], floor)
    data["framework_version"] = "0.5.1"
    with open(path, "w") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


if __name__ == "__main__":
    for system in SYSTEMS:
        migrate(system)
    print("migrated", len(SYSTEMS), "systems")
