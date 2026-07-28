# TASK

Generate comprehensive QA test artifacts using the attached project context and prompt templates.

---

# CONTEXT

Read and use the following files as the complete source of project information:

- `ALAMOS_Feature_Context.md`
- `ALAMOS_Project_Context.md`
- `ALAMOS_Testing_Context.md`

Understand the project, feature scope, workflows, business rules, integrations, and testing context before generating any output.

---

# PROMPT TEMPLATES

Use the following prompt templates exactly as provided:

- `FTC02-ComprehenciveTestCase.md` — Generate comprehensive Functional Test Cases.
- `API02-API Validation Tests.md` — Generate API Validation Tests.
- `API04-API Contract Testing.md` — Generate API Contract Testing scenarios and test cases.

Follow all instructions, constraints, formatting rules, and output requirements defined within each prompt template.

---

# TASK

Using the project context:

1. Analyze all attached context documents.
2. Generate comprehensive Functional Test Cases using `FTC02-ComprehenciveTestCase.md`.
3. Generate API Validation Tests using `API02-API Validation Tests.md`.
4. Generate API Contract Test Cases using `API04-API Contract Testing.md`.
5. Ensure all generated outputs are complete, consistent, and aligned with the documented requirements.

---

# OUTPUT

Generate the required artifacts in the format specified by each prompt template.

Save all generated files in the following folder:

`ALAMOS-Output`

Use the file naming conventions defined in the respective prompt templates. If no naming convention is specified, use clear, descriptive file names with a timestamp to avoid overwriting existing files.

---

# IMPORTANT

- Use **only** the information available in the provided context files.
- Do **not** make assumptions or invent undocumented functionality.
- If any requirement is unclear, incomplete, or ambiguous, mark it as **Needs clarification** instead of making assumptions.
- Ensure all generated files are production-ready and require no additional formatting or restructuring.
- Avoid duplicate coverage across Functional Test Cases, API Validation Tests, and API Contract Test Cases wherever possible while ensuring complete requirement coverage.