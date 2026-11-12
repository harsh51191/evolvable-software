"""The AI drafter: an interface where a real model plugs in, and a deterministic stand-in.

`RuleDrafter` is NOT a language model. It drafts an answer by rule from local source documents,
so the example runs offline and its tests are repeatable. A real drafter would implement the same
`draft_answer` method; everything it returns still goes through the door, the policy and the checks.
The question is treated as data only: it selects words and a source section, and never instructions.
"""
import glob
import os
import re

from .desk import tokens

STOP = {"a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "how", "i", "if",
        "in", "is", "it", "me", "my", "of", "on", "or", "the", "to", "we", "what", "when", "where", "who",
        "why", "will", "with", "you", "your"}


class Drafter:
    """Interface: return {"key": ..., "body": {...answer definition...}} or None if it cannot help."""
    name = "drafter"

    def draft_answer(self, question):
        raise NotImplementedError


class RuleDrafter(Drafter):
    name = "rule-drafter"

    def __init__(self, source_dir):
        self.sections = []
        for path in sorted(glob.glob(os.path.join(source_dir, "*.md"))):
            with open(path, encoding="utf-8") as f:
                parts = re.split(r"^## +(.+)$", f.read(), flags=re.M)
            rel = "sources/" + os.path.basename(path)
            for heading, text in zip(parts[1::2], parts[2::2]):
                self.sections.append((heading.strip(), " ".join(text.split()), rel))

    def draft_answer(self, question):
        wanted = tokens(question) - STOP
        best = None
        for heading, text, path in self.sections:
            overlap = wanted & tokens(heading + " " + text)
            if overlap and (best is None or len(overlap) > len(best[0])):
                best = (overlap, heading, text, path)
        if best is None:
            return None
        overlap, heading, text, path = best
        slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        keywords = sorted(overlap)[:5]
        sentences = re.split(r"(?<=[.!?]) +", text)
        return {"key": slug, "body": {"keywords": keywords, "need": min(2, len(keywords)),
                                      "answer": " ".join(sentences[:2]), "source": "%s#%s" % (path, slug)}}
