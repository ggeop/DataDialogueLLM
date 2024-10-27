# Release Strategy

## Overview
This document describes the release process for our project. We use semantic versioning with automated releases based on conventional commits.

## Table of Contents
1. [Version Numbering](#version-numbering)
2. [Branch Strategy](#branch-strategy)
3. [Release Process](#release-process)
4. [Commit Convention](#commit-convention)
5. [Automated Releases](#automated-releases)

## Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH) automatically calculated from commit messages:

- MAJOR version for breaking changes
- MINOR version for new features
- PATCH version for bug fixes

## Branch Strategy
- `main` - Production code
- `develop` - Integration branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `hotfix/*` - Emergency fixes

## Release Process
Releases are automated using semantic-release and triggered by merging to main:

1. Write commits following conventional commit format
2. Create PR to develop
3. Merge develop to main when ready to release
4. Automated process:
   - Calculates version
   - Creates changelog
   - Creates GitHub release
   - Tags Docker images

## Commit Convention
Format: `<type>(<scope>): <description>`

Types:
- `feat`: New feature (MINOR version)
- `fix`: Bug fix (PATCH version)
- `feat!` or `BREAKING CHANGE`: Breaking change (MAJOR version)
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

Examples:
```bash
feat: add new user authentication endpoint
fix: resolve memory leak in worker process
feat!: redesign API response format
```

## Automated Releases
Releases are handled by GitHub Actions workflow:

```yaml
name: Release
on:
  pull_request:
    types: [closed]
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cycjimmy/semantic-release-action@v4
```

For more details, see:
- [Changelog](../../CHANGELOG.md)
- [Contributing Guidelines](../CONTRIBUTING.md)