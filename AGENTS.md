# Repository instructions

- Keep skill content portable; host-specific packaging belongs in manifests.
- Claude and Codex manifests must resolve to the same plugin and skill files.
- Keep the two plugin manifest versions synchronized. Tool and plugin versions
  are independent; do not update a consumer's pinned tool without approval.
- Do not claim a skill or prompt guarantees enforcement. Required CI is the gate.
- Guard skills must preserve user configuration, baseline ratchets and changes.
- Never commit real credentials, personal account information, private fixtures
  or machine-specific paths. Use synthetic examples and secret names only.
- Run `python -m unittest discover -s tests -v` after packaging changes, and
  `claude plugin validate .` when Claude Code is available.
- Describe static validation and live behavioral evaluation separately. Never
  claim host compatibility was runtime-tested when only files were checked.
