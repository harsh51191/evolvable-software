"""Foundations 3, 4, 6, 9 and 11: one door for every change.

People (the CLI), the AI drafter and the product's own scheduler all call `submit`. Every change
goes: propose -> policy decision -> checks -> release to a share of traffic -> measure ->
keep, revise or undo. The checks and the policy are kinds of change too, so they come through
the same door and improve the same way.
"""
import hashlib

from . import checks
from . import policy as policy_rules
from .desk import TRAFFIC, apply, good, resolve
from .kinds import KEY_RE, validate_body

ACTOR_TYPES = ("person", "ai", "product")


class DoorError(Exception):
    pass


def parse_actor(actor):
    actor_type, _, name = actor.partition(":")
    if actor_type not in ACTOR_TYPES or not name:
        raise DoorError("an actor is written type:name, with type one of %s" % ", ".join(ACTOR_TYPES))
    return actor_type, name


class Door:
    def __init__(self, store, kinds):
        self.store = store
        self.kinds = kinds

    def policy(self):
        return self.store.stable_view("policy")["main"]

    def views(self):
        return {kind: self.store.stable_view(kind) for kind in TRAFFIC}

    def _body(self, change_id):
        return self.store.get_change(change_id)["body"] if change_id else None

    def _get(self, change_id):
        change = self.store.get_change(change_id)
        if change is None:
            raise DoorError("no change %s" % change_id)
        return change

    # Propose ---------------------------------------------------------------------
    def submit(self, kind, key, body, actor, note="", provenance=None):
        actor_type, _ = parse_actor(actor)
        if kind not in self.kinds:
            raise DoorError("unknown kind of change '%s'; see kinds.json" % kind)
        single = self.kinds[kind].get("single_key")
        if not KEY_RE.match(key) or (single and key != single):
            raise DoorError("'%s' is not a valid key for %s" % (key, kind))
        change_id = self.store.insert_change(kind, key, body, actor_type, actor, note, provenance)
        self.store.event(change_id, actor, "proposed", {"note": note})
        return self._gate(change_id)

    def approve(self, change_id, approver, share=None):
        change = self._get(change_id)
        if parse_actor(approver)[0] != "person":
            raise DoorError("only a person can approve a change")
        if change["status"] != "awaiting_approval":
            raise DoorError("change %s is %s, not awaiting approval" % (change_id, change["status"]))
        self.store.event(change_id, approver, "approved")
        return self._gate(change_id, approver=approver, share=share)

    def _gate(self, change_id, approver=None, share=None):
        """Policy first, then checks, then release or wait for a person. Re-run in full on approval."""
        change = self.store.get_change(change_id)
        kind, key = change["kind"], change["key"]
        stable_id, candidate_id = self.store.live(kind, key)
        prev = self._body(stable_id)
        decision, reason = policy_rules.decide(
            self.policy(), kind, key, change["body"], prev, change["actor_type"], self._auto_today(kind))
        if decision == "blocked":
            self.store.update_change(change_id, status="blocked", decision=decision)
            self.store.event(change_id, "product:policy", "blocked", {"reason": reason})
            return self.store.get_change(change_id)
        errors, report = self.check(change, candidate_id)
        self.store.event(change_id, "product:checks", "checked", {"errors": errors, "report": report})
        if errors:
            self.store.update_change(change_id, status="rejected", decision=decision)
            return self.store.get_change(change_id)
        self.store.update_change(change_id, decision=decision)
        if decision == "pre_approved":
            self._release(change_id, "product:policy", None, reason)
        elif approver:
            self._release(change_id, approver, share, "approved by a person")
        else:
            self.store.update_change(change_id, status="awaiting_approval")
            self.store.event(change_id, "product:policy", "awaiting_approval", {"reason": reason})
        return self.store.get_change(change_id)

    # Check --------------------------------------------------------------------------
    def check(self, change, candidate_id):
        kind, key, body = change["kind"], change["key"], change["body"]
        errors = validate_body(self.kinds[kind], body)
        if candidate_id and candidate_id != change["id"]:
            errors.append("change %s to this definition is still being released; keep or undo it first" % candidate_id)
        if errors:
            return errors, None
        report = None
        if kind == "policy":
            if body is None:
                errors.append("the policy cannot be removed")
            else:
                errors += policy_rules.validate(body, self.policy(), list(self.kinds), self.track_record)
        elif kind == "checks" and body is not None:
            report = {"passes_now": checks.passes(body, self.views())}
        elif kind in TRAFFIC:
            cases = self.store.stable_view("checks")
            report = checks.run(cases, self.views(), kind, key, body)
            report["check_versions"] = [self.store.live("checks", k)[0] for k in sorted(cases)]
            if report["regressions"]:
                errors.append("the change breaks checks that pass today: %s" % ", ".join(report["regressions"]))
        return errors, report

    # Release -------------------------------------------------------------------------
    def _release(self, change_id, actor, share, reason):
        change = self.store.get_change(change_id)
        kind, key = change["kind"], change["key"]
        stable_id, _ = self.store.live(kind, key)
        rules = policy_rules.rules_for(self.policy(), kind)
        now = self.store.now()
        if kind in TRAFFIC:
            share = float(share if share is not None else rules.get("initial_share", 0.5))
            if not 0 < share <= 1:
                raise DoorError("share must be above 0 and at most 1")
            measure = self._traffic_plan(change, rules)
            self.store.update_change(change_id, status="live", share=share, replaces=stable_id, released_at=now, measure=measure)
            self.store.set_live(kind, key, stable_id, change_id)
        else:
            share, measure = 1.0, self._loop_plan(rules)
            self.store.update_change(change_id, status="kept", share=share, replaces=stable_id, released_at=now, measure=measure)
            self.store.set_live(kind, key, change_id, None)
        self.store.event(change_id, actor, "released", {"share": share, "reason": reason, "measure": measure})

    def _traffic_plan(self, change, rules):
        """Baseline from recorded questions this change would touch; target; window; tolerance."""
        kind, key = change["kind"], change["key"]
        before = self.views()
        after = dict(before, **{kind: apply(before[kind], key, change["body"])})
        outcomes = []
        for s in self.store.signals(limit=500):
            seen = set()
            for v in (before, after):
                r = resolve(s["question"], v["answers"], v["routing-rules"])
                seen.update([r["answer"], r["rule"]])
            if key in seen:
                outcomes.append(good(s, kind))
        window = rules.get("window", 8)
        outcomes = outcomes[-window:]
        baseline = round(sum(outcomes) / len(outcomes), 3) if len(outcomes) >= 3 else None
        target = round(min(1.0, baseline + rules.get("min_gain", 0.1)), 3) if baseline is not None else 0.5
        return {"name": self.kinds[kind]["measure"], "baseline": baseline, "target": target, "window": window,
                "tolerance": rules.get("tolerance", 0.15), "history": len(outcomes)}

    def _decided_traffic(self, after=None):
        rows = [c for kind in TRAFFIC for c in self.store.list_changes(kind)]
        rows = [c for c in rows if c["decision"] != "seed" and c["released_at"] is not None
                and c["status"] in ("kept", "undone") and (after is None or c["released_at"] > after)]
        return sorted(rows, key=lambda c: (c["released_at"], c["id"]))

    def _loop_plan(self, rules):
        """A change to the loop (checks, policy) is measured by how many later changes are kept."""
        window = rules.get("window", 5)
        last = self._decided_traffic()[-window:]
        baseline = round(sum(c["status"] == "kept" for c in last) / len(last), 3) if last else None
        return {"name": "changes_kept", "baseline": baseline, "target": baseline, "window": window,
                "tolerance": rules.get("tolerance", 0.2)}

    def promote(self, change_id, actor):
        change = self._get(change_id)
        if change["status"] != "live":
            raise DoorError("change %s is %s; only a live change can be kept" % (change_id, change["status"]))
        self.store.set_live(change["kind"], change["key"], change_id, None)
        self.store.update_change(change_id, status="kept", share=1.0)
        self.store.event(change_id, actor, "kept", {"share": 1.0})
        return self.store.get_change(change_id)

    # Measure -------------------------------------------------------------------------
    def evaluate(self, change_id):
        change = self._get(change_id)
        m = change["measure"]
        if not m:
            raise DoorError("change %s has not been released, so it has no measurement" % change_id)
        if change["kind"] in TRAFFIC:
            rows = self.store.exposure_rows(change_id)
            cand = [good(s, change["kind"]) for arm, s in rows if arm == "candidate"]
            ctrl = [good(s, change["kind"]) for arm, s in rows if arm == "control"]
            rate_c = round(sum(cand) / len(cand), 3) if cand else None
            rate_k = round(sum(ctrl) / len(ctrl), 3) if len(ctrl) >= max(3, m["window"] // 2) else None
            result = {"candidate_n": len(cand), "control_n": len(ctrl), "candidate_rate": rate_c, "control_rate": rate_k}
            if len(cand) < m["window"]:
                decision = "waiting"
            else:
                worse = (m["baseline"] is not None and rate_c < m["baseline"] - m["tolerance"]) or (
                    rate_k is not None and rate_c < rate_k - m["tolerance"])
                decision = "undo" if worse else "keep" if rate_c >= m["target"] else "revise"
        else:
            later = self._decided_traffic(after=change["released_at"])[: m["window"]]
            rate = round(sum(c["status"] == "kept" for c in later) / len(later), 3) if later else None
            result = {"later_changes": len(later), "kept_rate": rate}
            if len(later) < m["window"]:
                decision = "waiting"
            elif m["baseline"] is None or rate >= m["baseline"] - m["tolerance"]:
                decision = "keep"
            else:
                decision = "revise"
        result["decision"] = decision
        m["result"] = result
        self.store.update_change(change_id, measure=m)
        self.store.event(change_id, "product:measure", "measured", result)
        return result

    # Off switch and undo ---------------------------------------------------------------
    def switch_off(self, change_id, actor):
        change = self._get(change_id)
        if change["status"] != "live":
            raise DoorError("change %s is %s; only a live change can be switched off" % (change_id, change["status"]))
        self.store.update_change(change_id, status="off")
        self.store.event(change_id, actor, "switched_off")
        return self.store.get_change(change_id)

    def switch_on(self, change_id, actor):
        change = self._get(change_id)
        if parse_actor(actor)[0] != "person" or change["status"] != "off":
            raise DoorError("only a person can switch a change back on, and only one that is off")
        self.store.update_change(change_id, status="live")
        self.store.event(change_id, actor, "switched_on")
        return self.store.get_change(change_id)

    def undo(self, change_id, actor, reason="", event="undone"):
        change = self._get(change_id)
        kind, key = change["kind"], change["key"]
        if kind == "policy" and parse_actor(actor)[0] != "person":
            raise DoorError("only a person may undo a policy change")
        stable_id, candidate_id = self.store.live(kind, key)
        if candidate_id == change_id:
            self.store.set_live(kind, key, stable_id, None)
        elif stable_id == change_id:
            if candidate_id:
                raise DoorError("undo change %s, which is being released, first" % candidate_id)
            if kind == "policy" and change["replaces"] is None:
                raise DoorError("the first policy cannot be undone")
            self.store.set_live(kind, key, change["replaces"], None)
        else:
            raise DoorError("change %s is not the current version; undo goes one step at a time" % change_id)
        self.store.update_change(change_id, status="undone")
        self.store.event(change_id, actor, event, {"reason": reason, "restored": change["replaces"] if stable_id == change_id else stable_id})
        return self.store.get_change(change_id)

    # Records used by the policy and the scheduler -------------------------------------------
    def track_record(self, kind):
        rows = [c for c in self.store.list_changes(kind) if c["decision"] != "seed" and c["released_at"] is not None
                and c["status"] in ("kept", "undone")][-20:]
        return {"kept": sum(c["status"] == "kept" for c in rows), "undone": sum(c["status"] == "undone" for c in rows)}

    def _auto_today(self, kind):
        since = self.store.now() - 86400
        return sum(1 for c in self.store.list_changes(kind) if c["decision"] == "pre_approved" and c["created_at"] >= since)

    def propose_check(self, question, expect, actor, note, provenance):
        """Turn a failure into a check case, through the same door as any other change."""
        key = "case-" + hashlib.sha1(question.lower().encode()).hexdigest()[:8]
        if any(c["status"] not in ("blocked", "rejected") for c in self.store.list_changes("checks", key)):
            return None
        return self.submit("checks", key, {"question": question, "expect": expect}, actor, note, provenance)
