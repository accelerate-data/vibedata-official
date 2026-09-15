# Roll Back a Release

A release is a tag in the public GHCR package + its matching CLI binaries + a GitHub Release on `accelerate-data/vibedata-official`. There is no control plane pushing to operator hosts — rollback is whatever an operator pulls next.

## Primary — yank the latest GitHub Release

Mark the latest GitHub Release on `vibedata-official` as a non-latest (or draft) entry. The previous release becomes "Latest" again. New installs pick it up; already-installed operators are unaffected until they `vibedata update compose`.

## Forward-fix as a new release

If the bad version's content must be replaced rather than hidden, mint and promote a new candidate via `release.yml` → `deploy.yml`. It can carry the previous good digest under a new version. This is a forward release, not an in-place rollback.
