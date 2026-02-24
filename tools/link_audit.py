#!/usr/bin/env python3
"""Dependency-free Markdown link audit.

Checks local (repo-relative) links in Markdown-like files and reports broken targets and
missing heading anchors. No network calls.

Exit codes:
  0 - OK (no problems)
  1 - Broken links found
  2 - Usage / argument error
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class LinkIssue:
    source_file: Path
    source_line: int
    raw_target: str
    reason: str


def _is_external(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "tel:", "data:"))


def _split_target(target: str) -> tuple[str, str | None]:
    # Strip surrounding whitespace; keep original for reporting.
    target = target.strip()
    if "#" not in target:
        return target, None
    path_part, anchor = target.split("#", 1)
    return path_part, anchor


def _github_slugify(text: str) -> str:
    """Approximate GitHub heading slug generation.

    This is intentionally conservative and dependency-free.
    """
    text = text.strip().lower()
    # Remove punctuation except spaces, hyphens, and underscores.
    # (GitHub-style anchors commonly preserve underscores in practice.)
    text = re.sub(r"[^a-z0-9\s\-_]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def _collect_heading_anchors(markdown_path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}

    try:
        content = markdown_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = markdown_path.read_text(encoding="utf-8", errors="replace")

    in_fence = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("````"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped.startswith("#"):
            continue

        # ATX heading: # Title
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if not match:
            continue

        heading_text = match.group(2)
        base = _github_slugify(heading_text)
        if not base:
            continue

        n = counts.get(base, 0)
        counts[base] = n + 1
        if n == 0:
            anchors.add(base)
        else:
            anchors.add(f"{base}-{n}")

    return anchors


def _iter_candidate_files(root: Path) -> list[Path]:
    patterns = ["**/*.md", "**/*.agent.md", "llms.txt"]
    ignore_dirs = {".git", ".venv", "node_modules", "dist", "build", ".pytest_cache"}

    results: list[Path] = []
    for pattern in patterns:
        for p in root.glob(pattern):
            if any(part in ignore_dirs for part in p.parts):
                continue
            if p.is_file():
                results.append(p)

    # De-dupe while preserving order.
    seen: set[Path] = set()
    deduped: list[Path] = []
    for p in results:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        deduped.append(p)
    return deduped


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _is_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def audit_file(
    source_file: Path,
    root: Path,
    anchor_cache: dict[Path, set[str]],
    *,
    strict: bool,
) -> list[LinkIssue]:
    try:
        text = source_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = source_file.read_text(encoding="utf-8", errors="replace")

    issues: list[LinkIssue] = []

    for match in LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        if not raw_target:
            continue

        # Allow links like <...> inside ()
        if raw_target.startswith("<") and raw_target.endswith(">"):
            raw_target = raw_target[1:-1].strip()

        if _is_external(raw_target):
            continue

        path_part, anchor = _split_target(raw_target)

        # In default mode, MULTI_AGENT_SPEC.md intentionally contains portable examples with
        # non-existent paths. To keep this tool actionable, validate only intra-document anchors
        # for that file unless --strict is used.
        if not strict and source_file.name == "MULTI_AGENT_SPEC.md" and path_part != "":
            continue

        # Same-file anchor link
        if path_part == "" and anchor is not None:
            target_path = source_file
        else:
            # Ignore pure fragment-less empty link
            if path_part == "":
                continue
            # Drop query string
            path_part = path_part.split("?", 1)[0]
            path_part = unquote(path_part)
            target_path = (source_file.parent / path_part).resolve()

        # Default behavior: do not validate links that point outside the current repo root
        # (MULTI_AGENT_SPEC.md contains portable examples that intentionally reference ../ paths).
        if not strict and not _is_within_root(target_path, root):
            continue

        # Special-case: for MULTI_AGENT_SPEC.md, treat missing out-of-repo targets as non-errors
        # in non-strict mode, but still validate intra-doc anchors and in-repo links.
        if (
            not strict
            and source_file.name == "MULTI_AGENT_SPEC.md"
            and path_part != ""
            and not _is_within_root(target_path, root)
        ):
            continue

        source_line = _line_number(text, match.start(1))

        if not target_path.exists():
            issues.append(
                LinkIssue(
                    source_file=source_file,
                    source_line=source_line,
                    raw_target=raw_target,
                    reason=(
                        "target path does not exist: "
                        + (
                            str(target_path.relative_to(root))
                            if _is_within_root(target_path, root)
                            else str(target_path)
                        )
                    ),
                )
            )
            continue

        if anchor is None or anchor == "":
            continue

        # If it's a directory, we don't validate anchors.
        if target_path.is_dir():
            continue

        # Only validate anchors for Markdown-like targets and llms.txt.
        if target_path.suffix.lower() not in {".md", ".txt"}:
            continue

        anchors = anchor_cache.get(target_path)
        if anchors is None:
            anchors = _collect_heading_anchors(target_path)
            anchor_cache[target_path] = anchors

        # GitHub treats anchors as already slugified; keep user's anchor as-is,
        # but allow common percent-decoding.
        normalized_anchor = unquote(anchor).strip().lower()
        # Be tolerant to '_' vs '-' variations.
        variants = {normalized_anchor, normalized_anchor.replace("_", "-")}
        if not any(v in anchors for v in variants):
            issues.append(
                LinkIssue(
                    source_file=source_file,
                    source_line=source_line,
                    raw_target=raw_target,
                    reason=(
                        f"missing anchor '#{anchor}' in "
                        + (
                            str(target_path.relative_to(root))
                            if _is_within_root(target_path, root)
                            else str(target_path)
                        )
                    ),
                )
            )

    return issues


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit local Markdown links (no network).")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also validate links that resolve outside the current repo root (may flag portable/examples in MULTI_AGENT_SPEC.md).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scan. If omitted, scans the repository root for *.md, *.agent.md, and llms.txt.",
    )
    args = parser.parse_args(argv)

    root = Path.cwd().resolve()

    if args.paths:
        candidates: list[Path] = []
        for p in args.paths:
            path = Path(p)
            if not path.exists():
                print(f"ERROR: path does not exist: {p}", file=sys.stderr)
                return 2
            if path.is_dir():
                candidates.extend(_iter_candidate_files(path.resolve()))
            else:
                candidates.append(path.resolve())
    else:
        candidates = _iter_candidate_files(root)

    anchor_cache: dict[Path, set[str]] = {}
    all_issues: list[LinkIssue] = []
    for f in candidates:
        all_issues.extend(audit_file(f, root=root, anchor_cache=anchor_cache, strict=args.strict))

    if not all_issues:
        print("OK: no broken local links found")
        return 0

    print(f"FOUND: {len(all_issues)} issue(s)")
    for issue in all_issues:
        rel = issue.source_file
        try:
            rel = issue.source_file.relative_to(root)
        except Exception:
            pass
        print(f"- {rel}:{issue.source_line} -> {issue.raw_target} :: {issue.reason}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
