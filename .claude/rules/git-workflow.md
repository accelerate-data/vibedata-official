# Git Workflow

## Branches

- Do not commit directly to `main`.
- Create a feature branch for every change and merge through a pull request.
- Keep pull requests focused on one repository concern at a time.

## PR Format

- Title: `<issue-id>: short description` when the change is tracked
- Body: include the purpose of the change, validation performed, and any follow-up work

## Safety

- Never force-push `main`.
- Do not bypass branch protection.
- Keep `CODEOWNERS` aligned with the set of maintainers who are allowed to merge or push protected changes.
