#!/usr/bin/env python3
"""End-to-end demo: rubric + student work → graded Excel report.

Uses Anthropic's API to spawn one cluster-evaluator per rubric cluster.
This mirrors the multi-agent design of the rubric-evaluator skill in a
single Python script so people without Claude Desktop can still try it.

Usage:
    pip install anthropic openpyxl
    export ANTHROPIC_API_KEY=sk-ant-...

    python run_demo.py \
        --rubric ../examples/sample-rubric.json \
        --student-work ../examples/sample-student-report.txt \
        --output ../examples/evaluation_report.xlsx
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import tempfile
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("Missing dependency: pip install anthropic")

# Re-use the aggregator
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from aggregate_scores import (  # noqa: E402
    build_workbook,
    compute_final_grade,
    load_rubric,
)

MODEL = "claude-sonnet-4-6"

CLUSTER_PROMPT = """You evaluate ONE cluster of a rubric against a student artifact.

Cluster definition:
{cluster_json}

Student artifact (plain text):
---
{student_text}
---

Instructions:
- For each criterion, find concrete evidence in the student text (quotes, references to sections).
- Match evidence to one of the levels; pick the lower level if ambiguous.
- Compute achieved_score = max_score * level_score_multiplier.
- Motivations must cite specific evidence — no vague "ok work".

Return ONLY a JSON object with this shape:
{{
  "cluster_id": "{cluster_id}",
  "cluster_score": <sum of achieved_score>,
  "cluster_max": <sum of max_score>,
  "criteria": [
    {{
      "id": "<criterion id>",
      "achieved_score": <number>,
      "max_score": <number>,
      "level_label": "<level label>",
      "motivation": "<2-4 sentences with evidence>"
    }}
  ]
}}
No prose outside the JSON."""


def evaluate_cluster(client: anthropic.Anthropic, cluster: dict, student_text: str) -> dict:
    """Run one cluster-evaluator and return its parsed JSON result."""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": CLUSTER_PROMPT.format(
                    cluster_json=json.dumps(cluster, indent=2, ensure_ascii=False),
                    student_text=student_text,
                    cluster_id=cluster["id"],
                ),
            }
        ],
    )
    text = msg.content[0].text.strip()
    # Strip code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[len("json"):].strip()
    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rubric", required=True, type=Path)
    parser.add_argument("--student-work", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Set ANTHROPIC_API_KEY environment variable.")

    rubric = load_rubric(args.rubric)
    student_text = args.student_work.read_text(encoding="utf-8")
    client = anthropic.Anthropic()

    print(f"Evaluating {len(rubric['clusters'])} clusters in parallel...")
    results: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(evaluate_cluster, client, cluster, student_text): cluster["id"]
            for cluster in rubric["clusters"]
        }
        for fut in concurrent.futures.as_completed(futures):
            cluster_id = futures[fut]
            try:
                results[cluster_id] = fut.result()
                print(f"  ✓ {cluster_id}")
            except Exception as e:
                print(f"  ✗ {cluster_id}: {e}", file=sys.stderr)
                results[cluster_id] = {
                    "cluster_id": cluster_id,
                    "cluster_score": 0,
                    "cluster_max": next(
                        c["weight"] for c in rubric["clusters"] if c["id"] == cluster_id
                    ),
                    "criteria": [],
                    "error": str(e),
                }

    total, max_total = compute_final_grade(rubric, results)
    wb = build_workbook(rubric, results, total, max_total)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)
    grade_10 = round(total / max_total * 10, 1) if max_total else 0
    print(f"\nEindcijfer: {grade_10} ({round(total,1)}/{round(max_total,1)})")
    print(f"Rapport opgeslagen: {args.output}")


if __name__ == "__main__":
    main()
