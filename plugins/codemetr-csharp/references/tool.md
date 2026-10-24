# Codemetr tool reference

## Prerequisites and setup

The plugin contains instructions, not a tool binary. The source of
`Codemetr.CSharp` is not required. Check `dotnet --version` and the repository's
`global.json`, existing local tool manifests and documented installation first.
The published tool requires .NET 10.

## Offer and perform missing setup

Do not stop at saying a dependency is missing. Offer to install or restore it:

1. Identify the missing prerequisite and describe the exact commands, download
   source, version, network access and scope (repository-local or machine-wide).
   Explain any tool-manifest or SDK changes before requesting confirmation.
2. Prefer restoring the existing pinned tool, then adding a repository-local
   tool if none is declared. Offer a global installation as an alternative, not
   an unannounced fallback. Bundle the required steps into one clear proposal.
3. Wait for explicit confirmation. Then execute the approved commands using
   the host's normal permissions. Installing this plugin is not installation
   consent for other software. Do not bypass a sandbox or elevation prompt.
4. Verify `dotnet --version` and the selected tool's `--help`, then continue the
   original analyze/check task. If setup fails, explain the failure rather than
   silently changing the version, package source or installation scope.

If the .NET 10 SDK is missing, inspect the OS and existing `global.json`. Propose
an OS-appropriate installation using Microsoft's official .NET download guidance:
https://dotnet.microsoft.com/download/dotnet/10.0. On Windows, for example,
`winget install --id Microsoft.DotNet.SDK.10 --exact --source winget` may be
offered if WinGet is available. Explain any elevation or system-wide impact;
never modify `global.json` or run a downloaded installer without approval.
If no supported installation method is available in the current environment,
offer manual setup instructions and resume verification when it is complete.

Prefer an existing repository-local tool version. With user approval, a new
local installation can be created from the target repository root:

```bash
dotnet new tool-manifest
dotnet tool install Codemetr.CSharp.Tool --version 0.0.1
dotnet tool run codemetr-csharp --help
```

Do not create or overwrite a manifest that already exists. If the tool is
already declared but not restored, ask before running `dotnet tool restore`.
Do not automatically update a pinned version. The plugin version and tool
version are independent; these instructions initially target tool `0.0.1`.

A global installation is an alternative, also requiring permission:

```bash
dotnet tool install --global Codemetr.CSharp.Tool --version 0.0.1
codemetr-csharp --help
```

Installing and restoring from NuGet requires network access. Analysis itself is
local and does not require uploading source. Package sources are determined by
the user's NuGet configuration; never ask for credentials in chat or write them
into the repository.

## Commands

Run from the target repository root. The examples assume a local tool:

```bash
dotnet tool run codemetr-csharp analyze --format json
dotnet tool run codemetr-csharp check --format json
dotnet tool run codemetr-csharp analyze src --type OrderService --format json
```

`analyze` reports metrics and violations but returns 0 unless there is an input
error. `check` is the gate: 0 passed, 1 findings or stale baseline, 2 input error.

`codemetr.json` configures limits, overrides, exclusions and type-resolution
context. `codemetr.baseline.json` records accepted debt. Neither file is required
for the default check. Changing either changes what the gate judges and needs
explicit approval. `baseline` is a mutating command, not a read-only report.

Metrics are signals, not proof of correctness. In particular, parse errors,
excluded/generated files, inactive preprocessor branches and unresolved external
types can limit the result. Run builds and tests separately when appropriate.

Upstream documentation: https://github.com/codemetr/Codemetr.CSharp
