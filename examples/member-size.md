# Member-size adoption

Use the target repository's existing tool and read its versioned documentation.
Tool 0.1.0 has member complexity but no codeLines, statementCount, memberHotspots,
maxMemberCodeLines or maxMemberStatements. This plugin's 0.3.0 guidance is forward
compatible; do not install a local development package or silently upgrade a pin.

For a release explicitly supporting the feature, analyse the intended source with
`codemetr-csharp analyze src --format json --top 10` (prefix with `dotnet tool run`
for a local installation). Inspect memberHotspots with exact source/overload identity.
Code lines and syntactic statements distinguish a long flat method from a short
branch-heavy one. They do not prove that a method has a single responsibility.

After explicit policy approval, a feature-capable configuration can include:

```json
{ "rules": { "maxMemberCodeLines": 40, "maxMemberStatements": 25 } }
```

These values are illustrative choices, not defaults or universal recommendations.
Equality passes. Preserve existing rules, overrides and baseline ratchets. Explain
unsupported fields before making changes with an older version. Reformatting to
hide lines is not an appropriate fix.

No Cover data is imported by the static hotspot list. Measured zero coverage and
unavailable coverage differ; separate reports require compatible source evidence
before drawing combined conclusions. The upstream feature 007 follow-up plans
that source-bound join rather than implying it is already implemented.
