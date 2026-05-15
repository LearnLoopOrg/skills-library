# Installeren

Twee manieren om deze skills te gebruiken.

## 1. Als Claude Desktop / Cowork plugin (aanbevolen)

Via de marketplace-registratie:

```
/plugin marketplace add LearnLoopOrg/skills-library
/plugin install slimmer-collegejaar@skills-library
```

Herstart Claude Desktop. De skills triggeren daarna automatisch wanneer je:

- een rubric of beoordelingsformulier deelt en zegt *"maak hier een rubric van"*
- een rubric.json + studentdocument hebt en zegt *"evalueer deze scriptie"*

## 2. Als losstaand Python-script (zonder Claude Desktop)

Voor docenten zonder Cowork-toegang:

```bash
git clone https://github.com/LearnLoopOrg/skills-library.git
cd skills-library/slimmer-collegejaar-plugin/skills/rubric-evaluator

pip install anthropic openpyxl
export ANTHROPIC_API_KEY=sk-ant-xxx

python scripts/run_demo.py \
  --rubric examples/sample-rubric.json \
  --student-work examples/sample-student-report.txt \
  --output examples/evaluation_report.xlsx
```

Open `evaluation_report.xlsx` voor het eindcijfer, per-cluster scores en per-criterium motiveringen.

## Vereisten

- **Plugin-route**: Claude Desktop (Mac/Windows/Linux) of Cowork met plugin-functionaliteit.
- **Python-route**: Python 3.10+ en een Anthropic API key (zie https://console.anthropic.com).

## Eigen rubric gebruiken

Twee opties:

1. Maak een `rubric.json` met de structuur uit `slimmer-collegejaar-plugin/skills/rubric-evaluator/examples/sample-rubric.json`.
2. Geef je beoordelingsformulier (PDF, screenshot, Word-doc) aan de `rubric-builder` skill in Claude Desktop en laat 'm de JSON voor je genereren.

**Wat moet kloppen in een rubric:**

- Cluster-gewichten tellen op tot `total_points`.
- Criteria-gewichten binnen een cluster tellen op tot het cluster-gewicht.
- Elk criterium heeft minimaal 3 levels met observeerbare indicators.
