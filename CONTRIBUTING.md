# Contributing to Accelerate Data

Thank you for contributing. This guide covers the workflow and standards for all repositories in the `accelerate-data` organization.

## Getting Started

1. Clone the repository and install dependencies per its README.
2. Create a branch from `main` using the naming conventions below.
3. Make your changes, push, and open a pull request.

## Branch Naming

| Prefix | Use |
|---|---|
| `feature/VD-XXX-short-desc` | New functionality |
| `fix/VD-XXX-short-desc` | Bug fixes |
| `docs/topic` | Documentation only |
| `chore/short-desc` | Tooling, CI, dependencies |
| `refactor/short-desc` | Code restructuring with no behavior change |

## Worktree Workflow

Never switch branches on the main repository checkout. Every feature gets its own git worktree — an isolated copy of the codebase with its own branch, files, and environment.

See the full guide: [guides/worktree-workflow.md](https://github.com/accelerate-data/vd-docs-engineering-framework/blob/main/guides/worktree-workflow.md)

## Linear-Driven Lifecycle

All work is tracked in Linear. The typical flow:

1. **Create** a Linear issue (`/create-linear-issue`) describing the work.
2. **Implement** the issue (`/implement-linear-issue`), referencing it in commits and PRs.
3. **Close** the issue (`/close-linear-issue`) once the PR merges.

## Pull Request Requirements

- **Title format**: `VD-XXX: Short description of change`
- **Body**: Include `Fixes VD-XXX` to auto-link the Linear ticket.
- **CI**: All checks must pass, including CodeQL and `claude-code-review`.
- **Review**: Requires AI review (claude-code-review) plus at least 1 human approval.
- **Merge strategy**: Squash merge to `main`.

## Code Standards

- Follow the linting and formatting rules configured in the repository.
- Write tests for new functionality. Maintain or improve existing coverage.
- Do not commit secrets, credentials, or `.env` files.

## Documentation

Follow the README-first principle: update the README before or alongside code changes. For design documents, specifications, and proposals, use the `doc-skills` plugin.

## Marketplace Plugins

For plugins and extensions, see the [Plugin Marketplace](https://github.com/accelerate-data/plugin-marketplace).

## Questions

Open an issue or reach out to the maintainers if anything is unclear.
