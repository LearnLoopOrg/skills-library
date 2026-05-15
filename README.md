# skills-library — UvA AI Chat extension

Een Claude plugin marketplace die de **UvA AI Chat** uitbreidt met AI-nakijken voor docenten. Ontwikkeld vanuit de LearnLoop-pilot binnen het UvA-project *Slimmer Collegejaar* (2024–2026).

## Wat dit is

Een set Claude-skills die docenten direct kunnen aanroepen vanuit de UvA AI Chat (en vanuit Claude Desktop / Cowork) om:

1. een **rubric** te bouwen uit een beoordelingsformulier, opdrachtomschrijving of screenshot, en
2. **studentwerk te beoordelen** tegen die rubric, met per-cluster sub-agents die elk een deel van de rubric grondig nalopen, en als output een Excel-rapport met eindcijfer en onderbouwde motiveringen.

Net zoals skills in Claude Desktop automatisch triggeren op de juiste vraag, triggeren ze ook in de UvA AI Chat zodra die plugin-ondersteuning aanzet. Docent typt *"maak hier een rubric van"* of *"evalueer deze scriptie"* — de skill doet de rest.

## Structuur

```
skills-library/
├── .claude-plugin/
│   └── marketplace.json              ← marketplace-manifest
├── slimmer-collegejaar-plugin/       ← één plugin (later komen er meer)
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

`marketplace.json` is de single source of truth — elke plugin moet daar geregistreerd staan voordat de UvA AI Chat / Claude Desktop hem ziet.

## Plugins in deze marketplace

| Plugin | Wat het doet |
|---|---|
| [`slimmer-collegejaar`](./slimmer-collegejaar-plugin) | AI-nakijken toolkit. Bundelt `rubric-builder` (beoordelingsformulier → gestructureerde rubric) en `rubric-evaluator` (rubric + studentwerk → Excel-rapport met eindcijfer en per-criterium motivering mét bewijs uit het werk). |

## Installeren

In de UvA AI Chat of Claude Desktop / Cowork:

```
/plugin marketplace add LearnLoopOrg/skills-library
/plugin install slimmer-collegejaar@skills-library
```

Daarna triggeren de skills automatisch op vragen zoals:

- *"maak een rubric van dit beoordelingsformulier"*
- *"evalueer deze scriptie met de rubric"*
- *"nakijken volgens de rubric die we hadden gemaakt"*

## Bijdragen

Nieuwe plugins gaan in een eigen top-level folder met dezelfde structuur (`<plugin>/.claude-plugin/plugin.json` + `<plugin>/skills/<skill>/SKILL.md`) en moeten geregistreerd worden in `.claude-plugin/marketplace.json` — anders wordt de plugin niet gevonden.

## Licentie

MIT — zie `LICENSE`.

## Contact

LearnLoop · onderdeel van het UvA-project *Slimmer Collegejaar*.
