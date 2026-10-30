# Member-size adoption

Use the target repository's existing tool and read its versioned documentation.
Published tool **0.2.0** provides codeLines, statementCount, memberHotspots,
maxMemberCodeLines and maxMemberStatements. Tool 0.1.0 does not. Plugin 0.3.1
supports both by checking availability; never silently upgrade a consumer pin.

With tool 0.2.0, analyse the intended source using
`codemetr-csharp analyze src --format json --top 10` (prefix with `dotnet tool run`
for a local installation). Inspect memberHotspots with exact source/overload identity.
Code lines and syntactic statements distinguish a long flat method from a short
branch-heavy one. They do not prove that a method has a single responsibility.

After explicit policy approval, a tool 0.2.0 configuration can include:

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
