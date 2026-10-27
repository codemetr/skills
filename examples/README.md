# Consumer setup examples

The workflow in `codemetr-guard.yml` assumes a committed local tool manifest and
a compatible .NET 10 SDK selected by `global.json`. For a **new** repository
without a tool manifest, create one and install the published version:

```bash
dotnet new tool-manifest
dotnet tool install Codemetr.CSharp.Tool --version 0.1.0
dotnet tool restore
dotnet tool run codemetr-csharp -- --version
dotnet tool run codemetr-csharp -- check src --format text
```

`dotnet-tools.json` shows the resulting manifest shape. Commit the generated
`.config/dotnet-tools.json`; do not overwrite an existing project's manifest or
change its pin without approval. Then copy the example workflow into that
project's `.github/workflows/` directory and require its guard check before merge.
This marketplace repository is not the target C# repository.

For exploring 0.1.0 measurements with a local tool:

```bash
dotnet tool run codemetr-csharp -- analyze src --format json
dotnet tool run codemetr-csharp -- check src --include-metrics --format json
```

For an existing real Stryker report, optionally add
`--mutation-report reports/mutation.json` to `analyze`. Importing is not test
execution and the report's source correspondence must be checked separately.

See the [runnable sample and expected interpretation](https://github.com/codemetr/Codemetr.CSharp/tree/main/examples)
for partial types, dependency cycles, cognitive complexity, cohesion and a clearly
synthetic mutation-import example. These advisory measurements do not create
new default thresholds. Enabling `aggregatePartialTypes` is a separate policy
change, not an automatic consequence of upgrading the tool or plugin.
