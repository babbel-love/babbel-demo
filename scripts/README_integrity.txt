🌐 Babbel Integrity Utilities

✅ Commands:

  make rebuild    # Fully resets the environment
  make check      # Runs tests + override scan
  make guard      # Scans for forbidden GPT-style patterns
  make hooks      # Ensures pre-commit hook is active
  make structure  # Show folder layout
  make reset      # Wipe cached test/temp data

📌 Notes:

- Prompts are locked to protocol enforcement.
- Tests block fallback contamination.
- CI + local hooks guarantee override integrity.

