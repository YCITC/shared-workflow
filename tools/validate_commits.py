#!/usr/bin/env python3
"""
Commit message validator

Validates that commits follow Conventional Commits standard.
"""

import subprocess
import re
import sys
import os
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_pr_commits():
    """Get commits in current PR or branch"""
    try:
        # Use GitHub Actions base ref if available, otherwise default to main
        base_branch = os.environ.get('GITHUB_BASE_REF', 'main')

        # Try to get commits from GitHub PR environment
        base_ref = subprocess.run(
            ["git", "merge-base", "HEAD", f"origin/{base_branch}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Get commits since base
        result = subprocess.run(
            ["git", "log", f"{base_ref}..HEAD", "--pretty=format:%H|||%s"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|||')
                if len(parts) == 2:
                    commits.append({
                        'hash': parts[0][:8],
                        'message': parts[1]
                    })

        return commits

    except subprocess.CalledProcessError:
        print("⚠️  Warning: Could not get PR commits")
        return []


def is_conventional_commit(message):
    """
    Check if commit message follows Conventional Commits

    Valid formats:
    - type: description
    - type(scope): description
    - type!: description (breaking change)
    - type(scope)!: description (breaking change with scope)
    """
    # Allow merge commits
    if message.startswith('Merge '):
        return True, "merge"

    # Allow automated commits
    if message.startswith('chore: bump version'):
        return True, "automated"

    # Check conventional commit format
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore|build|ci)(\([a-z0-9\-_]+\))?(!)?:\s.{1,}'

    if re.match(pattern, message, re.IGNORECASE):
        return True, "conventional"

    return False, "invalid format"


def validate_single_message(message):
    """Validate a single message (e.g. PR title)"""
    print(f"🔍 Validating message: \"{message}\"...\n")
    
    is_valid, error_reason = is_conventional_commit(message)
    
    if is_valid:
        print("✅ Message is valid!")
        return True
    else:
        print(f"❌ Invalid message format! Reason: {error_reason}\n")
        print_help()
        return False


def validate_commits():
    """Validate all commits in PR"""
    commits = get_pr_commits()

    if not commits:
        print("✅ No commits to validate (or could not read commits)")
        return True

    invalid_commits = []

    print(f"🔍 Validating {len(commits)} commit(s)...\n")

    for commit in commits:
        is_valid, commit_type = is_conventional_commit(commit['message'])

        if is_valid:
            print(f"✅ {commit['hash']}: {commit['message'][:60]}...")
        else:
            print(f"❌ {commit['hash']}: {commit['message'][:60]}...")
            invalid_commits.append(commit)

    print()

    if invalid_commits:
        print("❌ Invalid commit messages found!\n")
        print_help()
        return False

    print("✅ All commits follow Conventional Commits standard!")
    return True


def print_help():
    """Print conventional commits help"""
    print("Please use Conventional Commits format:\n")
    print("  feat: add new feature")
    print("  fix: resolve bug")
    print("  docs: update documentation")
    print("  chore: maintenance tasks")
    print("  refactor: code restructuring")
    print("  test: add or update tests")
    print("  style: formatting changes")
    print("  perf: performance improvements")
    print("\nWith optional scope:")
    print("  feat(dashboard): add dark mode")
    print("  fix(api): resolve timeout issue")
    print("\nBreaking changes:")
    print("  feat!: breaking API change")
    print("  fix(core)!: breaking fix")
    print("\nFor more info: https://www.conventionalcommits.org/")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate commit messages or PR title')
    parser.add_argument('--message', type=str, help='Validate a single message (e.g. PR title) instead of git log')
    
    args = parser.parse_args()
    
    if args.message:
        success = validate_single_message(args.message)
    else:
        success = validate_commits()
        
    sys.exit(0 if success else 1)
