# Feishu wiki archive defaults (requirements-to-prd)

[中文](wiki-archive-defaults.md)

> **What this file is**: the **public** copy holds **placeholders** `<YOUR_*>` only. If you embed real `space_id`/parent tokens in **your** system prompt, do that via an **untracked local file** or a **private** fork—**never** push real tenant identifiers to a public repo.  
> **When you ship this skill**: recipients must supply **their** `space_id` and parent `wiki token` (or a parseable wiki URL). **Do not** assume they share your private targets.  
> When **switching teams or wiki spaces**, the **current user** must provide a new `space_id` and parent `wiki token`, or parse them from the wiki URL via `lark-cli wiki spaces get_node` (see [lark-wiki-SKILL.md](lark-wiki-SKILL.md)).

## Pre-flight checklist (before any write)

| Item | Notes |
|------|--------|
| Wiki space | Feishu **space_id** (numeric string); placeholders in table below. |
| Parent node | **parent_node_token** of the wiki node under which the PRD node is created (often the segment after `/wiki/` in the URL); placeholders in table below. |
| Product title | Wiki **title** for the new PRD node (aligned with product/project name in the requirement). |
| Local files | Main body **`PRD_REPORT.md`**; extra files under **`PRD_prompts/`** (file names → child doc titles; extension may be stripped by convention). |
| Identity | `lark-cli auth login` completed; user can create nodes and edit docs in the target space (see [lark-shared-SKILL.md](lark-shared-SKILL.md)). |

If you replace the placeholders below with real values (or skip this table entirely), the **current operator** (or URL parsing) must supply **space_id** and **parent_node_token**; alternatively pass only `--parent-node-token` and let the CLI resolve `space_id` (must stay consistent with an explicit `--space-id` when both are used).

## Recommended lark-cli Skills (aligned with maintainer bundle)

| Skill | Role |
|-------|------|
| `lark-wiki` | Create wiki nodes and tree structure |
| `lark-doc` | Write Markdown into the cloud doc bound to a node (**treat as required** alongside `lark-wiki` for this flow) |
| `lark-whiteboard` | Turn PRD Mermaid/flowcharts into Feishu whiteboards (optional) |
| `lark-shared` | Auth and identity |
| `lark-openapi-explorer` | Fallback to raw OpenAPI when shortcuts do not cover the need |

Full table and notes: [lark-cli.md](lark-cli.md) — the section **「写入飞书时的 Skill 组合（推荐）」** right after the CLI path intro (table is language-agnostic).

## Placeholders for public repos (put real values locally or in private config)

| Variable | Placeholder | Notes |
|----------|-------------|--------|
| `space_id` | `<YOUR_SPACE_ID>` | Your target wiki space ID (numeric string) |
| `parent_node_token` | `<YOUR_PARENT_NODE_TOKEN>` | Parent wiki node token (often the segment after `/wiki/` in the URL) |

> Do **not** commit real `space_id` or wiki tokens to **public** Git. Maintainers may copy this table into a private prompt or a local `*.local.md` (and `.gitignore` it). When Feishu structure changes, update your local table or CLI args only.

## Archive flow (logical order)

Details and flags follow **`lark-wiki`** / **`lark-doc`** Skills and CLI (local copies: [lark-wiki-SKILL.md](lark-wiki-SKILL.md), [lark-doc-SKILL.md](lark-doc-SKILL.md)).

1. **Create the main PRD doc node**  
   - Run `wiki +node-create` under the default parent (e.g. `--space-id`, `--parent-node-token`, `--title` = product name or user-provided title).  
   - Capture `node_token`, `obj_token` (bound docx).

2. **Fill the main document**  
   - Push **`PRD_REPORT.md`** into the cloud doc from step 1 (Markdown → doc shortcuts per `lark-doc`, e.g. create/update commands; **follow your installed CLI version**).

3. **Attach `PRD_prompts/` children**  
   - For each file, `wiki +node-create --parent-node-token <main_PRD_node_token> --title "<child title>"`.  
   - Then write each file’s body into the corresponding cloud doc.

4. **Verify**  
   - In Feishu wiki, expand the parent and confirm hierarchy and readable bodies.

## Relation to demo regression

- **`demo/TEST-RUN.md` / `demo/README.md`**: regression covers **Markdown PRD gold file + section checklist only**; it does **not** run `lark-cli` or write to Feishu.  
- To validate “archive to Feishu”, run the steps above in a logged-in, permitted environment and record results separately (e.g. a `TECH-TEST` pattern used elsewhere in the repo).
