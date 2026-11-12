"""The product's own scheduler: measures, keeps, reverses, learns from failures, and tightens.

Run it with `tick`. It acts as `product:scheduler` and goes through the same door as everyone else.
Safety actions (measuring, reversing a change that made things worse, lowering autonomy) are
always allowed. Starting new changes depends on the dial: at 3 the product turns recorded failures
into proposed checks; at 5 it also chooses unmet questions to answer and drafts them itself.
"""
from . import policy as policy_rules
from .desk import TRAFFIC, good, resolve

ACTOR = "product:scheduler"


def tick(app):
    door, store = app.door, app.store
    actions = []
    for kind in TRAFFIC:
        for change in store.candidates(kind):
            result = door.evaluate(change["id"])
            if result["decision"] == "undo":
                door.undo(change["id"], ACTOR, "its measure got worse", event="auto_reversed")
                actions.append({"action": "reversed", "change": change["id"], "result": result})
                actions.extend(_after_reversal(app, change))
            elif result["decision"] == "keep" and policy_rules.dial(door.policy(), kind) >= 3:
                door.promote(change["id"], ACTOR)
                actions.append({"action": "kept", "change": change["id"], "result": result})
            elif result["decision"] != "waiting":
                actions.append({"action": "needs_review", "change": change["id"], "result": result})

    for kind in ("checks", "policy"):
        for change in store.list_changes(kind):
            m = change["measure"]
            if change["status"] == "kept" and m and m.get("result", {}).get("decision", "waiting") == "waiting":
                result = door.evaluate(change["id"])
                if result["decision"] != "waiting":
                    actions.append({"action": "measured", "change": change["id"], "result": result})

    # Failures that a person flagged with the outcome they expected become proposed checks.
    for s in store.signals():
        if s["expected"] and s["check_change"] is None:
            proposed = door.propose_check(s["question"], s["expected"], ACTOR, "flagged failure",
                                          {"signal": s["id"]})
            if proposed:
                store.link_check(s["id"], proposed["id"])
                actions.append({"action": "proposed_check", "change": proposed["id"], "status": proposed["status"]})

    # Self-chosen work: only when the answers dial is at 5.
    pol = door.policy()
    if policy_rules.dial(pol, "answers") >= 5:
        drafted = {(c["provenance"] or {}).get("question") for c in store.list_changes("answers")}
        for question, count in app.desk.unmet():
            if count >= pol["min_unmet"] and question not in drafted:
                result = app.draft(question, actor=ACTOR)
                actions.append({"action": "drafted", "question": question, "status": result.get("status")})
    return actions


def _after_reversal(app, change):
    """A reversed change passed every check, so the checks missed something: record it and add one."""
    door, store = app.door, app.store
    actions = []
    checked = [e for e in store.events(change["id"]) if e["event"] == "checked"]
    versions = (checked[-1]["detail"]["report"] or {}).get("check_versions", []) if checked else []
    store.event(change["id"], ACTOR, "wrong_pass", {"checks_that_passed_it": versions})
    bad = [s for arm, s in store.exposure_rows(change["id"]) if arm == "candidate" and not good(s, change["kind"])]
    if bad:
        views = door.views()
        r = resolve(bad[0]["question"], views["answers"], views["routing-rules"])
        expect = {"answer": r["answer"]} if r["answer"] else {"answer": None, "team": r["team"]}
        proposed = door.propose_check(bad[0]["question"], expect, ACTOR, "change %s was reversed" % change["id"],
                                      {"reversed_change": change["id"], "signal": bad[0]["id"]})
        if proposed:
            actions.append({"action": "proposed_check", "change": proposed["id"], "status": proposed["status"]})

    # Losing autonomy is automatic and scoped to the kind of change that went wrong.
    pol_change_id = store.live("policy", "main")[0]
    since = store.get_change(pol_change_id)["released_at"] or 0
    reversed_auto = [c for c in store.list_changes(change["kind"]) if c["decision"] == "pre_approved"
                     and any(e["event"] == "auto_reversed" and e["at"] >= since for e in store.events(c["id"]))]
    pol = door.policy()
    level = policy_rules.dial(pol, change["kind"])
    if level >= 4 and len(reversed_auto) >= pol["demote_after_reversals"]:
        lowered = {**pol, "kinds": {**pol["kinds"], change["kind"]: {**pol["kinds"][change["kind"]], "dial": level - 1}}}
        result = door.submit("policy", "main", lowered, ACTOR, "%d automatic reversals of %s" % (len(reversed_auto), change["kind"]),
                             {"reversed": [c["id"] for c in reversed_auto]})
        actions.append({"action": "lowered_dial", "kind": change["kind"], "to": level - 1, "change": result["id"],
                        "status": result["status"]})
    return actions
