#!/usr/bin/env python3
"""
Scans category folders for .md writeups (excluding README.md/TEMPLATE.md),
counts them as "solved", and rewrites the progress table in README.md
between the PROGRESS-TABLE markers.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOTALS_FILE = os.path.join(ROOT, "scripts", "totals.json")
README_FILE = os.path.join(ROOT, "README.md")

EXCLUDED_DIRS = {".github", "scripts", "assets", ".git"}
EXCLUDED_FILES = {"readme.md", "template.md"}

START_MARKER = "<!-- PROGRESS-TABLE-START -->"
END_MARKER = "<!-- PROGRESS-TABLE-END -->"


def count_solved(folder_path):
    if not os.path.isdir(folder_path):
        return 0
    count = 0
    for f in os.listdir(folder_path):
        if f.lower() in EXCLUDED_FILES:
            continue
        if f.lower().endswith(".md"):
            count += 1
    return count


def make_bar(solved, total, width=10):
    if not total:
        return "░" * width
    filled = round(width * min(solved, total) / total)
    return "█" * filled + "░" * (width - filled)


def main():
    with open(TOTALS_FILE, "r") as f:
        totals = json.load(f)

    rows = []
    total_solved = 0
    for folder, meta in totals.items():
        solved = count_solved(os.path.join(ROOT, folder))
        total_solved += solved
        total = meta.get("total")
        name = meta.get("name", folder)
        bar = make_bar(solved, total)
        solved_display = f"**{solved}**" if solved > 0 else "0"
        total_display = total if total else "—"
        rows.append(f"| {name} | {solved_display} | {total_display} | {bar} |")

    table = "| Category | Solved | Total | Progress |\n|---|---|---|---|\n" + "\n".join(rows)
    table += f"\n\n**Total labs solved: {total_solved}**"

    with open(README_FILE, "r") as f:
        readme = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{table}\n{END_MARKER}"

    if not pattern.search(readme):
        raise SystemExit(
            f"Could not find {START_MARKER} / {END_MARKER} markers in README.md"
        )

    new_readme = pattern.sub(replacement, readme)

    if new_readme != readme:
        with open(README_FILE, "w") as f:
            f.write(new_readme)
        print(f"README.md updated. Total solved: {total_solved}")
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
