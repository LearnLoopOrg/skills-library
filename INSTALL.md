# Installeren

Deze plugin is bedoeld voor de UvA AI Chat en werkt daarnaast in Claude Desktop / Cowork — overal waar Claude-skills draaien.

## Marketplace registreren en plugin installeren

In de UvA AI Chat of Claude Desktop / Cowork:

```
/plugin marketplace add LearnLoopOrg/skills-library
/plugin install slimmer-collegejaar@skills-library
```

Eventueel even de chat herstarten. Daarna triggeren de skills automatisch.

## Gebruiken in de chat

**Een rubric bouwen** — upload of plak een beoordelingsformulier, opdrachtomschrijving of screenshot van een rubric, en zeg:

> "Maak hier een rubric van"

De `rubric-builder` skill levert een gestructureerde `rubric.json` met clusters, criteria, gewichten en niveaus.

**Studentwerk nakijken** — geef de rubric en het studentdocument (PDF, docx, of plain text), en zeg:

> "Evalueer deze scriptie met de rubric"

De `rubric-evaluator` skill verdeelt de rubric over sub-agents (één per cluster), beoordeelt elk onderdeel apart en levert een Excel-rapport met eindcijfer, per-cluster scores en per-criterium motiveringen met bewijs uit het werk.

## Eigen rubric

Zie `slimmer-collegejaar-plugin/skills/rubric-evaluator/examples/sample-rubric.json` voor de verwachte structuur. Wat moet kloppen:

- Cluster-gewichten tellen op tot `total_points`.
- Criteria-gewichten binnen een cluster tellen op tot het cluster-gewicht.
- Elk criterium heeft minimaal 3 levels met observeerbare indicators.

Of laat de `rubric-builder` skill het voor je doen op basis van je bestaande beoordelingsformulier — dat is meestal de snelste route.
