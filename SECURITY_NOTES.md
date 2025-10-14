Security notes — `.env` and secret rotation
===========================================

This project contained a `.env` file with secret keys. To avoid accidental exposure, follow these steps locally:

1) Ensure `.env` is in `.gitignore` (already present in this repo):

   - If not present, add `.env` to `.gitignore` and commit.

2) Stop tracking `.env` (run locally from the repository root):

   git rm --cached .env
   git commit -m "Remove .env from repo tracking"
   git push

3) (Optional) Purge `.env` from git history (destructive):

   # Requires git-filter-repo (recommended) or BFG. Example with git-filter-repo:
   git filter-repo --path .env --invert-paths
   git push --force

   NOTE: rewriting history is disruptive for collaborators. Coordinate first.

4) Rotate any exposed secrets immediately:

   - NVIDIA NIM API key: Revoke + re-create via https://build.nvidia.com/settings/api-keys
   - Twilio auth token / SID: Regenerate in Twilio Console
   - SMTP password: Rotate credentials at your mail provider

5) Use a secrets manager for production deployments (Vault, AWS Secrets Manager, GitHub Secrets, etc.) and avoid committing `.env`.

If you'd like, I can create a PR with the removal steps or help craft rotation emails for each provider.
