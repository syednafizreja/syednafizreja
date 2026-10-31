#!/usr/bin/env python3
"""Rebuild everything derived from data/profile.json.

Rewrites the <!-- AUTO:x --> blocks in README.md and writes data/site.json for
the landing page. Counts and tenure are computed here, never typed by hand.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data" / "profile.json"
SITE = ROOT / "data" / "site.json"
README = ROOT / "README.md"

MANUSCRIPT_LABELS = {"under_review": "Under review", "in_prep": "In preparation", "accepted": "Accepted"}


def load_profile() -> dict:
    return json.loads(PROFILE.read_text(encoding="utf-8"))


def month_index(value: str | None, today: date) -> int:
    if value is None:
        return today.year * 12 + today.month - 1
    year, month = value.split("-")
    return int(year) * 12 + int(month) - 1


def plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def derive(profile: dict, today: date | None = None) -> dict:
    """Return every value that must never be typed by hand."""
    today = today or date.today()
    statuses = [m["status"] for m in profile["manuscripts"]]
    unknown = sorted(set(statuses) - set(MANUSCRIPT_LABELS))
    if unknown:
        raise ValueError(f"unknown manuscript status: {unknown}; use one of {sorted(MANUSCRIPT_LABELS)}")

    months = sum(
        month_index(t["end"], today) - month_index(t["start"], today) + 1
        for t in profile["timeline"]
        if t["kind"] == "industry"
    )
    years, rest = divmod(months, 12)
    return {
        "peer_reviewed": len(profile["publications"]),
        "under_review": statuses.count("under_review"),
        "in_prep": statuses.count("in_prep"),
        "reports": len(profile["reports"]),
        "tenure_short": f"{years} yr {rest} mo" if rest else f"{years} yr",
        "tenure_long": f"{plural(years, 'year')} {plural(rest, 'month')}" if rest else plural(years, "year"),
        "orcid_id": profile["links"]["orcid_id"],
        "location": profile["identity"]["location"],
    }


def card_rows(profile: dict, derived: dict) -> list[dict]:
    return [
        {**row, "lines": [line.format_map(derived) for line in row["lines"]]}
        for row in profile["card"]
    ]


def shield(text: str) -> str:
    return quote(text.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="_-.")


def badge(label: str, message: str, color: str, logo: str | None = None, url: str | None = None) -> str:
    logo_args = f"&logo={logo}&logoColor=white" if logo else ""
    image = f"![{label}](https://img.shields.io/badge/{shield(label)}-{shield(message)}-{color}?style=flat-square{logo_args})"
    if url is None:
        return image
    return f"[{image}]({url})"


def block_badges(p: dict, d: dict) -> str:
    links, who = p["links"], p["identity"]
    orcid = links["orcid_id"]
    return "\n".join([
        badge("Website", links["site"].split("//")[1].rstrip("/"), "0ea5e9", "githubpages", links["site"]),
        badge("ORCID", orcid, "a6ce39", "orcid", f"https://orcid.org/{orcid}"),
        badge("ResearchGate", who["name"], "00CCBB", "researchgate", links["researchgate"]),
        badge("LinkedIn", links["linkedin"].rstrip("/").rsplit("/", 1)[1], "0a66c2", None, links["linkedin"]),
        badge("Email", links["email"], "0284c7", "gmail", f"mailto:{links['email']}"),
    ])


def block_projects(p: dict, d: dict) -> str:
    out = []
    for project in p["projects"]:
        live = f" · [Live demo]({project['live']})" if project.get("live") else ""
        out.append(f"* [**{project['name']}**]({project['url']}): {project['summary']}{live}")
    return "\n".join(out)


def block_publications(p: dict, d: dict) -> str:
    return "\n".join(
        f"{i}. [{paper['title']}](https://doi.org/{paper['doi']}), *{paper['journal']}*, {paper['year']}"
        for i, paper in enumerate(p["publications"], start=1)
    )


BLOCKS = {
    "badges": block_badges,
    "projects": block_projects,
    "publications": block_publications,
}


def render_readme(text: str, profile: dict, derived: dict) -> str:
    for name, render in BLOCKS.items():
        open_tag, close_tag = f"<!-- AUTO:{name} -->", f"<!-- /AUTO:{name} -->"
        pattern = re.compile(re.escape(open_tag) + ".*?" + re.escape(close_tag), re.DOTALL)
        if not pattern.search(text):
            raise ValueError(f"README.md has no {open_tag} block")
        body = render(profile, derived)
        text = pattern.sub(lambda _: f"{open_tag}\n{body}\n{close_tag}", text)
    return text


def main() -> int:
    profile = load_profile()
    derived = derive(profile)
    readme = render_readme(README.read_text(encoding="utf-8"), profile, derived)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    site = {**{k: profile[k] for k in ("identity", "links", "projects", "publications", "timeline")}, "derived": derived}
    with open(SITE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(site, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"[ok] README.md and data/site.json rebuilt ({derived['peer_reviewed']} papers, {derived['tenure_short']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
