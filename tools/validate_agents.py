#!/usr/bin/env python3
"""Dependency-free agent prompt contract checks.

These checks act as lightweight "golden tests" for prompt structure: they catch accidental
removals of critical rules (iteration limits, role separation, output formats).

Exit codes:
  0 - OK
  1 - Validation failures
  2 - Usage / argument error
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


AGENT_DIR = Path(".github/copilot/agents")


@dataclass(frozen=True)
class CheckFailure:
    file: Path
    message: str


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def _must_contain(text: str, needles: list[str]) -> list[str]:
    missing = []
    for n in needles:
        if n not in text:
            missing.append(n)
    return missing


def validate_orchestrator(path: Path, text: str) -> list[CheckFailure]:
    missing = _must_contain(
        text,
        [
            "## Task Protocol",
            "Execution loop",
            "Final verification",
            "max 3 iterations",
            "Do not combine executor and critic",
            "Language rule",
        ],
    )
    return [CheckFailure(path, f"Missing required marker: {m}") for m in missing]


def validate_executor(path: Path, text: str) -> list[CheckFailure]:
    missing = _must_contain(text, ["## Task Protocol", "apply_patch", "get_errors"])
    return [CheckFailure(path, f"Missing required marker: {m}") for m in missing]


def validate_tooling(path: Path, text: str) -> list[CheckFailure]:
    missing = _must_contain(text, ["argparse", "exit codes", "No network calls"])
    return [CheckFailure(path, f"Missing required marker: {m}") for m in missing]


def validate_critic(path: Path, text: str) -> list[CheckFailure]:
    missing = _must_contain(text, ["Verdict:", "APPROVE", "REQUEST_CHANGES"])
    failures = [CheckFailure(path, f"Missing required marker: {m}") for m in missing]
    if "Does NOT write files" not in text and "Does NOT write" not in text:
        failures.append(CheckFailure(path, "Critic must explicitly state it does NOT write files"))
    return failures


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate agent prompt contracts (golden checks).")
    parser.add_argument(
        "agent_dir",
        nargs="?",
        default=str(AGENT_DIR),
        help="Directory containing *.agent.md (default: .github/copilot/agents)",
    )
    args = parser.parse_args(argv)

    agent_dir = Path(args.agent_dir)
    if not agent_dir.exists() or not agent_dir.is_dir():
        print(f"ERROR: agent_dir not found: {agent_dir}", file=sys.stderr)
        return 2

    agent_files = sorted(agent_dir.glob("*.agent.md"))
    if not agent_files:
        print(f"ERROR: no *.agent.md files found in {agent_dir}", file=sys.stderr)
        return 2

    failures: list[CheckFailure] = []
    for path in agent_files:
        text = _read_text(path)
        name = path.name
        if "orchestrator" in name:
            failures.extend(validate_orchestrator(path, text))
        elif "tooling" in name:
            failures.extend(validate_tooling(path, text))
        elif "critic" in name:
            failures.extend(validate_critic(path, text))
        else:
            failures.extend(validate_executor(path, text))

    if not failures:
        print("OK: agent prompt contracts look good")
        return 0

    print(f"FOUND: {len(failures)} failure(s)")
    for f in failures:
        print(f"- {f.file}: {f.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
