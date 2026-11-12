"""Foundations 8 and 12: written limits, enforced in code, and an autonomy dial per kind of change.

The model never decides whether its own change may ship. `decide` does, from the current policy
definition, which is itself versioned data that changes through the same door.
"""
import copy

DIAL_NAMES = ["Engineers only", "Self-serve", "Drafted", "Carried", "Pre-approved", "Self-chosen"]
# The lowest dial at which each kind of actor may propose a change at all.
MIN_DIAL_TO_PROPOSE = {"person": 1, "ai": 2, "product": 3}
# Invariant held in code, not in the editable policy: the policy itself never ships without a
# person, except a change that only lowers dials (tightening), which the product may make.
POLICY_MAX_DIAL = 3


def rules_for(policy, kind):
    return policy["kinds"].get(kind, {"dial": 1})


def dial(policy, kind):
    return rules_for(policy, kind).get("dial", 1)


def is_tightening(old, new):
    """True when `new` only lowers one or more dials and changes nothing else."""
    if old is None or new is None or set(old["kinds"]) != set(new["kinds"]):
        return False
    lowered = False
    a, b = copy.deepcopy(old), copy.deepcopy(new)
    for kind in old["kinds"]:
        d_old, d_new = a["kinds"][kind].pop("dial", 1), b["kinds"][kind].pop("dial", 1)
        if d_new > d_old:
            return False
        lowered = lowered or d_new < d_old
    return lowered and a == b


def decide(policy, kind, key, body, prev_body, actor_type, auto_today):
    """Return (decision, reason). decision is 'blocked', 'needs_person' or 'pre_approved'."""
    if kind == "policy" and actor_type == "product" and is_tightening(prev_body, body):
        return "pre_approved", "the change only lowers autonomy"
    rules = rules_for(policy, kind)
    level = rules.get("dial", 1)
    needed = MIN_DIAL_TO_PROPOSE[actor_type]
    if level < needed:
        return "blocked", "the %s dial is %d (%s); changes by %s need %d or more" % (
            kind, level, DIAL_NAMES[level], actor_type, needed)
    if actor_type == "person":
        return "needs_person", "a person releases people's changes"
    if body is None:
        return "blocked", "AI and the product may not remove definitions"
    if key in rules.get("protected_keys", []):
        return "blocked", "'%s' is protected: only people may change it" % key
    if kind == "checks" and prev_body is not None:
        return "blocked", "AI and the product may add checks, never change or remove them"
    if kind == "policy" or level < 4:
        return "needs_person", "the %s dial is %d (%s): a person approves each release" % (kind, level, DIAL_NAMES[level])
    if auto_today >= rules.get("max_auto_per_day", 0):
        return "blocked", "the limit of %d %s changes a day without a person is reached" % (
            rules.get("max_auto_per_day", 0), kind)
    return "pre_approved", "the %s dial is %d (%s) and the change is within its limits" % (kind, level, DIAL_NAMES[level])


def validate(new, old, kind_names, track_record):
    """Check a proposed policy. Raising a dial needs a measured record (foundation 12)."""
    errors = []
    missing = sorted(set(kind_names) - set(new["kinds"]))
    if missing:
        errors.append("the policy must cover every kind of change; missing: %s" % ", ".join(missing))
    raise_rule = old["raise_rule"]  # the rule in force decides, so it cannot be loosened and used at once
    for kind, rules in sorted(new["kinds"].items()):
        if kind not in kind_names:
            errors.append("unknown kind of change '%s'" % kind)
            continue
        level = rules.get("dial")
        if not isinstance(level, int) or not 0 <= level <= 5:
            errors.append("%s: dial must be 0 to 5" % kind)
            continue
        if kind == "policy" and level > POLICY_MAX_DIAL:
            errors.append("policy: the policy itself can never ship without a person (dial at most %d)" % POLICY_MAX_DIAL)
        share = rules.get("initial_share", 1.0)
        if not isinstance(share, (int, float)) or not 0 < share <= 1:
            errors.append("%s: initial_share must be above 0 and at most 1" % kind)
        old_level = dial(old, kind)
        if level > old_level:
            if level - old_level > 1:
                errors.append("%s: raise the dial one step at a time (%d to %d)" % (kind, old_level, level))
            record = track_record(kind)
            decided = record["kept"] + record["undone"]
            rate = record["undone"] / decided if decided else 0.0
            if record["kept"] < raise_rule["min_kept"] or rate > raise_rule["max_reversal_rate"]:
                errors.append(
                    "%s: raising the dial needs %d kept changes and at most %d%% undone; the record shows %d kept, %d undone"
                    % (kind, raise_rule["min_kept"], round(raise_rule["max_reversal_rate"] * 100), record["kept"], record["undone"]))
    return errors
