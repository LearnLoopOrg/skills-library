# skills-library — LearnLoop Claude marketplace

Een marketplace van plugins en skills gebouwd door LearnLoop voor Claude Cowork, Claude Code en Claude Desktop. Ontwikkeld vanuit de LearnLoop-pilot voor het UvA-project *Slimmer Collegejaar* (2024–2026).

## Wat is dit repo?

Een Claude **plugin marketplace** — één git-repo met daarin één of meer plugins, elk met skills, commands, en (optioneel) MCP servers. Cowork-gebruikers installeren een plugin met één klik; Claude Code-gebruikers registreren de marketplace en installeren plugins eruit.

## Structuur

```
skills-library/
├── .claude-plugin/
│   └── marketplace.json              ← lijst van alle plugins in dit repo
├── slimmer-collegejaar-plugin/       ← één folder per plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       ├── rubric-builder/
│       │   └── SKILL.md
│       └── rubric-evaluator/
│           ├── SKILL.md
│           ├── agents/
│           ├── scripts/
│           └── examples/
└── README.md
```

Het marketplace-manifest in `.claude-plugin/marketplace.json` is de single source of truth — elke plugin-folder moet daar geregistreerd staan.

## Plugins in deze marketplace

| Plugin | Wat het doet |
|---|---|
| [`slimmer-collegejaar`](./slimmer-collegejaar-plugin) | AI-nakijken toolkit: zet een beoordelingsformulier om in een rubric en beoordeelt studentwerk per cluster met sub-agents. Output is een Excel-rapport met eindcijfer, per-criterium scores en motiveringen met bewijs uit het studentwerk. |

## Installeren

In Claude Cowork of Claude Code:

```
/plugin marketplace add LearnLoopOrg/skills-library
/plugin install slimmer-collegejaar@skills-library
```

Daarna triggeren de skills automatisch wanneer je:

- een beoordelingsformulier of opdrachtbeschrijving deelt en zegt *"maak hier een rubric van"*
- een rubric + studentdocument hebt en zegt *"evalueer deze scriptie"*

## Zonder Claude Desktop / Cowork

Voor docenten zonder Claude Desktop is er ook een Python-versie van de evaluator-flow — zie [`INSTALL.md`](./INSTALL.md).

## Bijdragen

Nieuwe plugins gaan in een eigen top-level folder. Registreer ze altijd in `.claude-plugin/marketplace.json` voordat je merget — Claude vindt alleen plugins die daar staan.

## Licentie

MIT — zie `LICENSE`.

## Contact

LearnLoop · onderdeel van UvA-project *Slimmer Collegejaar*.
