# Update Studio (Local Docker)

Updating selects new images while preserving `DATA_DIR`.

1. Install the `vibedata` binary for the target version (CLI version selects the release — pairing is strict 1:1).
2. Run:
   ```bash
   vibedata update compose
   ```
3. Confirm the services are back up:
   ```bash
   docker compose ps
   ```

`update compose` does not change the `DATA_DIR` root. If it cannot pull images, regenerate assets, start containers, or complete migrations, it exits with a **blocked** state (exit code `3`) and leaves existing durable state intact for retry.
