#!/usr/bin/env python3
"""Sync docs/refactor/refactor-index.md by service boundary."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    ".idea",
    ".vscode",
    "docs",
    "node_modules",
    "dist",
    "build",
    "target",
    "coverage",
    "tmp",
    "vendor",
    "scripts",
    "tests",
    "test",
    ".github",
}

SERVICE_INDICATORS = {
    "package.json",
    "go.mod",
    "pyproject.toml",
    "requirements.txt",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Cargo.toml",
    "composer.json",
    "Dockerfile",
}


@dataclass
class StatusRow:
    service: str
    status: str = "pending"
    owner: str = "-"
    last_updated: str = "-"
    commit: str = "-"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover services and sync docs/refactor/refactor-index.md"
    )
    parser.add_argument("--repo-root", default=".", help="Target repository root")
    parser.add_argument(
        "--index-file",
        default="docs/refactor/refactor-index.md",
        help="Index markdown path relative to repo root",
    )
    parser.add_argument(
        "--service-roots",
        default="services,apps",
        help="Comma-separated roots containing service directories",
    )
    parser.add_argument(
        "--exclude-dirs",
        default=",".join(sorted(DEFAULT_EXCLUDES)),
        help="Comma-separated directory names to skip",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated content without writing file",
    )
    return parser.parse_args()


def parse_csv(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


def discover_services(repo_root: Path, service_roots: list[str], excludes: set[str]) -> list[str]:
    discovered: list[str] = []

    for root_name in service_roots:
        root_path = repo_root / root_name
        if not root_path.is_dir():
            continue
        for child in sorted(root_path.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith(".") or child.name in excludes:
                continue
            discovered.append(child.relative_to(repo_root).as_posix())

    if discovered:
        return discovered

    top_level = []
    for child in sorted(repo_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in excludes:
            continue
        top_level.append(child)

    with_indicators = []
    for candidate in top_level:
        if any((candidate / marker).exists() for marker in SERVICE_INDICATORS):
            with_indicators.append(candidate.relative_to(repo_root).as_posix())

    if with_indicators:
        return with_indicators

    return [x.relative_to(repo_root).as_posix() for x in top_level]


def extract_section(text: str, heading: str) -> str:
    pattern = rf"(?ms)^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip("\n") if match else ""


def parse_status_rows(text: str) -> dict[str, StatusRow]:
    content = extract_section(text, "Service Status")
    if not content:
        content = extract_section(text, "Module Status")
    if not content:
        return {}

    rows: dict[str, StatusRow] = {}
    for line in content.splitlines():
        striped = line.strip()
        if not striped.startswith("|"):
            continue
        cols = [x.strip() for x in striped.split("|")[1:-1]]
        if len(cols) < 5:
            continue
        if cols[0].lower() in {"service", "module"}:
            continue
        if cols[0].startswith("---"):
            continue
        service = cols[0]
        rows[service] = StatusRow(
            service=service,
            status=cols[1] or "pending",
            owner=cols[2] or "-",
            last_updated=cols[3] or "-",
            commit=cols[4] or "-",
        )
    return rows


def parse_timeline_rows(text: str) -> list[str]:
    content = extract_section(text, "Round Timeline")
    if not content:
        return []
    out: list[str] = []
    for line in content.splitlines():
        striped = line.strip()
        if not striped.startswith("|"):
            continue
        cols = [x.strip() for x in striped.split("|")[1:-1]]
        if len(cols) < 5:
            continue
        if cols[0].lower() == "round":
            continue
        if cols[0].startswith("---"):
            continue
        out.append("| " + " | ".join(cols[:5]) + " |")
    return out


def compose_index(services: list[str], existing: dict[str, StatusRow], timeline_rows: list[str]) -> str:
    merged: list[StatusRow] = []
    seen = set()

    for service in services:
        row = existing.get(service, StatusRow(service=service))
        merged.append(row)
        seen.add(service)

    for service, row in existing.items():
        if service in seen:
            continue
        merged.append(row)

    today = str(date.today())
    lines = [
        "# Refactor Index",
        "",
        "## Scope",
        "- Refactor unit: service boundary",
        f"- Last sync date: {today}",
        "",
        "## Service Status",
        "| Service | Status (`pending`/`in-progress`/`done`) | Owner | Last Updated | Commit |",
        "|---|---|---|---|---|",
    ]

    for row in merged:
        lines.append(
            f"| {row.service} | {row.status} | {row.owner} | {row.last_updated} | {row.commit} |"
        )

    lines.extend(
        [
            "",
            "## Next Pick Rule",
            "- Pick first `in-progress` service.",
            "- If none exists, pick first `pending` service.",
            "- Always skip services with `done`.",
            "",
            "## Round Timeline",
            "| Round | Service | Result | Commit | Date |",
            "|---|---|---|---|---|",
        ]
    )

    lines.extend(timeline_rows)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    excludes = set(parse_csv(args.exclude_dirs))
    service_roots = parse_csv(args.service_roots)

    index_path = (repo_root / args.index_file).resolve()
    index_path.parent.mkdir(parents=True, exist_ok=True)

    old_content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    old_status = parse_status_rows(old_content)
    timeline_rows = parse_timeline_rows(old_content)

    services = discover_services(repo_root, service_roots, excludes)
    new_content = compose_index(services, old_status, timeline_rows)

    if args.dry_run:
        print(new_content, end="")
        return 0

    index_path.write_text(new_content, encoding="utf-8")
    print(f"[OK] Synced {index_path}")
    print(f"[OK] Discovered services: {len(services)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
