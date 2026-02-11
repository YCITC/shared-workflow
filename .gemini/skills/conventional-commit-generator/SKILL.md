---
name: conventional-commit-generator
description: Generates a conventional commit message based on staged Git changes and performs the commit. Includes checks for branch naming and requires a ClickUp Task ID.
---

# Conventional Commit Generator

## Overview

This skill automates the process of creating conventional commit messages by analyzing staged Git changes, validating the current branch, and ensuring a ClickUp Task ID is included.

## Workflow

Your task is to generate a conventional commit message based on the staged code changes in the repository.
**Automatically run `git diff --staged` to obtain the code changes, generate the commit message, and then execute `git commit -m <message>` to complete the commit.**
Before committing, check the current git branch by running `git branch --show-current`. If the branch is `main` or `main-candidate`, prompt the user to switch to a recommended feature or fix branch (e.g., `feat/xxx` or `fix/xxx`) before proceeding. Only continue with the commit if the branch is appropriate.
The commit message should be concise, descriptive, and adhere to the Conventional Commits specification. The agent will handle the entire commit process automatically.

### Steps for Conventional Commit Automation
- Step 1: Check ClickUp Task ID
    - Verify if a ClickUp Task ID (format: CU-xxxxxx) is provided.
    - If not provided, prompt the user to supply one.
- Step 2: Check Current Branch
    - Run `git branch --show-current` to get the current branch name.
    - If the branch is main or main-candidate, prompt the user to switch to a feat/* or fix/* branch and abort the process.
    - If the branch is feat/* or fix/*, continue.
- Step 3: Get Staged Changes
    - Run `git diff --staged` to get all staged code changes.
- Step 4: Generate Conventional Commit Message
    - Automatically generate the commit message based on the diff and Conventional Commits specification.
        - type: feat, fix, docs, style, refactor, perf, test, chore, build, ci, revert
        - scope: affected area (optional)
        - subject: concise description
        - body: detailed explanation (optional)
        - footer: must include ClickUp Task ID
- Step 5: Execute Commit
    - Run `git commit -m "<message>"` to complete the commit.
- Step 6: Report Result
    - Provide feedback to the user with the commit result and message.

### Branch Structure

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready releases. Protected branch. |
| `main-candidate` | Staging/development branch for testing before release. |
| `feat/*`, `fix/*` | Feature and bugfix branches |

### Commit Message Structure:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Rules:

*   **type**: Must be one of the following:
    *   `feat`: A new feature
    *   `fix`: A bug fix
    *   `docs`: Documentation only changes
    *   `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semicolons, etc.)
    *   `refactor`: A code change that neither fixes a bug nor adds a feature
    *   `perf`: A code change that improves performance
    *   `test`: Adding missing tests or correcting existing tests
    *   `chore`: Other changes that don't modify src or test files (e.g., build process, auxiliary tools, libraries)
    *   `build`: Changes that affect the build system or external dependencies (e.g., gulp, npm)
    *   `ci`: Changes to our CI configuration files and scripts (e.g., Travis, Circle)
    *   `revert`: Reverts a previous commit
*   **scope**: (Optional) A short phrase describing the section of the codebase affected. Use a specific and relevant noun (e.g., `api`, `auth`, `ui`, `docs`, `config`, `server`, `client`, `deps`).
*   **subject**: A concise, imperative, present-tense description of the change. Do not capitalize the first letter and do not add a period at the end.
*   **body**: (Optional) A longer description providing more context about the change. Use imperative, present tense. Explain the motivation for the change and any relevant context.
*   **footer**: (Required) Include the ClickUp Task ID in the format `CU-xxxxxx`. You may also include any relevant issue references (e.g., `ClickUp Task: CU-123abc`) or breaking changes (e.g., `BREAKING CHANGE: description of the change`).

### Example:

**Input (Code Changes/Diff):**

```diff
diff --git a/src/app.py b/src/app.py
index abc1234..def5678 100644
--- a/src/app.py
+++ b/src/app.py
@@ -10,6 +10,10 @@
 def hello_world():
     return {
         "message": "Hello, World!"
    }

+@app.get("/greet/{name}")
+async def greet_user(name: str):
+    return {"message": f"Hello, {name}!"}

```

**Expected Output:**

```text
feat(api): add a new greeting endpoint

This commit introduces a new `/greet/{name}` endpoint that returns a personalized greeting message.

ClickUp Task: CU-123abc
```