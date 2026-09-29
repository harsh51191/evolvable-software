#!/usr/bin/env python3
"""Create a neutral MSR score-input template from the rubric."""

import argparse
import datetime
import json
import os
import re


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RUBRIC = os.path.join(HERE, "..", "references", "rubric.md")
ARCHETYPES = (
    "configurable-application-platform",
    "agent-runtime",
    "developer-platform",
    "focused-application",
    "other",
)


def criterion_ids(path):
    ids = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            match = re.match(r"^### ([A-Z]\d+)\s+", line.strip())
            if match:
                ids.append(match.group(1))
    if not ids:
        raise SystemExit(f"No criteria found in {path}")
    return ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", required=True)
    parser.add_argument("--archetype", required=True, choices=ARCHETYPES)
    parser.add_argument("--source", required=True)
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--rubric", default=DEFAULT_RUBRIC)
    args = parser.parse_args()

    output = {
        "product": args.product,
        "date": args.date,
        "source": args.source,
        "archetype": args.archetype,
        "scores": {
            criterion: {
                "status": "not_evidenced",
                "searched": "Not evaluated yet",
            }
            for criterion in criterion_ids(args.rubric)
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
