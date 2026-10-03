# EVOLVE: self-evolution readiness

EVOLVE assesses how ready a software product is to evolve itself safely: to take a user's request through to release, find and fix the issues users face, and notice adjacent opportunities, increasingly with AI doing the work.

For each of those three loops it reports a Software Autonomy Level from L0 (manual) to L5 (self-directing), how far AI itself carries the loop, the critical controls that fail (such as rolling back every change users can make, or restoring scheduled jobs safely), exactly what blocks the next level, and a prerequisite-ordered plan to get there. Every score is tied to file-level evidence.

## Use it

Ask for an assessment of a repository you can read, for example: "Assess how ready this repository is to evolve itself safely." The skill sets the scope with you, gathers evidence, scores each criterion, runs the bundled scorer and writes a scorecard.

## What it runs and sends

- **Reads** only the repositories and documents you point it at, and asks before cloning or opening a new remote source. It never changes the repository it assesses.
- **Writes** one assessment input file (JSON) at a path you choose, and the reports you ask for.
- **Runs** two bundled Python scripts, `scripts/init_scores.py` and `scripts/score.py`, which use the standard library only. They make no network calls and install nothing.
- **Sends** nothing to any service. There are no hooks, MCP servers or telemetry.

## More

The framework, design notes, tests and an 11-product field test live at https://github.com/harsh51191/evolvable-software. MIT licensed.
