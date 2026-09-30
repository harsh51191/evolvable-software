#!/usr/bin/env python3
"""One-off migration of the v0.2 field-test inputs to rubric v0.3.

Applies only the changes the revised rubric requires (removed M2, new P1 and P2,
rewritten J2, unbundled A2 and A3, default-versus-available scoring, the self
rule, and the widened OpenHands scope). Every changed entry carries its evidence.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def a(score, evidence, grade="A", **extra):
    return {"status": "assessed", "score": score, "grade": grade, "evidence": evidence, **extra}

CHANGES = {
 "frappe": {
  "A3": a(4, "Link, Dynamic Link and Table fields declare relations and Workflow DocTypes declare states and transitions in the UI (frappe/workflow/doctype/); the platform enforces transitions (frappe/model/workflow.py:119-246) and link integrity (frappe/model/delete_doc.py:414); both are creatable through the REST API with validation errors, which meets the rubric's definition of AI-authorable.", alt_score=3, alt_note="If AI-authorable is read as needing an AI authoring feature."),
  "J2": a(1, "No typed feedback or rating objects; Error Log links errors to reference documents but not to the definition version.", alt_score=2, alt_note="Error Log entries are typed signals linked to documents."),
  "P1": a(2, "The Recorder proposes database indexes from recorded queries when a person runs it (frappe/core/doctype/recorder/db_optimizer.py:242); nothing proposes changes without being asked."),
  "P2": a(1, "Suggested changes are applied by a person; there is no automated evaluation."),
 },
 "directus": {
  "A2": a(3, "Typed fields with validation rules, conditions, required, unique and is_indexed are created in the UI and read by forms and the generated APIs (api/services/fields.ts:62, 1008-1012). v0.3 moved the privacy tag to E3.", alt_score=2, alt_note="Validation rules are partial for some field types."),
  "A3": a(3, "M2O, O2M, M2M and M2A relations are declared in the UI with database-level referential actions; lifecycle states are not a feature, and v0.3 accepts either at level 3.", alt_score=2, alt_note="If lifecycle states are considered central for this product."),
  "J2": a(1, "Item comments are free text; no typed feedback or rating objects linked to definitions."),
  "P1": a(1, "The AI assistant acts only on request (api/src/ai); nothing learns from use."),
  "P2": a(1, "AI-authored changes pass a human approval (api/src/ai/tools/registry.ts:198-214); there is no evaluation against a baseline."),
 },
 "discourse": {
  "D1": a(2, "By default: the automation plugin and watched words with a test mode (plugins/automation, app/models/watched_word.rb). The workflows plugin with versions, validators and test sessions is an off-by-default beta (plugins/discourse-workflows/config/settings.yml:4-11).", available_score=3),
  "D3": a(2, "By default, sandboxed code runs only as discourse-ai tool scripts with timeouts (plugins/discourse-ai/lib/agents/tool_runner.rb:44-58), and discourse-ai is off by default; the beta workflows Code node adds a sandbox with a resource budget (js_sandbox.rb, sandbox_budget.rb).", available_score=3),
  "F2": a(1, "By default, admins change settings and themes directly. With the beta workflows plugin on, an AI author writes risk-rated draft proposals that are validated and applied by an admin (plugins/discourse-workflows/lib/discourse_workflows/ai_workflow_author.rb:39-67).", available_score=2),
  "K2": a(1, "By default only the tutorial narrative bot is conversational (plugins/discourse-narrative-bot). With discourse-ai on (default false), AI agents answer members with retrieval and tools, and admins author workflows in natural language.", available_score=3),
  "M3": a(0, "By default there is no AI authoring lane; the beta workflows AI author is one when enabled.", available_score=2),
  "J2": a(2, "Typed flags feed a review queue with triage (app/models/reviewable.rb); they concern content, not the product's definitions and versions."),
  "P1": a(2, "Problem checks run on a schedule and raise configuration recommendations (app/services/problem_check); they are rules, not learning from experience."),
  "P2": a(1, "By default, changes are reviewed by people. With the workflows beta, AI proposals are validated with workflow_validate_patch before an admin applies them.", available_score=2),
 },
 "posthog": {
  "A2": a(3, "Event and person property definitions carry a validated property_type and format editable in Data management and read by queries and the UI (products/event_definitions/backend/models/property_definition.py:73-152). v0.3 moved the privacy tag to E3."),
  "J2": a(1, "Under the self rule, surveys and Signals concern customers' products and are not counted; no typed signals about PostHog's own configured definitions were found (searched products/signals, products/surveys, ee/hogai).", alt_score=2, alt_note="PostHog AI may record typed feedback on its answers."),
  "J3": a(2, "Under the self rule, Signals (which mines customers' products) is not counted; PostHog analyses its own query logs to decide what to materialise (ee/clickhouse/materialized_columns/analyze.py:89).", alt_score=3, alt_note="If Signals run on PostHog's own product counts."),
  "M1": a(2, "Query analysis recommends and applies materialised columns (ee/clickhouse/materialized_columns/analyze.py); Signals proposals target customers' repositories and are excluded under the self rule.", alt_score=3, alt_note="If Signals proposals count."),
  "M3": a(2, "PostHog AI creates insights, dashboards and other configured objects on request (ee/hogai); Tasks agents that open pull requests in customers' repositories are excluded under the self rule.", alt_score=3, alt_note="If the Tasks lane counts."),
  "P1": a(3, "A weekly scheduled task analyses the last week of queries and materialises hot properties without being asked (posthog/tasks/scheduled.py:927, ee/settings.py:68-73, ee/clickhouse/materialized_columns/analyze.py:89). Narrow: storage layout only.", alt_score=2, alt_note="Narrow to one area."),
  "P2": a(1, "No evaluation of materialisation changes against a baseline was found.", alt_score=2, alt_note="Materialisation may be checked in code not read."),
 },
 "n8n": {
  "J2": a(2, "Evaluation test runs record metrics per workflow (packages/@n8n/db/src/entities/test-run.ee.ts) and insights record per-workflow outcomes; no triage workflow.", alt_score=3, alt_note="Test runs are linked to the workflow they evaluate."),
  "P1": a(1, "The AI workflow builder and Instance AI change workflows when asked; nothing learns from runs without being asked.", alt_score=2, alt_note="Insights capture experience that the AI can read on request."),
  "P2": a(2, "Evaluations can compare a workflow version against a dataset before publishing (packages/cli/src/evaluation.ee), but they are run by people and are not tied to the publish decision.", alt_score=3, alt_note="If evaluations plus the review publish guard count as a pass or block decision."),
 },
 "dify": {
  "J2": a(2, "Message feedback (rating, content, source) is linked to messages and conversations (api/models/model.py:296-335) and triaged through logs and annotations; the link to the app configuration version was not verified.", alt_score=3, alt_note="Messages record the app configuration they ran with."),
  "P1": a(2, "Admins turn logged answers into annotations that the app reuses for similar questions (api/services/annotation_service.py); nothing proposes changes without being asked."),
  "P2": a(1, "Annotations and app changes are applied by people without evaluation against a baseline."),
 },
 "librechat": {
  "J2": a(2, "Message feedback with rating, tag and text is stored on messages (packages/data-schemas/src/schema/message.ts:103); no triage workflow."),
  "P1": a(1, "By default nothing learns from use. With the memory block enabled (commented out in librechat.example.yaml:1351-1360), a memory agent stores user facts from recent chat automatically.", available_score=3),
  "P2": a(1, "No checks on learned memories beyond configured key and token limits (librechat.example.yaml:1354-1358)."),
 },
 "hermes-agent": {
  "F2": a(2, "By default, skill and memory writes apply directly and are ledgered. With skills.write_approval or memory.write_approval on, writes are staged with a gist and applied through /skills approve (tools/write_approval.py:73-189); the self-evolution repo proposes evaluated skill variants as pull requests.", available_score=3),
  "F3": a(2, "By default only protected instruction files always need a human (cli-config.yaml.example:573-576); skill and memory gates default to off (hermes_cli/config_defaults.py:1320). With them on, each change class has its own gate.", available_score=3),
  "J2": a(3, "Every skill has view, use and patch counts linked to it (tools/skill_usage.py), and the curator triages skills into active, stale and archived (website/docs/user-guide/features/curator.md).", alt_score=2, alt_note="Usage counts are not versioned per skill revision."),
  "P1": a(3, "background_review is enabled by default (hermes_cli/config_defaults.py:814): after turns, a forked agent decides whether to save or update skills and memory (agent/background_review.py).", alt_score=4, alt_note="The curator's consolidation learns which skills stick, but only when enabled."),
  "P2": a(2, "Skill writes pass security scans, AST audits and a linter (tools/skills_guard.py, skills_ast_audit.py, skill_linter.py). The first-party GEPA optimiser evaluates variants against the baseline skill before proposing, when it is run (hermes-agent-self-evolution README).", available_score=3),
 },
 "openclaw": {
  "F3": a(2, "Defaults are autonomous.mode auto and approvalPolicy auto (src/skills/workshop/config.ts:15-20), so proposals apply without a person; evaluator block decisions only exist if an evaluator plugin is installed. Setting approvalPolicy to pending gives a per-class approval policy.", available_score=3),
  "J2": a(3, "Experience-review observations and evaluation findings are stored on the proposal revision they concern and recorded in the append-only proposal event ledger (src/skills/workshop/experience-review*.ts, docs/tools/skill-workshop/proposals.md).", alt_score=2, alt_note="Observations come from sessions, not from users."),
  "P1": a(3, "With autonomous.mode auto by default, the experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, proposal-generation.ts).", alt_score=4, alt_note="The curator tracks which skills persist."),
  "P2": a(2, "Proposals are scanned before apply (src/skills/workshop/proposal-scan.ts), and evaluator hooks can compare against the baseline and block, but no evaluator ships (none in extensions/)."),
 },
 "opencode": {
  "J2": a(0, "No feedback, rating or evaluation signals in the product."),
  "P1": a(1, "People write agents, commands and AGENTS.md by hand; nothing learns from sessions."),
  "P2": a(1, "Changes to OpenCode's definitions are reviewed by people only."),
 },
 "openhands": {
  "D2": a(3, "The agent server posts events to configured webhooks with buffering and retries (openhands-agent-server/openhands/agent_server/config.py:73-104)."),
  "D3": a(2, "Hooks run at defined points (openhands-sdk/openhands/sdk/hooks); agent actions run in Docker, Apptainer, cloud or remote workspaces (openhands-workspace/openhands/workspace), but hook isolation and egress control were not verified.", alt_score=3, alt_note="If hooks execute inside the sandboxed workspace."),
  "F3": a(2, "Confirmation policies (never, always, confirm risky) decide which agent actions need a person (openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43); they govern actions, not changes to the agent itself."),
  "F4": a(3, "CI checks REST API breakage, persisted-settings compatibility and deprecations on every change (software-agent-sdk .github/workflows/agent-server-rest-api-breakage.yml, persisted-settings-compat.yml, deprecation-check.yml)."),
  "K3": a(2, "The default confirmation policy is NeverConfirm (openhands-sdk/openhands/sdk/conversation/state.py:123); with ConfirmRisky, LLM security analyzers classify each action's risk and risky ones pause for a person (security/llm_analyzer.py, toolshield_llm_analyzer.py, ensemble.py).", available_score=3),
  "J2": a(1, "No typed feedback or learning signals in the canvas or the SDK."),
  "P1": a(1, "No learning from sessions was found in the SDK (searched openhands-sdk/openhands/sdk/skills, context, agent)."),
  "P2": a(1, "Critics evaluate task output for iterative refinement (openhands-sdk/openhands/sdk/critic), not changes to the agent itself."),
 },
}

SOURCES = {"openhands": "github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main)"}

for system, changes in CHANGES.items():
    path = os.path.join(ROOT, system, "scores.json")
    data = json.load(open(path))
    data["scores"].pop("M2", None)
    data["scores"].update(changes)
    data["framework_version"] = "0.3.0"
    if system in SOURCES:
        data["source"] = SOURCES[system]
        data["product"] = "OpenHands (Agent Canvas + software-agent-sdk)"
        data["scope_line"] = ("Scope: OpenHands/OpenHands (Agent Canvas front end) plus OpenHands/software-agent-sdk (SDK, agent server, tools, workspaces), "
                              "because v0.3 requires assessing delegated capabilities where they live. OpenHands Cloud is out of scope.")
    for key in ("reading",):
        data.pop(key, None)
    with open(path, "w") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
print("migrated", len(CHANGES))
