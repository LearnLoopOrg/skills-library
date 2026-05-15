---
name: rubric-builder
description: Convert a course assignment description, grading form, or screenshot of an assessment rubric into a structured machine-readable rubric (rubric.json) with weighted criteria grouped into logical clusters. Use this skill whenever the user uploads or pastes an assignment description, beoordelingsformulier, scoring guide, or screenshot of a rubric and needs it turned into a structured format for downstream evaluation. Trigger on phrases like "make a rubric from this", "turn this beoordelingsformulier into a rubric", "extract the criteria from this assignment", or any time the user provides assessment material and wants it formalized.
---

# Rubric Builder

Turn unstructured assessment material into a clean, weighted, clustered rubric.

## Why this exists

Teachers express criteria in many shapes: a Word doc full of paragraphs, a Canvas grading form, a screenshot of a beoordelingsformulier from a course manual, a few bullet points in an email. To use that material for systematic evaluation you need a structured representation: each criterion with a description, weight, and a cluster it belongs to. This skill produces exactly that.

## Output format

Write a single file `rubric.json` with this shape:

```json
{
  "title": "Korte titel van de opdracht",
  "total_points": 100,
  "clusters": [
    {
      "id": "inleiding",
      "name": "Inleiding",
      "weight": 15,
      "criteria": [
        {
          "id": "inl_research_question",
          "description": "Onderzoeksvraag is helder geformuleerd en relevant",
          "weight": 8,
          "levels": [
            {"label": "uitmuntend", "score": 1.0, "indicator": "Vraag is scherp, afgebakend, en sluit aan op bestaande literatuur"},
            {"label": "voldoende", "score": 0.7, "indicator": "Vraag is duidelijk maar enigszins breed"},
            {"label": "onvoldoende", "score": 0.3, "indicator": "Vraag is vaag of ontbreekt"}
          ]
        }
      ]
    }
  ]
}
```

## How to build a good rubric

1. **Read the source material twice.** First pass for what's being assessed; second pass for weighting cues (percentages, "belangrijk", "must", point allocations).

2. **Group into 4–7 clusters.** Typical clusters for academic writing: Inleiding, Methoden, Resultaten, Discussie/Conclusie, Taal en opmaak, Bronnen. For software projects: Functionaliteit, Codekwaliteit, Documentatie, Testen. Pick clusters that fit the artifact being assessed — don't force-fit.

3. **Each criterion gets weights and levels.** Aim for 3–5 levels per criterion (e.g., onvoldoende / voldoende / goed / uitmuntend). Levels need *observable indicators* — what would the assessor actually see in the work? Vague levels like "goed werk" are useless to a downstream evaluator.

4. **Weights should sum sensibly.** Cluster weights sum to the total (often 100). Criteria weights within a cluster sum to the cluster weight. Verify this before writing the file.

5. **Preserve original language.** If the source is in Dutch, keep criteria descriptions in Dutch — translation noise hurts downstream evaluation.

## When source material is thin

If the user provides only a one-paragraph assignment description with no explicit criteria, infer a sensible default rubric for that artifact type but flag it clearly in your reply:

> "Ik heb een standaard-rubric afgeleid voor een onderzoeksrapport — pas de gewichten aan als je andere accenten wilt."

Don't pretend you extracted criteria that weren't there.

## Examples of source → output

**Input:** Screenshot of a beoordelingsformulier with sections "Inleiding (20pt)", "Methoden (30pt)", "Resultaten (30pt)", "Conclusie (20pt)" each with sub-bullets.

**Output:** rubric.json with 4 clusters, weights 20/30/30/20, each containing 2–4 criteria with the sub-bullet wording verbatim and inferred 3-level scales.

**Input:** Email from a teacher saying "weeg de literatuurkennis zwaar en let op of de student de methode echt begrijpt".

**Output:** rubric.json with elevated weight on a "Literatuurkennis" cluster and a methodology criterion focused on understanding rather than execution. Note in reply that weights were inferred from emphasis cues.
