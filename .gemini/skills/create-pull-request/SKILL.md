---
name: create-pull-request
description: Facilitates the creation of a new GitHub pull request. Use this skill when a user explicitly requests to create a pull request for current changes, or when a task requires submitting changes for review. It guides the user through providing necessary details like repository owner, name, title, head branch, and base branch.
---

# Create Pull Request

## Overview

This skill automates the process of creating a new pull request on GitHub by guiding the user through the required information and utilizing the `github.create_pull_request` tool provided by the GitHub MCP server. It also integrates Conventional Commits by suggesting a PR title based on the current branch's commit history.

## Workflow

To create a pull request, follow these steps:

1.  **Get Current Branch**: Automatically determine the current Git branch to suggest as the `head` branch.
2.  **Generate Suggested PR Title**: 
    *   Retrieve the `git log` for the current branch (e.g., `git log --oneline --no-merges -n 5`).
    *   Analyze the commit messages to synthesize a single, concise Pull Request title that adheres to Conventional Commits specifications (`<type>(<scope>): <subject>`). Focus on the most recent or significant changes if multiple commits exist.
    *   Present the suggested title to the user for confirmation or modification.
3.  **Gather PR Details**: Prompt the user for the following information:
    *   **Repository Owner**: The GitHub username or organization that owns the repository.
    *   **Repository Name**: The name of the repository.
    *   **Title**: The suggested title (from Step 2) will be pre-filled, but the user can override it.
    *   **Head Branch**: The branch containing your changes (defaults to current branch from Step 1).
    *   **Base Branch**: The branch to merge changes into `main-candidate`.
    *   **Body (Optional)**: A description for the pull request.
4.  **Create Pull Request**: Use the `github.create_pull_request` tool with the collected details.
5.  **Report Result**: Provide feedback to the user with the pull request URL upon successful creation.

## Parameters

The following parameters are required to create a pull request:

*   **`owner`**: (Required) Repository owner (username or organization).
*   **`repo`**: (Required) Repository name.
*   **`title`**: (Required) Pull request title. A suggested title will be generated from `git log`, but can be overridden by the user.
*   **`head`**: (Required) Branch containing changes (e.g., `feature/my-new-feature`).
*   **`base`**: (Required) Branch to merge into `main-candidate`.
*   **`body`**: (Optional) Pull request description.

## Example

**User Request**: "Help me create a pull request for the `valteq/marlin` repository, targeting the `main-candidate` branch."

**Agent Action**:
1.  Automatically gets current branch (e.g., `feat/my-awesome-feature`).
2.  Reads `git log` and suggests a title like `feat(new-feature): implement awesome new functionality`.
3.  Prompts user to confirm/modify the suggested title, and provide `owner`, `repo`, `base` if not already specified.
4.  Calls `github.create_pull_request` with the confirmed title and other parameters.
5.  Reports the success and the URL of the new pull request.
