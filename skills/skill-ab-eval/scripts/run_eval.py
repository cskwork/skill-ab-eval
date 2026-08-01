#!/usr/bin/env python3
"""skill-ab-eval orchestrator — two axes, all over the CLI.

Axis 1 (skill):    run the same task WITH a skill loaded vs WITHOUT (baseline).
Axis 2 (harness):  run it through several CLI harnesses (claude/codex/gemini/agy/
                   openai) and see which one does the task best.

A judge harness grades every output against the eval's assertions (or holistically
when there are none), repeated over trials. You get a skill-lift table and a
harness leaderboard.

Two ways to drive it:
  task  — one ad-hoc task you type (optionally with a skill and assertions)
  run   — a skill dir's evals/evals.json suite

Stdlib only. CLI harnesses are invoked via the shell adapters in ../runners/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNNERS_DIR = ROOT / "runners"
# Built-in harnesses: how to pass the prompt as argv. The CLI is resolved on PATH
# and run directly (no shell), so it works the same on Windows/macOS/Linux. The
# mirror shell adapters in runners/*.sh are the portable reference + the extension
# point for custom harnesses. {prompt} is substituted with the full prompt.
BUILTIN_ARGS = {
    "claude": ["-p", "{prompt}"],
    "codex": ["exec", "--skip-git-repo-check", "{prompt}"],
    "gemini": ["-p", "{prompt}"],
    "agy": ["-p", "{prompt}"],
}


# ---------------------------------------------------------------- skill + evals
def load_skill_body(skill_dir: Path) -> str:
    """SKILL.md body with YAML frontmatter stripped."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()


def inline_files(prompt: str, files: list[str], base_dir: Path) -> str:
    """Replace {{filename}} placeholders; append any un-referenced files."""
    for rel in files or []:
        content = (base_dir / rel).read_text(encoding="utf-8")
        token = "{{" + Path(rel).name + "}}"
        prompt = prompt.replace(token, content) if token in prompt \
            else prompt + f"\n\n--- {Path(rel).name} ---\n{content}"
    return prompt


# ---------------------------------------------------------------- runners
def available_runners() -> list[str]:
    """Built-in runners whose CLI/key is actually present."""
    found = [name for name in BUILTIN_ARGS if shutil.which(name)]
    if os.environ.get("OPENAI_API_KEY"):
        found.append("openai")
    return found


def run_via(runner: str, prompt: str, cfg: argparse.Namespace) -> str:
    """Send a prompt to a runner, return its text answer."""
    if runner == "openai":
        return _openai_chat(prompt, cfg)
    if runner in BUILTIN_ARGS:
        return _run_builtin(runner, prompt, cfg)
    adapter = RUNNERS_DIR / f"{runner}.sh"   # custom harness (POSIX / git-bash)
    if not adapter.exists():
        raise FileNotFoundError(f"unknown runner '{runner}' (no runners/{runner}.sh)")
    if not shutil.which("bash"):
        raise RuntimeError(f"runner '{runner}': custom .sh adapters need bash "
                           "(install Git for Windows or WSL)")
    return _capture(["bash", "-c", adapter.read_text(encoding="utf-8")], runner, cfg,
                    env={**os.environ, "PROMPT": prompt})


def _run_builtin(runner: str, prompt: str, cfg: argparse.Namespace) -> str:
    exe = shutil.which(runner)
    if not exe:
        raise RuntimeError(f"{runner}: CLI not found on PATH")
    argv = [exe] + [prompt if a == "{prompt}" else a for a in BUILTIN_ARGS[runner]]
    if os.name == "nt":  # wrap shim scripts; bare .exe runs directly
        low = exe.lower()
        if low.endswith((".cmd", ".bat")):
            argv = ["cmd", "/c"] + argv
        elif low.endswith(".ps1"):
            argv = ["powershell", "-NoProfile", "-File"] + argv
    return _capture(argv, runner, cfg)


