# Installation

[Back to README](README.md)

## 1. Prerequisites

- A current Claude Code, GitHub Copilot CLI or Codex CLI with plugin marketplace support.
- The **.NET 10 SDK**, available from https://dotnet.microsoft.com/download/dotnet/10.0.
- Network access for marketplace downloads and NuGet package installation.
- A C# repository to analyze. The Codemetr tool's source code is not required.

Verify your SDK from the target C# repository:

```bash
dotnet --version
```

An existing `global.json` may select a different SDK. Preserve the project's
configuration; do not replace it just to install this plugin.

## 2. Install the Codemetr tool

Marketplace installation provides skill instructions, not the executable. The
skills proactively offer to install or restore missing prerequisites, explain
the proposed commands and their impact, and wait for confirmation. Once approved,
they perform the setup, verify it and continue the requested analysis or check.
They do not install software, update tool versions or change projects silently.
You can also use the manual steps below.

### Recommended: repository-local installation

Run from the **C# repository you want to analyze**, not this marketplace checkout.
If there is no existing tool manifest:

```bash
dotnet new tool-manifest
dotnet tool install Codemetr.CSharp.Tool --version 0.1.0
dotnet tool run codemetr-csharp --help
```

If a tool manifest already exists, do not recreate it. If it already declares
Codemetr, restore the declared version:

```bash
dotnet tool restore
dotnet tool run codemetr-csharp --help
```

If the manifest exists but does not contain Codemetr, use just the install command
above. Review and commit the manifest changes if the team should share the tool.
Installation and restoration use your configured NuGet sources.

### Alternative: global installation

```bash
dotnet tool install --global Codemetr.CSharp.Tool --version 0.1.0
codemetr-csharp --help
```

The executable must be on your shell's `PATH`. When both local and global
installations exist, prefer `dotnet tool run codemetr-csharp` to select the
repository's declared version.

## 3. Install the plugin

GitHub installation requires these marketplace files to be published on the
repository's default branch. No NuGet publishing credentials are needed to
install the public tool or plugin.

### Claude Code

Inside a Claude Code session:

```text
/plugin marketplace add codemetr/skills
/plugin install codemetr-csharp@codemetr-skills
/plugin install codemetr-csharp-cover@codemetr-skills
```

Start a new session, or reload plugins using the command supported by your
Claude Code version. From the target C# repository, invoke:

```text
/codemetr-csharp:analyze
/codemetr-csharp:guard
/codemetr-csharp-cover:coverage
/codemetr-csharp-cover:coverage-guard
```

### GitHub Copilot CLI

In your terminal:

```bash
copilot plugin marketplace add codemetr/skills
copilot plugin install codemetr-csharp@codemetr-skills
copilot plugin list
```

Alternatively, inside an interactive Copilot session:

```text
/plugin marketplace add codemetr/skills
/plugin install codemetr-csharp@codemetr-skills
```

Start a new session in the target C# repository and use a natural-language
request such as "Prüfe meine C#-Änderungen auf Codequalität." Copilot CLI reads
the existing `.claude-plugin/marketplace.json` and plugin manifest, so no separate
Copilot manifest is required. This is the Copilot **CLI** setup, not a VS Code
extension setup. Compatibility is based on GitHub documentation; installation
and automatic skill activation have not yet been runtime-tested in Copilot.

### Codex CLI

In your terminal:

```bash
codex plugin marketplace add codemetr/skills
```

Launch Codex, open `/plugins`, select **Codemetr Skills** and install
`codemetr-csharp`. Start a new session in the target C# repository and ask, for
example:

```text
Use the Codemetr analyze skill to explain this repository's C# hotspots.
```

```text
Use the Codemetr guard skill to check my C# changes without changing our rules
or baseline.
```

Plugin browsing and installation vary by host and CLI version. The marketplace
registration command alone does not mean the plugin has been installed.

## Use natural-language requests

In any of these clients, you can ask without naming the tool or skill:

```text
Zeige mir die Code-Metriken dieses C#-Projekts und erkläre die Hotspots.
```

```text
Prüfe, ob meine C#-Änderungen unsere Komplexitätsgrenzen verletzen.
```

The first request fits `analyze`; the second fits `guard`. English equivalents
work as well. The client/model selects skills using their descriptions and the
task context, not a deterministic keyword match. A plugin must be installed and
enabled in the session. If it is not selected, invoke the skill explicitly or
ask the agent to use it. This does not create automatic hooks after every edit.

## Coverage plugin

`codemetr-csharp-cover` needs its own tool, `Codemetr.CSharp.Cover.Tool`, and a
coverage engine in every test project. From the target C# repository root, with
an existing manifest (otherwise `dotnet new tool-manifest` first):

```bash
dotnet tool install Codemetr.CSharp.Cover.Tool --version 0.1.1
dotnet tool run codemetr-csharp-cover doctor --format text
```

