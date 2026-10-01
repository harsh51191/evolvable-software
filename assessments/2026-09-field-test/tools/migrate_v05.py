#!/usr/bin/env python3
"""One-off: add the v0.5 AI Readiness inputs to the field-test assessments.

Adds the three AI scope facts, the eight AIR checks, and the AI-qualified
reading for each of the 13 reused criteria. SAL inputs are not touched.
Provisional, single-rater evidence read at the tips named in each assessment.
The script refuses to run twice.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ["frappe", "directus", "discourse", "posthog", "n8n", "dify", "librechat",
           "hermes-agent", "openclaw", "opencode", "openhands"]
AIR = ["AIR-01", "AIR-02", "AIR-03", "AIR-04", "AIR-05", "AIR-06", "AIR-07", "AIR-08"]
READINGS = ["MAL-19", "MAL-20", "DEL-01", "DEL-04", "LRN-05", "LRN-06", "LRN-07", "LRN-08",
            "EXP-05", "GOV-09", "GOV-10", "GOV-11", "ARC-08"]
IT = {"implemented": True, "tested": True, "operated": False}
I = {"implemented": True, "tested": False, "operated": False}


def a(score, evidence, grade="A", **extra):
    return {"status": "assessed", "score": score, "grade": grade, "evidence": evidence, **extra}


def up(score, evidence, note, **extra):
    return a(score, evidence, alt_score=score + 1, alt_note=note, **extra)


def na(reason):
    return {"status": "not_applicable", "rationale": reason}


def f(value, evidence, available=None):
    out = {"value": value, "evidence": evidence}
    if available is not None:
        out["available_value"] = available
    return out


ALL_TRUE = lambda ai, data, act: {"ai_features": f(True, ai), "ai_data_access": f(True, data), "ai_actions": f(True, act)}

FACTS = {
 "frappe": {"ai_features": f(False, "No model-backed features in the framework (searched frappe/ for openai, anthropic, llm)."),
            "ai_data_access": f(False, "No AI features."), "ai_actions": f(False, "No AI features.")},
 "directus": ALL_TRUE("The AI assistant and MCP server (api/src/ai).", "AI tools read items, files, schema and flows (api/src/ai/tools).",
                      "AI tools create and change collections, fields, flows and items behind approvals (api/src/ai/tools/registry.ts)."),
 "discourse": {"ai_features": f(False, "discourse-ai ships bundled but discourse_ai_enabled defaults to false (plugins/discourse-ai/config/settings.yml:2-3).", True),
               "ai_data_access": f(False, "Off by default; when enabled, agents search and read topics and RAG documents.", True),
               "ai_actions": f(False, "Off by default; when enabled, agent tools edit posts, change categories and site settings (plugins/discourse-ai/lib/agents/tools).", True)},
 "posthog": ALL_TRUE("PostHog AI (ee/hogai) and the LLM gateway (services/llm-gateway).", "PostHog AI queries the team's events, insights and taxonomy (ee/hogai/context).",
                     "PostHog AI creates and edits insights, dashboards and other objects (ee/hogai/tools)."),
 "n8n": ALL_TRUE("AI workflow builder, Instance AI and AI agent nodes (packages/@n8n/ai-workflow-builder.ee, packages/cli/src/modules/instance-ai).",
                 "Instance AI reads workflows, executions and node parameters (packages/cli/src/modules/instance-ai).",
                 "Instance AI and the builder create and change workflows behind approvals."),
 "dify": ALL_TRUE("LLM apps, agents and workflows are the product (api/core).", "Knowledge-base retrieval (api/core/rag).",
                  "Agent and workflow tools call external services and write data (api/core/tools)."),
 "librechat": ALL_TRUE("Chat with many model providers and agents (packages/api/src/endpoints, agents).", "File search over uploaded files (api/app/clients/tools/util/fileSearch.js).",
                       "Agents call tools and MCP servers that act on external systems (packages/api/src/mcp)."),
 "hermes-agent": ALL_TRUE("The product is an LLM agent.", "Reads the user's files, sessions, memory and skills (session search, memory providers).",
                          "Runs commands, edits files and sends messages on the user's behalf (tools/)."),
 "openclaw": ALL_TRUE("The product is an LLM agent.", "Reads memory, sessions and workspace files (src/memory, src/context-engine).",
                      "Runs commands, sends channel messages and changes skills (src/agents, src/skills)."),
 "opencode": ALL_TRUE("The product is an LLM coding agent.", "Reads the workspace through read, grep, glob and LSP tools.",
                      "Edits files and runs shell commands (packages/opencode/src/tool)."),
 "openhands": ALL_TRUE("The product runs LLM agents (openhands-sdk).", "Agents read repositories and workspace files in their sandbox.",
                       "Agents edit code, run commands and open pull requests; automations run them unattended."),
}

AIR_SCORES = {
 "directus": {
  "AIR-01": a(2, "OpenAI, Anthropic, Google and OpenAI-compatible providers configured by admins, model chosen in the chat (api/src/ai/providers/registry.ts); no fallback or declared resilience strategy."),
  "AIR-02": a(1, "Usage is streamed to the client per request (api/src/ai/chat/controllers/chat.post.ts:71-72); not recorded per user, and no budgets."),
  "AIR-03": a(3, "Schema-aware tools read live collections, fields, relations, items and files (api/src/ai/tools/schema, items, files); results come from the source records."),
  "AIR-04": a(3, "Tool calls run through services with the requesting user's accountability, so Directus permissions apply (api/src/ai/tools/items, tests pass accountability through: items/index.test.ts).", facets=IT),
  "AIR-05": a(0, "No evaluation harness for the assistant (searched api/src/ai for eval)."),
  "AIR-06": a(0, "No evaluation in CI; AI changes ship unevaluated (.github/workflows)."),
  "AIR-07": a(2, "Opt-in Langfuse and Braintrust telemetry records model calls with user, role, provider and model (api/src/ai/telemetry); revisions record data changes by the user, without the model or prompt."),
  "AIR-08": a(0, "No feedback or quality monitoring for the assistant."),
 },
 "discourse": {
  "AIR-01": a(2, "Admins configure LLM models per provider and assign them per agent and feature (app/models/llm_model.rb); no fallback when a model fails. Scored as shipped, with discourse-ai enabled."),
  "AIR-02": a(3, "Per-group LLM quotas on tokens and usages per period, credit allocations and daily usage (app/models/llm_quota.rb, llm_credit_allocation.rb, llm_credit_daily_usage.rb), with admin screens."),
  "AIR-03": a(3, "Embeddings, semantic search and RAG fragments kept up to date by jobs (app/models/rag_document_fragment.rb, embedding_definition.rb); agents search and read topics with citations."),
  "AIR-04": a(3, "Agent tools read with an anonymous Guardian unless private reading is allowed, then with the user's Guardian (lib/agents/tools/read.rb:51-62); 34 tools use Guardian checks, with specs.", facets=IT),
  "AIR-05": a(2, "An evaluation harness with an LLM judge (plugins/discourse-ai/evals/lib/eval.rb, judge.rb) run from the command line; datasets live outside this repository."),
  "AIR-06": a(1, "Evaluations are not run in CI; prompt and model changes are reviewed manually."),
  "AIR-07": a(3, "Every LLM call is logged with user, topic, model, feature, request and response payloads and tokens (app/models/ai_api_audit_log.rb, migration 20230424055354); tool actions are recorded and can be reviewed (ai_tool_action.rb, reviewable_ai_tool_action.rb).", facets=IT),
  "AIR-08": a(2, "Accuracy of AI triage against moderator decisions and spam logs are recorded per model and feature (app/models/model_accuracy.rb, ai_spam_log.rb); no drift alerts."),
 },
 "posthog": {
  "AIR-01": a(3, "The LLM gateway routes across providers with Cloudflare, Modal and Bedrock fallbacks and a circuit breaker (services/llm-gateway/src/llm_gateway/baseten.py:34, circuit_breaker.py), with tests (tests/test_circuit_breaker.py)."),
  "AIR-02": a(3, "Generations are marked billable for AI credits in the usage report and rate-limited (ee/hogai/llm.py:129-167, 282); credits are enforced per organisation through billing."),
  "AIR-03": a(3, "PostHog AI gets taxonomy, schema and entity context through tools over the team's live data (ee/hogai/context, tools)."),
  "AIR-04": a(3, "PostHog AI acts within the user's team with resource-level access control (products/access_control) and approval policies on mutating actions; covered by tests.", facets=IT),
  "AIR-05": a(3, "Maintained offline and CI evaluation suites per capability with scored metrics (ee/hogai/eval/ci: funnel, retention, insight search, memory, root; eval/offline)."),
  "AIR-06": a(2, "LLM evals run on pull requests labelled evals-ready (.github/workflows/ci-ai.yml:2-20); they are not automatic for every AI change and no blocking threshold was found."),
  "AIR-07": a(3, "AI generations and traces are captured in PostHog's own LLM analytics, and AI changes are attributed in the activity log (ee/hogai/llm.py, ee/hogai/llm_traces_summaries).", facets=IT),
  "AIR-08": up(2, "Generations, traces and user feedback on PostHog AI are recorded and summarised (ee/hogai/llm_traces_summaries, chat_agent/slash_commands/commands/feedback); no drift alerts found.", "LLM analytics dashboards per model may act as continuous monitoring."),
 },
 "n8n": {
  "AIR-01": a(3, "AI agent nodes support a fallback model (packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/utils.ts, ToolsAgent/common.ts), and operators choose models per node."),
  "AIR-02": a(3, "Instance AI credits are tracked and enforced per instance with a credit display (packages/cli/src/modules/instance-ai/instance-ai-credit.service.ts, instance-ai-credit-display.ts)."),
  "AIR-03": a(3, "The builder gets node types and workflow context; Instance AI resolves workflows, executions and node parameters live (packages/cli/src/modules/instance-ai/instance-context.service.ts)."),
  "AIR-04": a(3, "Instance AI looks up workflows within the user's scopes (instance-ai.adapter.service.ts) with folder-scope tests (__tests__/instance-ai-folder-scope.test.ts, instance-ai-folder-scoped-listing.integration.test.ts).", facets=IT),
  "AIR-05": a(3, "Evaluation harness with evaluators, datasets and LangSmith runs for the workflow builder and Instance AI (packages/@n8n/ai-workflow-builder.ee/evaluations)."),
  "AIR-06": up(2, "Instance AI evals run automatically on pull requests touching AI paths (.github/workflows/ci-instance-ai-evals.yml:18-21) and builder evals on minor releases (test-evals-ai-release.yml); no blocking threshold was found.", "Results are posted on every relevant pull request.", facets=IT),
  "AIR-07": up(2, "Instance AI tracing service (packages/cli/src/modules/instance-ai/tracing) and audit events for approved actions; model and prompt version are not recorded with each change.", "Approval cards and tracing together approach level 3.", facets=IT),
  "AIR-08": a(2, "Evaluation metrics per test run and failure rates per workflow are recorded (packages/cli/src/evaluation.ee, modules/insights); no drift alerts."),
 },
 "dify": {
  "AIR-01": a(3, "Builders choose models per app from many providers; load balancing with cooldown fails over across credentials, with tests (api/core/model_manager.py:68-130, tests/unit_tests/services/test_model_load_balancing_service.py)."),
  "AIR-02": a(3, "Token usage and cost recorded per message, credit usage and billing quota reservation per tenant (api/core/credit_usage.py, api/services/billing_service.py:77-89)."),
  "AIR-03": a(3, "Knowledge bases with indexing, retrieval and citations (api/core/rag)."),
  "AIR-04": a(2, "Dataset permissions control which builders can attach knowledge (api/services/knowledge_retrieval_inner_service.py), but published apps retrieve with the app's datasets, not each end user's permissions."),
  "AIR-05": a(1, "Builders test prompts manually in debug and preview; no evaluation harness."),
  "AIR-06": a(1, "Publishing follows manual testing; nothing blocks a regression."),
  "AIR-07": a(3, "Every message and workflow run is logged with inputs, outputs, model, tokens and node and tool executions, viewable by builders, with optional Langfuse, LangSmith and other tracing (api/core/ops/ops_trace_manager.py).", facets=IT),
  "AIR-08": a(2, "End-user likes and dislikes and app statistics (satisfaction, tokens) per app (api/models/model.py:1299-1302); no drift alerts."),
 },
 "librechat": {
  "AIR-01": a(2, "Admins configure many providers and model specs (librechat.yaml, packages/api/src/endpoints); no declared resilience strategy."),
  "AIR-02": a(2, "Token transactions recorded per user; balances that limit spending are opt-in (librechat.example.yaml:363-378).", available_score=3),
  "AIR-03": a(2, "File search over uploaded files through the RAG API (api/app/clients/tools/util/fileSearch.js); other product data is not indexed."),
  "AIR-04": up(2, "Retrieval covers files attached to the conversation or agent; agents shared through ACLs carry their builder's files to other users.", "Per-user file ownership checks may meet level 3.", facets=IT),
  "AIR-05": a(0, "No evaluation harness."),
  "AIR-06": a(1, "Configuration changes are tested manually in chat."),
  "AIR-07": a(2, "Messages store model, tokens and tool calls; Langfuse fan-out tracing is optional (packages/api/src/langfuse, traces/handlers.ts)."),
  "AIR-08": a(2, "Users rate messages with tags, and admin insights summarise usage (packages/data-schemas/src/schema/message.ts:103, packages/api/src/insights); no drift alerts."),
 },
 "hermes-agent": {
  "AIR-01": a(3, "Fallback providers and credential pools take over when a primary model fails, with tests (agent/agent_init.py, tests/agent/test_restore_primary_pool_reselect.py)."),
  "AIR-02": up(2, "Usage and pricing per turn and per account are tracked (agent/usage_pricing.py, turn_usage.py, billing_usage.py) and iterations are budgeted (agent/iteration_budget.py); no spend limit per user.", "Iteration budgets bound usage per task."),
  "AIR-03": a(3, "Session search over full-text indexes, memory and skills injected into context, with memory provider plugins (hermes_state_fts.py, plugins)."),
  "AIR-04": a(3, "A single-user agent acting with the user's own permissions; the gateway accepts only paired users, profiles isolate homes, and dangerous commands need approval (tools/approval_smart.py), with security tests (tests/security).", facets=IT),
  "AIR-05": a(2, "Regression probes named after failures found in use (evals/) and GEPA skill evaluation in the companion repository, run on request."),
  "AIR-06": a(1, "Evaluations are not part of CI."),
  "AIR-07": a(3, "Sessions record every message, tool call and model in the state database, with trajectories and trace upload (agent/trajectory.py, trace_upload.py, hermes_state_*.py), queryable through hermes sessions and insights.", facets=IT),
  "AIR-08": a(1, "Skill usage counts feed the curator; no quality or feedback monitoring of the agent's answers."),
 },
 "openclaw": {
  "AIR-01": a(3, "Model fallback with candidate generation and configured provider fallback, with tests (src/agents/model-fallback-attempt.ts, configured-provider-fallback.ts, configured-provider-fallback.test.ts)."),
  "AIR-02": a(2, "Agent run usage is recorded (src/infra/agent-run-usage.ts); no spend limit per user."),
  "AIR-03": a(3, "Memory host, context engine and session memory search assemble context automatically (src/memory, src/context-engine)."),
  "AIR-04": a(3, "A personal agent acting with the owner's permissions; DM pairing restricts who can instruct it, tool policies and exec approvals gate actions, with tests (src/pairing, src/agents/bash-tools.exec-approval-followup.test.ts).", facets=IT),
  "AIR-05": a(1, "Evaluator hooks exist for skill proposals but no evaluation set ships."),
  "AIR-06": a(1, "No evaluation gates in CI."),
  "AIR-07": a(3, "An agent event audit store with typed events and queries (src/audit/agent-event-audit.ts, audit-event-store.ts, audit-event-queries.ts) and session transcripts.", facets=IT),
  "AIR-08": a(1, "Diagnostic events only; no quality or feedback monitoring."),
 },
 "opencode": {
  "AIR-01": a(2, "Many providers through models.dev, with model choice per agent in configuration; retries with back-off (packages/opencode/src/session/retry.ts), no declared fallback."),
  "AIR-02": a(2, "Tokens and cost per session are recorded and shown by opencode stats (packages/opencode/src/cli/cmd/stats.ts); no spend limit."),
  "AIR-03": a(3, "Read, grep, glob and LSP tools give live, attributed workspace context, plus AGENTS.md instructions."),
  "AIR-04": a(3, "A local agent acting with the user's permissions; permission rules allow, ask or deny each tool and pattern, enforced in code (packages/opencode/src/permission/evaluate.ts), with tests.", facets=IT),
  "AIR-05": a(1, "No evaluation harness in the repository."),
  "AIR-06": a(1, "No evaluation gates in CI."),
  "AIR-07": a(3, "Sessions store every message, tool call, model and cost, and snapshots record file changes for revert (packages/opencode/src/session, snapshot).", facets=IT),
  "AIR-08": a(0, "No feedback or quality monitoring."),
 },
 "openhands": {
  "AIR-01": a(3, "LLM fallback strategy on connection, rate-limit and server errors, plus routers (openhands-sdk/openhands/sdk/llm/fallback_strategy.py, router), with tests (tests/sdk/llm/test_llm_fallback.py)."),
  "AIR-02": up(2, "Conversation cost and budget-exceeded handling (fallback_strategy.py), and run cost recorded per automation (automation repository: migrations/versions/013_add_run_cost.py); no per-user budgets.", "A per-conversation budget limits spend."),
  "AIR-03": a(3, "Agents work in a sandboxed workspace with repository files, skills and microagents loaded automatically."),
  "AIR-04": a(3, "Each conversation runs in its own sandbox with the user's provider tokens; automations use per-user API keys (automation repository: openhands/automation/auth.py), with tests.", facets=IT),
  "AIR-05": a(3, "Behaviour and integration test suites for agents (tests/integration) and SWE-bench evaluation runs (.github/workflows/run-eval.yml)."),
  "AIR-06": a(2, "Integration tests and evaluations run on labelled pull requests and releases (.github/workflows/integration-runner.yml, run-eval.yml); not blocking by default."),
  "AIR-07": a(3, "The event stream persists every action, observation and tool call per conversation, with LLM call metadata (openhands-sdk/openhands/sdk/conversation).", facets=IT),
  "AIR-08": a(1, "Critics score task output during a run; no production quality monitoring."),
 },
}

NO_AI = "No AI involvement in this behaviour."
AI_READ = {
 "directus": {
  "MAL-19": a(3, "MCP server over the AI tool registry with OAuth scopes (api/src/ai/mcp/server.ts)."),
  "MAL-20": a(2, "A grounded model-backed assistant for operators (api/src/ai/chat)."),
  "DEL-01": a(1, "The model receives free-text requests in chat; nothing structures them."),
  "DEL-04": up(1, "The AI lane drafts schema, flow and item changes behind approvals.", "An AI lane for narrow tasks on request."),
  "LRN-05": a(0, NO_AI), "LRN-06": a(0, NO_AI), "LRN-07": a(0, NO_AI),
  "LRN-08": a(1, "AI-made changes get human approval only (api/src/ai/tools/registry.ts:198-214)."),
  "EXP-05": a(0, NO_AI),
  "GOV-09": a(2, "AI acts with the user's accountability and mutations need approval; no idempotency or dry-run."),
  "GOV-10": a(2, "Per-tool approval and a switch to disable deletes; no blast-radius limit."),
  "GOV-11": a(1, "Untrusted content is not fenced from instructions."),
  "ARC-08": a(1, "Model errors are returned to the chat; no timeouts or breakers around model calls were found (api/src/ai/chat/lib)."),
 },
 "discourse": {
  "MAL-19": a(3, "Core MCP server with typed tools and scopes (lib/discourse_mcp)."),
  "MAL-20": a(0, "Off by default.", available_score=3),
  "DEL-01": a(0, NO_AI), "DEL-04": a(0, "Off by default.", available_score=2),
  "LRN-05": a(0, "Logster grouping is rule-based."), "LRN-06": a(0, "Problem checks are rules."), "LRN-07": a(0, NO_AI),
  "LRN-08": na("agent_mutations is false."), "EXP-05": a(0, NO_AI),
  "GOV-09": a(0, "Off by default.", available_score=3),
  "GOV-10": na("GOV-10 is not applicable."), "GOV-11": na("GOV-11 is not applicable."),
  "ARC-08": a(0, "Off by default.", available_score=2),
 },
 "posthog": {
  "MAL-19": a(3, "MCP service with typed tools per product and scoped keys (services/mcp)."),
  "MAL-20": a(3, "A grounded assistant that answers and creates objects (ee/hogai)."),
  "DEL-01": a(2, "Plan mode before acting (ee/hogai/chat_agent/prompts/plan.py)."),
  "DEL-04": up(2, "PostHog AI builds insights and dashboards on request.", "Broad object coverage."),
  "LRN-05": a(0, "Diagnosis of PostHog's own issues is not model-backed."),
  "LRN-06": a(0, "Materialisation recommendations are rule-based."),
  "LRN-07": a(0, "Column materialisation is heuristic tuning."),
  "LRN-08": a(1, "AI-made changes pass approval policies; no evaluation before apply."),
  "EXP-05": a(0, NO_AI),
  "GOV-09": up(2, "AI acts within the user's team with access control and approval policies; idempotency only on some writes.", "Approval policies may meet level 3."),
  "GOV-10": a(2, "A fixed tool set and approval policies; no blast-radius limit."),
  "GOV-11": up(2, "Session-derived content is fenced as data (ee/hogai/utils/untrusted.py).", "Systematic fencing."),
  "ARC-08": a(3, "LLM gateway circuit breaker and fallback, tested (services/llm-gateway, tests/test_circuit_breaker.py).", facets=IT),
 },
 "n8n": {
  "MAL-19": a(3, "Instance MCP server with scoped keys (packages/cli/src/modules/mcp)."),
  "MAL-20": a(3, "Instance AI grounded in workflows and executions, with plans and approvals."),
  "DEL-01": up(2, "The planner asks clarifying questions and drafts a plan (ai-workflow-builder.ee/src/types/planning.ts).", "Close to a specification."),
  "DEL-04": up(2, "The builder and Instance AI change workflows behind approvals.", "Wide coverage."),
  "LRN-05": up(2, "The AI assistant explains node errors with context on request.", "Close to level 3."),
  "LRN-06": a(0, "Breaking-change recommendations are rule-based."), "LRN-07": a(0, NO_AI),
  "LRN-08": a(2, "AI-built workflow versions can be evaluated against datasets before publishing, run by people (packages/cli/src/evaluation.ee)."),
  "EXP-05": a(0, NO_AI),
  "GOV-09": up(2, "Scoped keys and approval cards for AI actions; no idempotency or dry-run.", "Approval cards preview actions."),
  "GOV-10": a(2, "Type-availability policies restrict AI-built workflows."),
  "GOV-11": up(2, "Instance AI wraps external data as untrusted (extract-resolved-node-parameters.ts:378-382).", "Systematic in Instance AI."),
  "ARC-08": up(2, "Retry-on-fail, timeouts and fallback models on agent nodes.", "Fallback models contain provider failure.", facets=I),
 },
 "dify": {
  "MAL-19": a(2, "Apps exposed as MCP servers with a per-app credential (api/controllers/mcp/mcp.py)."),
  "MAL-20": a(2, "Grounded end-user apps and builder generators."),
  "DEL-01": a(0, NO_AI), "DEL-04": a(2, "AI generators draft prompts, code and workflow steps (api/core/llm_generator)."),
  "LRN-05": a(0, NO_AI), "LRN-06": a(0, NO_AI), "LRN-07": a(0, "Annotations are curated by people."),
  "LRN-08": na("agent_mutations is false."), "EXP-05": a(0, NO_AI),
  "GOV-09": a(1, "Agent tools run with credentials configured by the builder, shared across end users."),
  "GOV-10": na("GOV-10 is not applicable."), "GOV-11": na("GOV-11 is not applicable."),
  "ARC-08": up(2, "Load balancing with cooldown across credentials (api/core/model_manager.py).", "Cooldown acts as a breaker.", facets=I),
 },
 "librechat": {
  "MAL-19": a(1, "Consumes MCP; exposes no MCP server for agents."),
  "MAL-20": a(2, "Grounded chat with retrieval and tools for members."),
  "DEL-01": a(0, NO_AI), "DEL-04": a(0, NO_AI), "LRN-05": a(0, NO_AI), "LRN-06": a(0, NO_AI),
  "LRN-07": a(0, "Off by default.", available_score=3),
  "LRN-08": na("agent_mutations is false."), "EXP-05": a(0, NO_AI),
  "GOV-09": a(2, "Agent API keys, on-behalf-of token exchange for MCP and tool-call approvals (api/server/services/OboTokenService.js)."),
  "GOV-10": na("GOV-10 is not applicable."), "GOV-11": na("GOV-11 is not applicable."),
  "ARC-08": a(2, "Timeouts on provider calls (packages/api/src/endpoints/openai/config.ts); errors contained per conversation."),
 },
 "hermes-agent": {
  "MAL-19": up(2, "MCP server and ACP adapter (mcp_serve.py, acp_adapter).", "Typed tool registry."),
  "MAL-20": up(3, "Model-backed conversation across platforms; skills and memory authored in natural language.", "Broad coverage."),
  "DEL-01": up(1, "Requests arrive as chat turns.", "Skill creation records name and description."),
  "DEL-04": up(2, "Background review is a model lane that applies skill and memory changes.", "Autonomous by default."),
  "LRN-05": a(1, "The agent explains errors when asked; hermes doctor is rule-based."),
  "LRN-06": up(2, "A background fork proposes skill and memory updates from the conversation.", "GEPA ranks variants."),
  "LRN-07": up(3, "Model reflection after turns writes skills and memory by default.", "Learns from GEPA results."),
  "LRN-08": a(2, "AI-written skills pass scans, AST audits and a linter.", available_score=3, facets=IT),
  "EXP-05": a(1, "Creates skills for tasks it has done; no unprompted proposals."),
  "GOV-09": up(2, "Dangerous commands need approval with LLM risk classification; the agent acts with the user's authority.", "Approval floors."),
  "GOV-10": a(2, "Protected files and write scans; no declared scope or rate limit."),
  "GOV-11": up(2, "Ledger actor and injection scans on skill writes.", "Both present."),
  "ARC-08": a(3, "Fallback providers and credential pools contain provider failure, with tests.", facets=IT),
 },
 "openclaw": {
  "MAL-19": a(3, "MCP channel-bridge server and typed gateway protocol (src/mcp)."),
  "MAL-20": up(3, "Model-backed conversation across channels; configuration by natural language.", "Broad coverage."),
  "DEL-01": up(2, "/learn turns a request into a pending skill proposal (src/skills/workshop/learn-prompt.ts).", "Close to a specification."),
  "DEL-04": up(2, "Experience review drafts and applies skills.", "Autonomous by default."),
  "LRN-05": a(1, "The agent explains errors when asked; doctor checks are rule-based."),
  "LRN-06": up(2, "Experience review proposes skills from observed runs.", "Ranked when idle."),
  "LRN-07": up(3, "Model review of runs drafts skills unprompted by default.", "Autonomous mode."),
  "LRN-08": a(2, "AI-made proposals are scanned before apply; no evaluator ships."),
  "EXP-05": a(1, "Proposes skills for observed tasks only."),
  "GOV-09": a(3, "Pairing identities, exec approvals with previews, tool policies and idempotency keys for agent actions."),
  "GOV-10": a(2, "Proposal size and origin limits; no blast-radius limit."),
  "GOV-11": up(2, "Origin recorded and proposals scanned; auto-apply by default.", "Both present."),
  "ARC-08": a(3, "Model fallback attempts and configured provider fallback, tested.", facets=IT),
 },
 "opencode": {
  "MAL-19": a(2, "HTTP API, SDK and ACP; no MCP server for agents."),
  "MAL-20": up(2, "Model-backed coding conversation; agents generated from descriptions.", "Broad coverage."),
  "DEL-01": a(0, "AI works on users' code, not on OpenCode's own changes."),
  "DEL-04": up(1, "The team's GitHub agent is not a first-party evolution system (rule 12).", "Narrow AI lane."),
  "LRN-05": a(0, NO_AI), "LRN-06": a(0, NO_AI), "LRN-07": a(0, NO_AI),
  "LRN-08": na("agent_mutations is false."), "EXP-05": a(0, NO_AI),
  "GOV-09": a(2, "Permission rules preview actions with ask prompts; commands run with the user's ambient authority."),
  "GOV-10": na("GOV-10 is not applicable."), "GOV-11": na("GOV-11 is not applicable."),
  "ARC-08": a(2, "Provider calls retried with back-off (packages/opencode/src/session/retry.ts)."),
 },
 "openhands": {
  "MAL-19": a(2, "A UI tool lets agents drive the canvas; no MCP server for it."),
  "MAL-20": a(2, "Model-backed agent conversations through the canvas."),
  "DEL-01": a(0, NO_AI),
  "DEL-04": up(1, "Automations change users' repositories, not OpenHands itself.", "Operator-configured automations."),
  "LRN-05": a(0, "Run failure kinds are rule-based."), "LRN-06": a(0, NO_AI), "LRN-07": a(0, NO_AI),
  "LRN-08": na("agent_mutations is false."), "EXP-05": a(0, NO_AI),
  "GOV-09": a(2, "Confirmation policy defaults to never; with ConfirmRisky, an LLM security analyser classifies actions (openhands-sdk/openhands/sdk/conversation/state.py:123).", available_score=3),
  "GOV-10": na("GOV-10 is not applicable."), "GOV-11": na("GOV-11 is not applicable."),
  "ARC-08": a(3, "Fallback strategy on provider errors, tested (tests/sdk/llm/test_llm_fallback.py).", facets=IT),
 },
}


def migrate(system):
    path = os.path.join(ROOT, system, "assessment.json")
    with open(path) as handle:
        data = json.load(handle)
    if data.get("framework_version") == "0.5.0":
        sys.exit(f"{system}: already migrated")
    data["scope_facts"].update(FACTS[system])
    for cid in AIR:
        if system in AIR_SCORES:
            data["scores"][cid] = AIR_SCORES[system][cid]
        else:
            data["scores"][cid] = na("ai_features is false: " + FACTS[system]["ai_features"]["evidence"])
    for cid in READINGS:
        if system in AI_READ:
            data["scores"][cid]["ai"] = AI_READ[system][cid]
    data["framework_version"] = "0.5.0"
    with open(path, "w") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


if __name__ == "__main__":
    for system in SYSTEMS:
        migrate(system)
    print("migrated", len(SYSTEMS), "systems")