def _capture(argv: list[str], runner: str, cfg: argparse.Namespace,
             env: dict | None = None) -> str:
    proc = subprocess.run(argv, capture_output=True, text=True,
                          timeout=cfg.timeout, env=env)
    out = proc.stdout.strip()
    if proc.returncode != 0:
        if not out:
            raise RuntimeError(f"{runner} failed (rc={proc.returncode}): "
                               f"{proc.stderr.strip()[:200]}")
        print(f"warning: {runner} exited {proc.returncode} but produced output; "
              f"grading it anyway", file=sys.stderr)
    return out


def _openai_chat(prompt: str, cfg: argparse.Namespace) -> str:
    import urllib.request
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("openai runner requires OPENAI_API_KEY")
    body = json.dumps({"model": cfg.openai_model,
                       "messages": [{"role": "user", "content": prompt}],
                       "temperature": cfg.temperature}).encode("utf-8")
    req = urllib.request.Request(
        cfg.base_url.rstrip("/") + "/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=cfg.timeout) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------------- judging
def build_judge_prompt(task: str, expected: str, assertions: list[str],
                       answer: str) -> str:
    if assertions:
        checks = "Assertions to check (pass or fail each, in order):\n" + \
            "\n".join(f"{i + 1}. {a}" for i, a in enumerate(assertions))
        schema = ('{"assertions": [true/false per assertion in order], '
                  '"score": 0-10, "notes": "one sentence"}')
    else:
        checks = "There are no explicit assertions; rate overall quality for the task."
        schema = '{"assertions": [], "score": 0-10, "notes": "one sentence"}'
    good = expected or "a correct, complete, well-formed answer to the task"
    return (
        "You are a strict, impartial grader. Grade the answer below ONLY on the "
        "evidence in it. Do not reward or penalize style you were not asked about.\n\n"
        f"Task that was given:\n{task}\n\n"
        f"What a good answer looks like:\n{good}\n\n{checks}\n\n"
        f"--- ANSWER ---\n{answer}\n--- END ANSWER ---\n\n"
        f"Return STRICT JSON only, no prose:\n{schema}")


def parse_judge_json(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"no JSON in judge reply: {raw[:160]}")
    return json.loads(match.group(0))


def grade(task: str, ev: dict, answer: str, cfg: argparse.Namespace) -> dict:
    raw = run_via(cfg.judge, build_judge_prompt(
        task, ev.get("expected_output", ""), ev.get("assertions", []), answer), cfg)
    parsed = parse_judge_json(raw)
    asserts = parsed.get("assertions", [])
    if not isinstance(asserts, list):
        asserts = []
    try:
        score = float(parsed.get("score", 0))
    except (TypeError, ValueError):
        score = 0.0
    return {"assertions": asserts, "score": score, "notes": parsed.get("notes", "")}


# ---------------------------------------------------------------- evaluation
def sides_for(skill_body: str) -> list[str]:
    return ["with_skill", "without_skill"] if skill_body else ["baseline"]


def full_prompt(skill_body: str, task: str, side: str) -> str:
    if side == "with_skill":
        return (f"Follow these instructions exactly:\n\n--- INSTRUCTIONS ---\n"
                f"{skill_body}\n--- END INSTRUCTIONS ---\n\nTask:\n{task}")
    return f"Task:\n{task}"


def run_cell(task: str, ev: dict, runner: str, side: str, skill_body: str,
             cfg: argparse.Namespace, out_dir: Path) -> list[dict]:
    """One (runner, side): run + grade across trials. Writes artifacts."""
    trials = []
    prompt = full_prompt(skill_body, task, side)
    for t in range(1, cfg.trials + 1):
        try:  # a flaky harness/judge shouldn't abort the whole matrix
            answer = run_via(runner, prompt, cfg)
            g = grade(task, ev, answer, cfg)
        except Exception as exc:
            print(f"  {ev['id']} | {runner:7} | {side:13} | trial {t} ERROR: "
                  f"{exc}", file=sys.stderr)
            continue
        cell = out_dir / runner / side / f"trial-{t}"
        cell.mkdir(parents=True, exist_ok=True)
        (cell / "answer.md").write_text(answer, encoding="utf-8")
        (cell / "judge.json").write_text(json.dumps(g, indent=2), encoding="utf-8")
        trials.append(g)
        print(f"  {ev['id']} | {runner:7} | {side:13} | trial {t}/{cfg.trials} "
              f"score={g['score']:.0f}")
    return trials


def pass_rate(grades: list[dict]) -> float:
    passed = sum(sum(1 for a in g["assertions"] if a) for g in grades)
    total = sum(len(g["assertions"]) for g in grades)
    return passed / total if total else 0.0


def mean_score(grades: list[dict]) -> float:
    return sum(g["score"] for g in grades) / len(grades) / 10 if grades else 0.0


def verdict_for(lift: float) -> str:
    if lift >= 0.20:
        return "clear positive"
    if lift >= 0.05:
        return "marginal"
    if lift > -0.05:
        return "no measurable effect"
    return "negative"


def _next_iteration(base: Path) -> Path:
    """Pick iteration-N+1 so reruns never overwrite prior results."""
    n = 1
    while (base / f"iteration-{n}").exists():
        n += 1
    return base / f"iteration-{n}"


def evaluate(evals: list[dict], skill_body: str, skill_name: str,
             cfg: argparse.Namespace) -> dict:
    out_root = _next_iteration(Path(cfg.workspace) / skill_name)
    has_assert = any(ev.get("assertions") for ev in evals)
    metric = pass_rate if has_assert else mean_score
    sides = sides_for(skill_body)
    per_eval = []
    for ev in evals:
        task = inline_files(ev["prompt"], ev.get("files", []), cfg.base_dir)
        cells = {}  # (runner, side) -> score
        for runner in cfg.runners:
            for side in sides:
                grades = run_cell(task, ev, runner, side, skill_body, cfg,
                                  out_root / ev["id"])
                cells[(runner, side)] = round(metric(grades), 3)
        per_eval.append({"id": ev["id"], "name": ev.get("name", ev["id"]),
                         "cells": {f"{r}|{s}": v for (r, s), v in cells.items()}})
    summary = _summarize(per_eval, cfg, sides, skill_name, metric.__name__)
    _write_summary(out_root, summary)
    return summary


# ---------------------------------------------------------------- reporting
def _avg_cell(per_eval: list[dict], runner: str, side: str) -> float:
    vals = [e["cells"][f"{runner}|{side}"] for e in per_eval
            if f"{runner}|{side}" in e["cells"]]
    return round(sum(vals) / len(vals), 3) if vals else 0.0


def _summarize(per_eval: list[dict], cfg: argparse.Namespace, sides: list[str],
               skill_name: str, metric: str) -> dict:
    skill_axis = "with_skill" in sides
    leaderboard_side = "with_skill" if skill_axis else "baseline"
    lift, leaderboard = [], []
    for runner in cfg.runners:
        leaderboard.append({"runner": runner,
                            "score": _avg_cell(per_eval, runner, leaderboard_side)})
        if skill_axis:
            w = _avg_cell(per_eval, runner, "with_skill")
            wo = _avg_cell(per_eval, runner, "without_skill")
            lift.append({"runner": runner, "with_skill": w, "without_skill": wo,
                         "lift": round(w - wo, 3), "verdict": verdict_for(w - wo)})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return {"skill_name": skill_name, "metric": metric, "trials": cfg.trials,
            "judge": cfg.judge, "runners": cfg.runners, "skill_axis": skill_axis,
            "skill_lift": lift, "harness_leaderboard": leaderboard, "evals": per_eval}


def _write_summary(out_root: Path, s: dict) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "results.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
    metric_label = "pass rate" if s["metric"] == "pass_rate" else "mean score"
    lines = [f"# skill-ab-eval report: {s['skill_name']}", "",
             f"- runners: {', '.join(s['runners'])} | judge: `{s['judge']}` | "
             f"trials: {s['trials']} | metric: {metric_label}", ""]
    if s["skill_axis"]:
        lines += ["## Skill lift by harness", "",
                  "| harness | with | without | lift | verdict |",
                  "|---------|------|---------|------|---------|"]
        lines += [f"| {r['runner']} | {r['with_skill']:.2f} | "
                  f"{r['without_skill']:.2f} | {r['lift']:+.2f} | {r['verdict']} |"
                  for r in s["skill_lift"]]
        lines.append("")
    side = "with skill" if s["skill_axis"] else "baseline"
    lines += [f"## Harness leaderboard ({side})", "", "| rank | harness | score |",
              "|------|---------|-------|"]
    lines += [f"| {i + 1} | {r['runner']} | {r['score']:.2f} |"
              for i, r in enumerate(s["harness_leaderboard"])]
    (out_root / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {out_root / 'report.md'}")
    print("\n".join(lines))


# ---------------------------------------------------------------- CLI
def _resolve_runners(cfg: argparse.Namespace) -> None:
    avail = available_runners()
    cfg.runners = [r.strip() for r in cfg.runners.split(",")] if cfg.runners else avail
    missing = [r for r in cfg.runners if r not in avail]
    if missing:
        print(f"warning: requested runners not detected (will error if used): "
              f"{missing}", file=sys.stderr)
    if not cfg.runners:
        sys.exit("error: no runners available. Install a CLI (claude/codex/gemini/agy) "
                 "or set OPENAI_API_KEY.")
    if cfg.judge not in cfg.runners and cfg.judge not in avail:
        cfg.judge = cfg.runners[0]


def cmd_runners(cfg: argparse.Namespace) -> int:
    avail = available_runners()
    print("Detected runners:" if avail else "No runners detected.")
    for r in avail:
        print(f"  - {r}")
    return 0


def cmd_task(cfg: argparse.Namespace) -> int:
    _resolve_runners(cfg)
    skill_body = load_skill_body(Path(cfg.skill)) if cfg.skill else ""
    cfg.base_dir = Path(cfg.skill) if cfg.skill else Path(".")
    ev = {"id": "adhoc", "name": "ad-hoc task", "prompt": cfg.prompt,
          "files": [], "expected_output": cfg.expected or "",
          "assertions": cfg.assert_ or []}
    name = Path(cfg.skill).name if cfg.skill else "adhoc-task"
    evaluate([ev], skill_body, name, cfg)
    return 0


def cmd_run(cfg: argparse.Namespace) -> int:
    _resolve_runners(cfg)
    skill_dir = Path(cfg.skill_dir)
    cfg.base_dir = skill_dir
    skill_body = load_skill_body(skill_dir)
    doc = json.loads((skill_dir / "evals" / "evals.json").read_text("utf-8"))
    evaluate(doc["evals"], skill_body, doc["skill_name"], cfg)
    return 0


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--runners", default="", help="comma list; default = all detected")
    p.add_argument("--judge", default="claude", help="runner used to grade")
    p.add_argument("--trials", type=int, default=2)
    p.add_argument("--timeout", type=int, default=240)
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--workspace", default="skill-ab-eval-workspace")
    p.add_argument("--base-url", default=os.environ.get(
        "OPENAI_BASE_URL", "https://api.openai.com/v1"))
    p.add_argument("--openai-model", default="gpt-4o-mini")


def main() -> int:
    ap = argparse.ArgumentParser(prog="skill-ab-eval",
                                 description="A/B + multi-harness skill evaluator.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("task", help="evaluate one ad-hoc task you type")
    pt.add_argument("prompt", help="the task to evaluate")
    pt.add_argument("--skill", help="skill dir to load on the with_skill side")
    pt.add_argument("--expected", help="what a good answer looks like (for the judge)")
    pt.add_argument("--assert", dest="assert_", action="append",
                    help="a binary assertion (repeatable)")
    _add_common(pt)
    pt.set_defaults(func=cmd_task)

    pr = sub.add_parser("run", help="evaluate a skill's evals/evals.json suite")
    pr.add_argument("skill_dir", help="path to skill dir (SKILL.md + evals/evals.json)")
    _add_common(pr)
    pr.set_defaults(func=cmd_run)

    prn = sub.add_parser("runners", help="list detected harnesses")
    prn.set_defaults(func=cmd_runners)

    cfg = ap.parse_args()
    return cfg.func(cfg)


if __name__ == "__main__":
    raise SystemExit(main())
