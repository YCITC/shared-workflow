# shared-workflows-YCITC

This repository contains reusable GitHub Actions workflows designed to streamline common CI/CD tasks across your projects.

## How to use the `pr-validation` reusable workflow

The `pr-validation` workflow helps ensure that your Pull Request titles adhere to Conventional Commits specifications and predicts the next version based on your commit messages.

### 1. Prerequisites for your repository

To use this reusable workflow, your repository must have the following:

-   A `VERSION` file at the root of your repository containing the current semantic version (e.g., `1.0.0`).
-   A `.github/workflows/` directory where you will call the reusable workflow.

### 2. Calling the `pr-validation` workflow

Create a new workflow file in your repository (e.g., `.github/workflows/pr-validation.yml`) with the following content:

```yaml
name: PR Validation

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  call-pr-validation:
    uses: YCITC/shared-workflow/.github/workflows/pr-validation.yml@main
    with:
      pull_request_title: ${{ github.event.pull_request.title }}
      pull_request_number: ${{ github.event.pull_request.number }}
      repo_owner: ${{ github.repository_owner }}
      repo_name: ${{ github.event.repository.name }}
```

**Explanation of inputs:**

-   `pull_request_title`: The title of the current Pull Request.
-   `pull_request_number`: The number of the current Pull Request.
-   `repo_owner`: The owner of the repository where the PR is located.
-   `repo_name`: The name of the repository where the PR is located.

### 3. Conventional Commit Guidelines

The `pr-validation` workflow validates PR titles against the [Conventional Commits](https://www.conventionalcommits.org/) specification. Here are some common types:

-   `feat:` - New feature (bumps minor version)
-   `fix:` - Bug fix (bumps minor version)
-   `docs:` - Documentation only (no version bump)
-   `chore:` - Maintenance (no version bump)
-   `BREAKING CHANGE:` - Breaking change (bumps major version)

**Examples:**

```
feat: add new trajectory smoother
fix: resolve modal centering issue
docs: update installation guide
chore: cleanup deprecated files
```

### 4. Versioning Automation

Once a PR is merged to `main` and passes validation, the version will be automatically bumped and a new release will be created.
