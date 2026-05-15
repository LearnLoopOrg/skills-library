---
name: rubric-evaluator
description: Evaluate a student's work (essay, report, code, presentation) against a structured rubric by spawning one sub-agent per logical cluster of criteria, then aggregating per-criterion scores into a final Excel report with a weighted grade and motivations. Use this skill whenever the user has a rubric.json (or a clear rubric in any form) plus a student artifact and wants a graded evaluation. Trigger on phrases like "nakijken met deze rubric", "score this report against the rubric", "evalueer deze scriptie", "give this student work a grade", or any combination of student work + assessment criteria where a structured evaluation is needed.
---

# Rubric Evaluator

Grade student work against a structured rubric using per-cluster sub-agents and produce an Excel report.

## Why this design

A single prompt asked to score a long document against 20+ criteria tends to drift toward the mean: most criteria get a vague "voldoende" because the model can't hold sharp attention on each one. Splitting the rubric into clusters and spawning a dedicated sub-agent per cluster forces real, separate analysis per topic. The aggregator then combines those into a coherent final grade.

This mirrors how human assessors actually grade — one section at a time, not the whole rubric in one breath.

## Inputs

- A `rubric.json` (use the `rubric-builder` skill first if the rubric isn't structured yet).
- A student artifact: a `.pdf`, `.docx`, `.md`, or `.txt` file. For PDFs, extract text first.

## Workflow

### Step 1: Load and validate the rubric

Read `rubric.json`. Verify that cluster weights sum to `total_points` and that criteria weights within each cluster sum to the cluster weight. If they don't, surface the discrepancy and ask whether to proceed or fix.

### Step 2: Extract the student artifact to plain text

For PDFs use `pdfplumber` or `pdftotext`. For .docx use `python-docx`. Save extracted text alongside the rubric so each sub-agent reads the same source.

### Step 3: Spawn one sub-agent per cluster

For each cluster, spawn a sub-agent (use the `Agent` tool) with the prompt template in `agents/group-evaluator.md`. Pass it:
- The cluster definition (its criteria + levels)
- The full student text
- An output path: `outputs/cluster_<cluster_id>.json`

Spawn them in parallel — they don't depend on each other. This keeps wall-clock time low even for long rubrics.

### Step 4: Wait for all clusters and aggregate

Once all `cluster_*.json` files are written, run `scripts/aggregate_scores.py`:

```bash
python scripts/aggregate_scores.py --rubric rubric.json --clusters-dir outputs/ --output evaluation_report.xlsx
```

This produces an Excel file with:
- **Sheet 1: Samenvatting** — eindcijfer, totaal punten, per-cluster scores
- **Sheet 2: Detail per criterium** — elke criterium met behaalde score, niveau-label, en motivering
- **Sheet 3: Rubric** — de gebruikte rubric voor reproduceerbaarheid

### Step 5: Brief the user

Report the final grade, the strongest and weakest clusters, and link to the Excel file. Keep it short — the report contains the detail.

## Output contract

Each sub-agent writes a `cluster_<id>.json` with this shape:

```json
{
  "cluster_id": "inleiding",
  "cluster_score": 12.5,
  "cluster_max": 15,
  "criteria": [
    {
      "id": "inl_research_question",
      "achieved_score": 6.4,
      "max_score": 8,
      "level_label": "voldoende",
      "motivation": "De onderzoeksvraag is geformuleerd op p.2 maar bevat geen scope-afbakening. Citaat: '...wat is het effect van X op Y...' — Y is niet gespecificeerd."
    }
  ]
}
```

Motivations should cite specific page numbers, paragraphs, or exact quotes from the student text. Vague motivations like "behoorlijk goed" are not acceptable — the student should be able to see *why* they got the score.

## When something goes wrong

- **Cluster weights don't sum correctly:** ask user to fix the rubric or proceed with normalized weights and flag it in the report.
- **Student artifact is empty or unreadable:** stop and surface the error — don't fabricate an evaluation.
- **A sub-agent fails or returns invalid JSON:** retry once; if it fails again, write a placeholder cluster_*.json with `error: <reason>` and continue, then mention the failed cluster in the final brief.
