# Codemetr Skills

Portable C# code-quality skills for **Claude Code**, **GitHub Copilot CLI** and **Codex CLI**, powered by
the [Codemetr .NET tool](https://github.com/codemetr/Codemetr.CSharp).

| Plugin | Skills |
| --- | --- |
| `codemetr-csharp` | `analyze`: measure and explain hotspots; `guard`: validate changes without weakening quality rules |

You do not need to name Codemetr or invoke a slash command. Once installed and
enabled, the skills can be selected by the agent for natural-language requests:

- "Zeige mir die Code-Metriken dieses C#-Projekts."
- "Welche Klassen haben eine hohe Komplexität oder Kopplung?"
- "Prüfe meine C#-Änderungen auf Codequalität und Grenzwertverletzungen."
- "Check whether this refactoring worsens our C# complexity metrics."

Selection depends on the client and model; these are routing cues, not mandatory
keyword hooks. Explicit skill invocation remains available when needed.

## Quick start

Requires the .NET 10 SDK and the separately installed `Codemetr.CSharp.Tool`.
If prerequisites are missing, the skills offer to install or restore them, wait
for confirmation, then verify setup and continue the requested task.
Marketplace commands work once these files are published on the default branch.
See the **[installation guide](INSTALL.md)** for tool setup, existing projects,
updates, local development and troubleshooting.

### Claude Code

```text
/plugin marketplace add codemetr/skills
/plugin install codemetr-csharp@codemetr-skills
```

Start a new session (or reload plugins), then invoke:

```text
/codemetr-csharp:analyze
/codemetr-csharp:guard
```

### GitHub Copilot CLI

In your terminal, using a current Copilot CLI with plugin support:

```bash
copilot plugin marketplace add codemetr/skills
copilot plugin install codemetr-csharp@codemetr-skills
```

Start a new Copilot session in your C# repository and ask, for example:
"Zeige mir die Code-Metriken dieses C#-Projekts."
Inside an interactive session, the equivalent commands start with
`/plugin marketplace add` and `/plugin install`.

### Codex CLI

Use a current Codex CLI with plugin marketplace support:

```bash
codex plugin marketplace add codemetr/skills
```

Open `/plugins`, select **Codemetr Skills**, and install `codemetr-csharp`.
Start a new session and ask to analyze C# code or run the Codemetr guard. The
plugin browser and installation UI depend on the host and CLI version.

Both marketplace manifests reference the same plugin and `SKILL.md` files.
Claude Code and Copilot CLI use `.claude-plugin/marketplace.json`; Codex uses
`.agents/plugins/marketplace.json` and a `.codex-plugin/plugin.json` compatibility
manifest. Copilot CLI compatibility follows GitHub's documented manifest support;
installation and skill activation have not yet been runtime-tested in Copilot.
Other clients may support the portable skills, but are not yet tested.

## A skill is not mandatory enforcement

Skills guide an agent; they do not automatically run after every edit and do not
install hooks. Keep a full check in required CI to enforce quality before merges.
See [the example workflow](examples/codemetr-guard.yml). It assumes the target
repository has committed a tool manifest containing Codemetr and an appropriate
`global.json`. This marketplace's own CI validates its packaging and smoke-tests
the published tool; it does not enforce a consuming project's quality gate.

## Contributing and validation

```bash
python -m unittest discover -s tests -v
```

CI checks marketplace consistency, plugin versions, skill metadata, references
and basic sensitive-file/token patterns. These checks are not a full secret
scanner or a substitute for review. Behavioral scenarios are in
`evals/evals.json`; they have not yet been benchmarked against live agents.

Never commit credentials, personal account details, machine-specific paths,
private reports or private source fixtures. See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE).
