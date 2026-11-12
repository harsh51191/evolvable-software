"""Smart matching: the best answer for a question, and the queue for the rest.

An answer matches on how many of its keywords appear in the question. Rules are tried
from the highest priority down; the first pattern that matches picks the queue."""
import re


def normalise(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def best_answer(question, answers):
    words = set(normalise(question).split())
    scored = [(len(words & {k.lower() for k in a["keywords"]}), a["key"], a) for a in answers]
    scored = [s for s in scored if s[0] > 0]
    return max(scored, key=lambda s: (s[0], s[1]))[2] if scored else None


def route(question, rules):
    for rule in sorted(rules, key=lambda r: (-r["priority"], r["key"])):
        if re.search(rule["pattern"], question, re.IGNORECASE):
            return rule["queue"]
    return "general"
