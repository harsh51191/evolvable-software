"""Command line for people and agents. The parser is generated from describe.OPERATIONS; output is JSON."""
import argparse
import json
import os
import sys
import time

from .app import App
from .describe import OPERATIONS, capability_map
from .door import DoorError, parse_actor
from .store import Store

TYPES = {"str": str, "int": int, "float": float, "json": json.loads}


def build_parser():
    parser = argparse.ArgumentParser(prog="answerdesk", description="Answer Desk: a small product born evolvable.")
    parser.add_argument("--store", default=os.environ.get("ANSWER_DESK_STORE", "answer-desk.db"),
                        help="path of the SQLite store (default: $ANSWER_DESK_STORE or answer-desk.db)")
    sub = parser.add_subparsers(dest="command", required=True)
    for op in OPERATIONS:
        p = sub.add_parser(op["name"], help=op["help"], description=op["help"])
        for name, spec in op["args"]:
            if spec["type"] == "flag":
                p.add_argument(name, action="store_true", help=spec.get("help"))
            elif name.startswith("--"):
                p.add_argument(name, type=TYPES[spec["type"]], required=spec.get("required", False), help=spec.get("help"))
            else:
                p.add_argument(name, type=TYPES[spec["type"]], help=spec.get("help"))
    return parser


def person(actor):
    if parse_actor(actor)[0] != "person":
        raise DoorError("on the command line you act as a person: --as person:NAME")
    return actor


def run(args):
    if args.command == "restore":
        return {"restored": Store.restore(args.backup, args.into)}
    app = App(args.store, time.time)
    try:
        door, desk, c = app.door, app.desk, args.command
        if c == "init":
            app.seed()
            return {"initialised": args.store}
        if c == "ask":
            return desk.ask(args.question, args.session or "cli")
        if c == "feedback":
            expected = {}
            if args.expected_answer:
                expected["answer"] = args.expected_answer
            if args.expected_team:
                expected.update({"answer": None, "team": args.expected_team})
            desk.feedback(args.signal, not args.unhelpful, expected or None)
            return app.store.signal(args.signal)
        if c == "signals":
            return [{"question": q, "count": n} for q, n in desk.unmet()] if args.unmet else app.store.signals()
        if c == "propose":
            if args.remove == (args.body is not None):
                raise DoorError("give either --body or --remove")
            return door.submit(args.kind, args.key, args.body, person(getattr(args, "as")), args.note or "")
        if c == "draft":
            return app.draft(args.question)
        if c == "approve":
            return door.approve(args.change, person(getattr(args, "as")), args.share)
        if c == "keep":
            return door.promote(args.change, person(getattr(args, "as")))
        if c == "off":
            return door.switch_off(args.change, person(getattr(args, "as")))
        if c == "on":
            return door.switch_on(args.change, person(getattr(args, "as")))
        if c == "undo":
            return door.undo(args.change, person(getattr(args, "as")), args.reason or "")
        if c == "evaluate":
            return door.evaluate(args.change)
        if c == "tick":
            return app.tick()
        if c == "changes":
            return app.store.list_changes(args.kind, args.key)
        if c == "audit":
            return app.store.events(args.change)
        if c == "describe":
            return capability_map(app)
        if c == "backup":
            return {"backup": app.store.backup(args.path)}
        if c == "migrate":
            return {"schema_version": app.store.migrate(args.to)}
        if c == "purge-signals":
            return {"deleted": app.store.purge_signals(app.store.now() - args.older_than_days * 86400)}
        raise DoorError("unknown command %s" % c)
    finally:
        app.close()


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except (DoorError, KeyError, ValueError, RuntimeError, FileExistsError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0
