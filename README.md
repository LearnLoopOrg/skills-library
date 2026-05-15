# Slimmer Collegejaar — AI-nakijken skills

Open-source skills voor het automatisch genereren van rubrics en het beoordelen van studentwerk met AI. Ontwikkeld vanuit de LearnLoop-pilot (UvA, 2024–2026, project "Slimmer Collegejaar").

## Wat zit erin

Twee samenwerkende Claude-skills:

**`rubric-builder/`** — Zet een opdrachtbeschrijving, beoordelingsformulier of screenshot om in een gestructureerde rubric met criteria, weegfactoren en logische clusters (bijv. *Inleiding*, *Methoden*, *Resultaten*).

**`rubric-evaluator/`** — Beoordeelt een studentdocument tegen die rubric. Voor elk cluster wordt een sub-agent gespawnd die alleen díe criteria toetst — zo blijft de beoordeling per onderdeel scherp in plaats van vaag-over-het-geheel. Output is een Excel-rapport met per criterium een score, motivering en eindcijfer.

## Waarom deze opzet

Bij het beoordelen van studentwerk loopt een enkele AI-prompt al snel vast: te veel criteria tegelijk → vlakke, gemiddelde scores. Door per cluster een eigen sub-agent te draaien forceer je dat elk onderdeel daadwerkelijk apart bekeken wordt. Dit volgt het principe dat ook in de LearnLoop-pilot is bevestigd: kleinere, gerichte beoordelingsvragen leveren bruikbaardere feedback dan één grote.

## Snel proberen

```bash
# Vereist: Python 3.10+, een ANTHROPIC_API_KEY
pip install anthropic openpyxl
export ANTHROPIC_API_KEY=sk-ant-...

# Voorbeeld: rubric maken + werk beoordelen
python rubric-evaluator/scripts/run_demo.py \
  --rubric examples/sample-rubric.txt \
  --student-work examples/sample-student-report.txt \
  --output examples/evaluation_report.xlsx
```

Of installeer als Claude-skill: zie `INSTALL.md`.

## Status

Werk-in-uitvoering vanuit de LearnLoop-pilot. Tested op scriptie-evaluaties (biologie, applied data science). Feedback en pull requests welkom.

## Licentie

MIT — zie `LICENSE`.

## Contact

LearnLoop · Luc Mahieu · onderdeel van UvA-project *Slimmer Collegejaar*.
