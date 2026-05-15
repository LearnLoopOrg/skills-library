# Installeren

Twee manieren om deze skills te gebruiken.

## 1. Als Claude Desktop / Cowork skill

Plaats de mappen `rubric-builder/` en `rubric-evaluator/` in je skills-directory:

```bash
# macOS / Linux
cp -r rubric-builder rubric-evaluator ~/.claude/skills/

# Of via een plugin: maak een .plugin bundle die deze twee skills bevat
```

Herstart Claude Desktop. De skills triggeren automatisch wanneer je:

- een rubric of beoordelingsformulier uploadt en zegt *"maak hier een rubric van"*
- een rubric.json + studentdocument deelt en zegt *"evalueer deze scriptie"*

## 2. Als losstaand Python-script

Voor docenten zonder Claude Desktop:

```bash
pip install anthropic openpyxl
export ANTHROPIC_API_KEY=sk-ant-xxx

python rubric-evaluator/scripts/run_demo.py \
  --rubric examples/sample-rubric.json \
  --student-work examples/sample-student-report.txt \
  --output examples/evaluation_report.xlsx
```

Open `evaluation_report.xlsx` voor het eindcijfer, per-cluster scores en per-criterium motiveringen.

## Vereisten

- Python 3.10+
- Voor de skills-route: Claude Desktop (Mac/Windows/Linux) met skills-functionaliteit
- Voor de Python-route: een Anthropic API key (zie https://console.anthropic.com)

## Eigen rubric gebruiken

1. Zet je rubric in `rubric.json` met de structuur uit `examples/sample-rubric.json`, of
2. Geef je beoordelingsformulier (PDF, screenshot, Word-doc) aan de `rubric-builder` skill en laat 'm de JSON voor je genereren.

Cluster-gewichten moeten optellen tot `total_points`. Criteria-gewichten binnen een cluster moeten optellen tot het cluster-gewicht.
