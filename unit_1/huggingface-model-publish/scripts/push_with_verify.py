"""Guard a Trainer.push_to_hub on an eval-metric threshold.

Usage:
    from push_with_verify import verify_and_push
    verify_and_push(trainer, metric="eval_accuracy", threshold=0.87,
                    push_kwargs=dict(dataset_tags="marsyas/gtzan",
                                     model_name="my-model",
                                     finetuned_from="ntu-spml/distilhubert",
                                     tasks="audio-classification"))

Prints a single `[RESULT]` line (easy to grep), pushes only if the metric
clears the threshold, and returns the eval-results dict either way.
"""
from __future__ import annotations
from typing import Any


def verify_and_push(
    trainer: Any,
    *,
    metric: str = "eval_accuracy",
    threshold: float,
    higher_is_better: bool = True,
    push_kwargs: dict | None = None,
) -> dict:
    res = trainer.evaluate()
    if metric not in res:
        raise KeyError(
            f"metric {metric!r} not in trainer.evaluate() keys: {sorted(res)}"
        )
    val = res[metric]
    passed = val >= threshold if higher_is_better else val <= threshold
    comp = ">=" if higher_is_better else "<"
    print(
        f"[RESULT] {metric}={val:.4f} target{comp}{threshold} "
        f"{'PASS' if passed else 'FAIL'}",
        flush=True,
    )
    if passed:
        print("[push] pushing to Hub...", flush=True)
        trainer.push_to_hub(**(push_kwargs or {}))
        print("[push] done", flush=True)
    else:
        print("[push] skipped (metric did not clear threshold)", flush=True)
    return res
