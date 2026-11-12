"""Foundation 10: the product describes itself in a machine-readable way.

OPERATIONS is the single definition of what can be done to Answer Desk. The command-line parser is
generated from it, and `describe` prints it with the kinds of change, the policy and the current
dial, so an agent can discover what it may do without reading the code.
"""
from . import policy as policy_rules

# Each argument: [name, {"type": "str"|"int"|"float"|"json"|"flag", "required": bool, "help": ...}]
OPERATIONS = [
    {"name": "init", "changes": True, "help": "Create the store and load the starting definitions", "args": []},
    {"name": "ask", "changes": False, "help": "Ask the desk a question; records a signal", "args": [
        ["question", {"type": "str", "help": "the customer's question"}],
        ["--session", {"type": "str", "help": "an opaque session id; stored only as a hash"}]]},
    {"name": "feedback", "changes": False, "help": "Record whether an answer helped", "args": [
        ["signal", {"type": "int"}], ["--unhelpful", {"type": "flag"}],
        ["--expected-answer", {"type": "str", "help": "staff only: the answer key it should have had"}],
        ["--expected-team", {"type": "str", "help": "staff only: the team it should have gone to"}]]},
    {"name": "signals", "changes": False, "help": "List recorded questions, or the unmet ones", "args": [
        ["--unmet", {"type": "flag"}]]},
    {"name": "propose", "changes": True, "help": "A person proposes a change through the door", "args": [
        ["kind", {"type": "str"}], ["key", {"type": "str"}],
        ["--body", {"type": "json", "help": "the new definition as JSON"}], ["--remove", {"type": "flag"}],
        ["--as", {"type": "str", "required": True, "help": "person:NAME"}], ["--note", {"type": "str"}]]},
    {"name": "draft", "changes": True, "help": "The AI drafter drafts an answer and sends it through the door", "args": [
        ["question", {"type": "str"}]]},
    {"name": "approve", "changes": True, "help": "A person approves a change; checks and policy run again", "args": [
        ["change", {"type": "int"}], ["--as", {"type": "str", "required": True}], ["--share", {"type": "float"}]]},
    {"name": "keep", "changes": True, "help": "Release a live change to everyone", "args": [
        ["change", {"type": "int"}], ["--as", {"type": "str", "required": True}]]},
    {"name": "off", "changes": True, "help": "Off switch: stop showing a live change at once", "args": [
        ["change", {"type": "int"}], ["--as", {"type": "str", "required": True}]]},
    {"name": "on", "changes": True, "help": "A person switches a change back on", "args": [
        ["change", {"type": "int"}], ["--as", {"type": "str", "required": True}]]},
    {"name": "undo", "changes": True, "help": "Undo a change in one step", "args": [
        ["change", {"type": "int"}], ["--as", {"type": "str", "required": True}], ["--reason", {"type": "str"}]]},
    {"name": "evaluate", "changes": False, "help": "Measure a change and recommend keep, revise or undo", "args": [
        ["change", {"type": "int"}]]},
    {"name": "tick", "changes": True, "help": "Run the product's scheduler once", "args": []},
    {"name": "changes", "changes": False, "help": "List changes and their status", "args": [
        ["--kind", {"type": "str"}], ["--key", {"type": "str"}]]},
    {"name": "audit", "changes": False, "help": "The audit trail, for one change or all", "args": [
        ["--change", {"type": "int"}]]},
    {"name": "describe", "changes": False, "help": "Print this capability map", "args": []},
    {"name": "backup", "changes": False, "help": "Copy the whole store to a file", "args": [["path", {"type": "str"}]]},
    {"name": "restore", "changes": True, "help": "Restore a backup into a fresh location and verify it", "args": [
        ["backup", {"type": "str"}], ["--into", {"type": "str", "required": True}]]},
    {"name": "migrate", "changes": True, "help": "Move the store's schema up or down", "args": [["--to", {"type": "int"}]]},
    {"name": "purge-signals", "changes": True, "help": "Retention: delete signals older than N days", "args": [
        ["--older-than-days", {"type": "int", "required": True}]]},
]


def capability_map(app):
    from .app import VERSION
    pol = app.door.policy()
    kinds = {}
    for kind, definition in app.kinds.items():
        rules = policy_rules.rules_for(pol, kind)
        level = rules.get("dial", 1)
        kinds[kind] = {
            "name": definition["name"], "who": definition["who"], "main": definition["main"],
            "fields": definition["fields"], "measure": definition["measure"],
            "released_gradually": bool(definition.get("traffic")),
            "dial": level, "dial_name": policy_rules.DIAL_NAMES[level],
            "who_may_propose": [a for a, d in policy_rules.MIN_DIAL_TO_PROPOSE.items() if level >= d],
            "ships_without_a_person": level >= 4 and kind != "policy",
            "limits": {k: v for k, v in rules.items() if k != "dial"},
            "definitions": len(app.store.stable_view(kind)),
        }
    return {
        "product": "Answer Desk", "version": VERSION, "schema_version": app.store.schema_version(),
        "door": ["propose", "policy decision", "checks", "release to a share of traffic", "measure", "keep, revise or undo"],
        "actors": {"person": "people, through the command line", "ai": "the AI drafter (a deterministic stand-in)",
                   "product": "the product's own scheduler"},
        "dial_names": policy_rules.DIAL_NAMES,
        "kinds": kinds,
        "policy": {"raise_rule": pol["raise_rule"], "demote_after_reversals": pol["demote_after_reversals"],
                   "invariants": ["the policy never ships without a person, except a change that only lowers dials",
                                  "AI and the product may add checks, never change or remove them",
                                  "AI and the product may not remove definitions",
                                  "a dial is raised one step at a time, and only on a measured record"]},
        "operations": OPERATIONS,
    }
