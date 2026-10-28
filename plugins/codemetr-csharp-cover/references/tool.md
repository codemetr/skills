# Codemetr cover tool reference

## Prerequisites and setup

The plugin contains instructions, not a tool binary. The tool's source is not
required. Check `dotnet --version`, the repository's `global.json`, existing
local tool manifests and documented installation first. The published tool
`Codemetr.CSharp.Cover.Tool` (command `codemetr-csharp-cover`) requires .NET 10.

The tool runs the repository's tests with Coverlet. Every test project needs the
engine of its test platform as a package reference:

| Platform | Typical frameworks | Package |
| --- | --- | --- |
| VSTest | xUnit v2, NUnit, MSTest | `coverlet.collector` |
| Microsoft.Testing.Platform | xUnit v3, MSTest runner, NUnit runner | `coverlet.MTP` 10 or later |

The tool never edits projects. `doctor` lists every test project with platform,
framework, engine and the exact fix command for anything missing.

## Offer and perform missing setup

Do not stop at saying a dependency is missing. Offer to install or restore it:

1. Identify the missing prerequisite and describe the exact commands, download
   source, version, network access and scope (repository-local, one test
   project, or machine-wide). Explain manifest or project-file changes first.
2. Prefer restoring an existing pinned tool, then a repository-local tool if none
   is declared. Offer a global installation as an alternative, not an unannounced
   fallback. Bundle the required steps into one clear proposal.
3. Adding a Coverlet package changes the test project: show the `doctor` fix
   commands and ask before running them. Never swap a project's test platform or
   remove other packages to make coverage work.
4. Wait for explicit confirmation. Then execute the approved commands with the
   host's normal permissions. Installing this plugin is not consent for other
   software. Do not bypass a sandbox or elevation prompt.
5. Verify `dotnet --version`, the tool's `--help` and `doctor`, then continue the
   original task. If setup fails, explain the failure rather than silently
   changing the version, package source or installation scope.

If the .NET 10 SDK is missing, propose an OS-appropriate installation from
https://dotnet.microsoft.com/download/dotnet/10.0 (on Windows, for example,
`winget install --id Microsoft.DotNet.SDK.10 --exact --source winget`). Never
modify `global.json` or run a downloaded installer without approval.

With user approval, a new local installation from the target repository root:

```bash
dotnet new tool-manifest
dotnet tool install Codemetr.CSharp.Cover.Tool --version 0.1.0
dotnet tool run codemetr-csharp-cover --help
dotnet tool run codemetr-csharp-cover doctor --format text
```

Do not create or overwrite a manifest that already exists; add the tool to it
instead. If the tool is declared but not restored, ask before `dotnet tool
restore`. Do not update a pinned version automatically. Plugin and tool versions
are independent; these instructions target tool `0.1.0`. A global installation
(`dotnet tool install --global Codemetr.CSharp.Cover.Tool --version 0.1.0`) also
needs permission. Restoring from NuGet needs network access; measuring is local.
Never ask for credentials in chat or write them into the repository.

## Commands

Run from the target repository root. The examples assume a local tool:

```bash
dotnet tool run codemetr-csharp-cover doctor --format text
dotnet tool run codemetr-csharp-cover analyze --format json
dotnet tool run codemetr-csharp-cover analyze --below 80,60 --format json --output cover-worklist.json
dotnet tool run codemetr-csharp-cover analyze --member OrderService.Submit --format text
dotnet tool run codemetr-csharp-cover check --format json
dotnet tool run codemetr-csharp-cover check --base origin/main --format json
```

- `analyze` builds and runs the tests and reports coverage, the riskiest
  under-tested members (CRAP) and findings. It returns 0 unless input fails.
- `analyze --below LINE[,BRANCH]` is a worklist of every member (or `--level type`,
  `--level file`) under the thresholds, sorted by the lines and branches still
  missing. It is never a verdict (`"verdict": null`). stdout is limited by `--top`
  (default 10); `worklist.total` always counts everything; `--output FILE` holds
  the complete list. Read the file in parts instead of raising `--top` on a large
  repository.
- `check` is the gate: 0 passed, 1 findings (including failed tests), 2 input
  error or untrustworthy coverage evidence. `--base REF` judges changed lines
  against `merge-base(REF, HEAD)` plus uncommitted and untracked work; without it,
  the configured `diff.base` or `HEAD` (uncommitted work only) applies.
- `baseline` is mutating: it records or tightens `codemetr-cover.baseline.json`.
- `--reports GLOB --test-results GLOB` reads existing Cobertura/OpenCover files and
  TRX results instead of running tests; stale or foreign reports are refused.
- Arguments after `--` go to every test run. Filters, paths, `--type`,
  `--files-from` and a narrower `--test` make a run partial (`"complete": false`).

## Reading the report

- `provenance`: source (`run` or `reports`), commit, test projects with platform,
  engine and test counts, report files, the diff base, and `partial` reasons.
- `summary`: line and branch coverage, diff coverage, counts of findings,
  `unreported`, `excluded`, `skipped`, `tightenable`, `listed` and `omitted`.
- `violations`: `rule`, `status` (`new`, `worsened`, `baselined`), location,
  `value`/`limit`, `uncoveredLines` as `[start, end]` ranges, `branches` with the
  untaken condition, `testIn` (a suggested test file, not a guarantee), `message`
  and `hint`.
- `diff.uncovered`: changed lines without coverage per member.
- `unreported`: code without coverage data; under the default `zero` it counts as
  0 %. That usually means no test project covers it, not that coverage failed.
- `exclusions`: `[ExcludeFromCodeCoverage]` and config globs in effect.
- `inputErrors`: with exit 2, a code such as `coverletMissing`, `staleBuild`,
  `staleCoverage`, `missingTestResults` or `unresolvedBase` and a hint.

Coverage shows which lines ran, not whether a test asserts anything. Branch
counts from Cobertura are per line. Local functions that coverlet.MTP does not
instrument are listed as uninstrumented and not counted.

Upstream documentation: https://github.com/codemetr/Codemetr.CSharp.Cover
