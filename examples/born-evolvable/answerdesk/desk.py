"""The product itself, and foundation 5: answering questions and recording signals.

Hot core logic (matching a question to an answer or a team) is code. What it matches against is
data: the stable and candidate versions of answers and routing rules. Every question becomes a
structured signal, with personal data removed before it is stored.
"""
import hashlib
import re

WORD = re.compile(r"[a-z0-9]+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
NUMBER = re.compile(r"\+?\d[\d\s().-]{5,}\d")
TRAFFIC = ("answers", "routing-rules")


def redact(text):
    """Remove email addresses and long numbers (phone, card, account) before anything is stored."""
    text = EMAIL.sub("[email]", text)
    text = NUMBER.sub("[number]", text)
    return " ".join(text.split())[:300]


def tokens(text):
    return set(WORD.findall(text.lower()))


def resolve(question, answers, rules):
    """Pick the answer with the most keyword overlap (ties by key); otherwise route by rule."""
    words = tokens(question)
    best = None
    for key, body in sorted(answers.items()):
        overlap = len(words & set(body["keywords"]))
        if overlap >= body.get("need", 1) and (best is None or overlap > best[0]):
            best = (overlap, key)
    if best:
        return {"answer": best[1], "team": None, "rule": None}
    for key, body in sorted(rules.items(), key=lambda kv: (-kv[1].get("priority", 0), kv[0])):
        if words & set(body["keywords"]):
            return {"answer": None, "team": body["team"], "rule": key}
    return {"answer": None, "team": "triage", "rule": None}


def apply(view, key, body):
    """Return a copy of a {key: body} view with one definition replaced or removed."""
    view = dict(view)
    if body is None:
        view.pop(key, None)
    else:
        view[key] = body
    return view


def bucket(change_id, session):
    """Deterministic share of traffic: the same session always lands in the same arm of a change."""
    digest = hashlib.sha256(("%s:%s" % (change_id, session)).encode()).hexdigest()
    return int(digest[:8], 16) % 1000 / 1000.0


def good(signal, kind):
    """The outcome each traffic kind is measured on."""
    if signal["feedback"] == "unhelpful":
        return False
    if kind == "answers":
        return signal["answer_key"] is not None
    return signal["answer_key"] is None and signal["team"] not in (None, "triage")


class Desk:
    def __init__(self, store):
        self.store = store

    def ask(self, question, session):
        store = self.store
        session = hashlib.sha256(("answer-desk:" + session).encode()).hexdigest()[:16]
        stable = {kind: store.stable_view(kind) for kind in TRAFFIC}
        served = dict(stable)
        arms = []
        for kind in TRAFFIC:
            for change in store.candidates(kind):
                arm = "candidate" if bucket(change["id"], session) < change["share"] else "control"
                if arm == "candidate":
                    served[kind] = apply(served[kind], change["key"], change["body"])
                arms.append((kind, change, arm))
        result = resolve(question, served["answers"], served["routing-rules"])

        # A question is exposed to a change only when the change could affect its outcome.
        exposures = []
        for kind, change, arm in arms:
            with_change = dict(served, **{kind: apply(served[kind], change["key"], change["body"])})
            without = dict(served, **{kind: apply(served[kind], change["key"], stable[kind].get(change["key"]))})
            seen = set()
            for view in (with_change, without):
                r = resolve(question, view["answers"], view["routing-rules"])
                seen.update([r["answer"], r["rule"]])
            if change["key"] in seen:
                exposures.append((change["id"], arm))

        answer_change = None
        if result["answer"]:
            exposed_ids = {cid for cid, arm in exposures if arm == "candidate"}
            candidate = [c for k, c, a in arms if k == "answers" and c["key"] == result["answer"] and c["id"] in exposed_ids]
            answer_change = candidate[0]["id"] if candidate else store.live("answers", result["answer"])[0]
        signal_id = store.add_signal(session, redact(question), result["answer"], answer_change, result["team"], exposures)
        if result["answer"]:
            text = served["answers"][result["answer"]]["answer"]
        else:
            text = "I have passed your question to the %s team." % result["team"]
        return {"signal": signal_id, "answer_key": result["answer"], "team": result["team"], "text": text}

    def feedback(self, signal_id, helpful, expected=None):
        if self.store.signal(signal_id) is None:
            raise KeyError("no question %s" % signal_id)
        self.store.set_feedback(signal_id, "helpful" if helpful else "unhelpful", expected)

    def unmet(self):
        """Questions the desk could not answer, grouped, most frequent first."""
        counts = {}
        for s in self.store.signals():
            if s["answer_key"] is None:
                q = s["question"].lower().strip(" ?!.")
                counts[q] = counts.get(q, 0) + 1
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