`doctor` lists each test project with its platform and engine, and prints the
exact command for anything missing, for example:

```bash
dotnet add tests/Shop.Tests/Shop.Tests.csproj package coverlet.collector   # VSTest: xUnit v2, NUnit, MSTest
dotnet add tests/Shop.Api.Tests/Shop.Api.Tests.csproj package coverlet.MTP # Microsoft.Testing.Platform, 10 or later
```

Adding a package changes the test project; review and commit it like any other
change. The skills ask before running these commands. Then verify:

```bash
dotnet tool run codemetr-csharp-cover analyze --format text
dotnet tool run codemetr-csharp-cover check --base origin/main --format text
```

`analyze` never fails on findings; `check` returns 0 passed, 1 findings
(including failed tests), 2 input error or untrustworthy coverage evidence.
`codemetr-cover.json` sets thresholds and `codemetr-cover.baseline.json` records
coverage floors; changing either needs approval. For CI, adapt the
[coverage workflow](examples/codemetr-cover-guard.yml).

Example requests: "Wie hoch ist die Testabdeckung dieses Projekts?" fits
`coverage`; "Prüfe, ob meine Änderungen durch Tests abgedeckt sind" fits
`coverage-guard`.

## 4. Verify the tool and scope

For a local tool, from the target C# repository root:

```bash
dotnet tool run codemetr-csharp analyze --format text
dotnet tool run codemetr-csharp check --format text
```

For a global installation, omit `dotnet tool run`.

- `analyze` reports findings but does not fail the process for quality violations.
- `check` returns **0** for passed, **1** for guard findings or stale baseline
  entries, and **2** for input/usage errors.
- A failed quality check can mean the installation works but the source does not
  meet the configured limits. Do not automatically loosen rules or create a
  baseline to make it pass.

Skills are advisory, not automatic hooks or mandatory enforcement. To protect
merges, copy the [CI example](examples/codemetr-guard.yml), adapt it to the
target repository, and make its `guard` status check required in GitHub.

## Updates

Plugin and NuGet-tool versions are independent. Updating one does not update the
other.

For Claude Code, inside a session:

```text
/plugin marketplace update codemetr-skills
/plugin update codemetr-csharp@codemetr-skills
```

For GitHub Copilot CLI, refresh the catalog and update the plugin:

```bash
copilot plugin marketplace update codemetr-skills
copilot plugin update codemetr-csharp@codemetr-skills
```

For Codex, refresh the marketplace and use `/plugins` to review available updates:

```bash
codex plugin marketplace upgrade codemetr-skills
```

Start a new session after updating. Only update a repository's pinned tool
version deliberately; review the resulting tool-manifest diff. Do not substitute
a newer global tool for the repository's declared version.

## Local development before publication

From this marketplace checkout, validate and load Claude's plugin directly:

```bash
claude plugin validate .
claude plugin validate ./plugins/codemetr-csharp
claude --plugin-dir ./plugins/codemetr-csharp
```

Alternatively, register the local marketplace inside Claude Code, substituting
your checkout location for the placeholder:

```text
/plugin marketplace add <marketplace-checkout>
/plugin install codemetr-csharp@codemetr-skills
```

For Codex, register the local checkout from its root, then install via `/plugins`:

```bash
codex plugin marketplace add .
```

Local marketplace registration changes your client configuration. Direct Claude
loading with `--plugin-dir` is session-scoped. Avoid registering both a local and
remote marketplace with the same name; remove the development registration
before switching to GitHub.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Marketplace cannot be found | The files must be published on GitHub. For unpublished work, use a local checkout as described above. |
| Codex has no plugin commands or browser | Update to a CLI version supporting plugin marketplaces; confirm with `codex plugin marketplace --help`. |
| Copilot has no plugin commands | Update GitHub Copilot CLI and check `copilot plugin --help`. These instructions do not target the legacy `gh copilot` extension. |
| Claude skill is missing | Verify the plugin is installed and enabled, then start a new session. |
| Tool command is missing | Restore the local tool from the target repository, or check `PATH` for a global installation. |
| SDK or runtime error | Check the installed .NET 10 SDK and the target repository's `global.json`. |
| NuGet download fails | Check network access and configured NuGet sources. Never paste credentials into chat or commit them to this repository. |
| Guard exits with 1 | Inspect the report: this is a quality finding, not necessarily an installation failure. |
| Guard exits with 2 | Fix the reported input, configuration or syntax error before interpreting quality results. |

## References

- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Codex plugins](https://developers.openai.com/codex/plugins)
- [GitHub Copilot CLI plugin installation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)
- [GitHub Copilot CLI manifest support](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Codemetr tool documentation](https://github.com/codemetr/Codemetr.CSharp)
- [Codemetr cover tool documentation](https://github.com/codemetr/Codemetr.CSharp.Cover)
- [Security guidance](SECURITY.md)
