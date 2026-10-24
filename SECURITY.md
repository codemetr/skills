# Security

Do not publish tokens, passwords, private keys, personal account information,
private code samples, or local machine paths in this repository or issue reports.
Secret names and public repository/package identifiers are safe to document;
their credential values are not.

Review skills before enabling them. These skills run the locally installed
Codemetr tool with the host's existing permissions. They do not bypass approvals,
install hooks, or upload source code. Package installation/restoration contacts
the configured NuGet sources and should be explicitly approved.

If a credential is exposed, revoke or rotate it immediately; deleting the latest
file does not remove it from Git history, caches or published artifacts.
Do not paste the credential into a public issue. Use GitHub's private vulnerability
reporting if enabled; otherwise contact a maintainer privately before sharing
details. Public issues should contain only a sanitized description.
