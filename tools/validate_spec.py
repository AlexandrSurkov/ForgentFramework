#!/usr/bin/env python3
"""Lightweight validation for ForgentFramework specification Markdown.

Goals:
- Catch broken fenced code blocks (unbalanced ``` / ```` fences).
- Catch obvious heading numbering mistakes (e.g., duplicated top-level title).

This is intentionally dependency-free.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


RE_FENCE = re.compile(r"^(?P<ticks>`{3,})(?P<info>.*)$")
RE_H1 = re.compile(r"^\ufeff?\s*#\s+.+")


@dataclass(frozen=True)
class Finding:
    severity: str  # ERROR | WARNING
    file: str
    line: int
    message: str


def iter_lines(text: str):
    # Keep universal newlines and stable line numbering.
    return text.splitlines()


def validate_fences(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    fence_stack: list[tuple[str, int]] = []  # (ticks, line)

    lines = iter_lines(path.read_text(encoding="utf-8"))
    for idx, line in enumerate(lines, start=1):
        m = RE_FENCE.match(line)
        if not m:
            continue

        ticks = m.group("ticks")
        if not fence_stack:
            fence_stack.append((ticks, idx))
            continue

        open_ticks, _open_line = fence_stack[-1]
        # While inside a fenced block, treat other fences as literal content
        # unless they close the current block.
        if len(ticks) >= len(open_ticks):
            fence_stack.pop()

    for open_ticks, open_line in fence_stack:
        findings.append(
            Finding(
                severity="ERROR",
                file=str(path.as_posix()),
                line=open_line,
                message=f"Unclosed fenced code block opened with {len(open_ticks)} backticks.",
            )
        )

    return findings


def validate_single_h1(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    lines = iter_lines(path.read_text(encoding="utf-8"))

    h1_lines: list[int] = []
    fence_stack: list[str] = []
    for idx, line in enumerate(lines, start=1):
        m = RE_FENCE.match(line)
        if m:
            ticks = m.group("ticks")
            if not fence_stack:
                fence_stack.append(ticks)
                continue
            open_ticks = fence_stack[-1]
            if len(ticks) >= len(open_ticks):
                fence_stack.pop()
            continue

        if fence_stack:
            continue

        if RE_H1.match(line):
            h1_lines.append(idx)
    if len(h1_lines) == 0:
        findings.append(Finding("WARNING", str(path.as_posix()), 1, "No H1 title found (# ...)."))
    elif len(h1_lines) > 1:
        findings.append(
            Finding(
                "WARNING",
                str(path.as_posix()),
                h1_lines[1],
                f"Multiple H1 titles found (count={len(h1_lines)}). Consider keeping a single H1.",
            )
        )

    return findings


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    spec = repo_root / "MULTI_AGENT_SPEC.md"

    targets = [spec]
    missing = [p for p in targets if not p.exists()]
    if missing:
        for p in missing:
            print(f"ERROR: missing file: {p}")
        return 2

    findings: list[Finding] = []
    for p in targets:
        findings.extend(validate_fences(p))
        findings.extend(validate_single_h1(p))

    if findings:
        error_count = sum(1 for f in findings if f.severity == "ERROR")
        for f in findings:
            print(f"{f.severity}: {f.file}:{f.line}: {f.message}")
        print(f"\nSummary: {error_count} error(s), {len(findings) - error_count} warning(s)")
        return 1 if error_count else 0

    print("OK: validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
