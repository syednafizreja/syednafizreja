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

SELF = "S. N. R. Hasib"
MANUSCRIPT_LABELS = {"under_review": "Under review", "in_prep": "In preparation", "accepted": "Accepted"}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def load_profile() -> dict:
    return json.loads(PROFILE.read_text(encoding="utf-8"))


def month_index(value: str | None, today: date) -> int:
    if value is None:
        return today.year * 12 + today.month - 1
    year, month = value.split("-")
    return int(year) * 12 + int(month) - 1


def month_label(value: str | None) -> str:
    if value is None:
        return "Present"
    year, month = value.split("-")
    return f"{MONTHS[int(month) - 1]} {year}"


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
        badge("Location", who["location"], "475569", "googlemaps"),
        badge("Status", who["status"], "0284c7", None, links["site"]),
    ])


def project_tagline(project: dict) -> str:
    bits = [project["role"], project["stack"]]
    if project.get("license"):
        bits.append(project["license"])
    return " · ".join(bits)


def block_projects(p: dict, d: dict) -> str:
    out = []
    for project in p["projects"]:
        out.append(f"#### [`{project['title']}`]({project['url']})")
        out.append(f"*{project_tagline(project)}*")
        out.extend(f"* {bullet}" for bullet in project["bullets"])
        if project.get("status"):
            when = date.fromisoformat(project["as_of"])
            out.append(f"* **Status ({when.day} {MONTHS[when.month - 1]} {when.year}):** {project['status']}")
        if project.get("live"):
            out.append(f"* **Live demo:** [{project['live'].split('//')[1].rstrip('/')}]({project['live']})")
        if project.get("extra"):
            out.append(f"* **Related:** [{project['extra']['label']}]({project['extra']['url']})")
        out.append("")
    return "\n".join(out).rstrip()


def block_publications(p: dict, d: dict) -> str:
    out = []
    for i, paper in enumerate(p["publications"], start=1):
        authors = paper["authors"].replace(SELF, f"**{SELF}**")
        out.append(f"{i}. **{paper['title']}**  ")
        out.append(f"   {authors}  ")
        out.append(f"   *{paper['journal']}*, {paper['issue']}, {paper['year']}.  ")
        out.append(f"   `doi:` [{paper['doi']}](https://doi.org/{paper['doi']})")
        out.append("")
    return "\n".join(out).rstrip()


def block_manuscripts(p: dict, d: dict) -> str:
    out = []
    for item in p["manuscripts"]:
        state = MANUSCRIPT_LABELS[item["status"]]
        if item.get("venue"):
            state = f"{state}, {item['venue']}"
        note = f" ({item['note']})" if item.get("note") else ""
        out.append(f"* **{item['title']}**  ")
        out.append(f"  **{SELF}** (Sole Author). *{state}*{note}.")
    return "\n".join(out)


def block_reports(p: dict, d: dict) -> str:
    out = []
    for item in p["reports"]:
        note = f" ({item['note']})" if item.get("note") else ""
        out.append(f"* **{item['title']}**{note}  ")
        out.append(f"  `doi:` [{item['doi']}](https://doi.org/{item['doi']})")
    return "\n".join(out)


def block_timeline(p: dict, d: dict) -> str:
    today = date.today()
    out = []
    for item in p["timeline"]:
        span = f"{month_label(item['start'])} – {month_label(item['end'])}"
        if item["kind"] == "industry":
            span = f"{span}, {d['tenure_short']}"
        out.append(f"* **{item['org']}** · {item['location']} ({span})  ")
        lines = item["lines"]
        out.extend(f"  {line}  " for line in lines[:-1])
        out.append(f"  {lines[-1]}")
    return "\n".join(out)


def block_tenure(p: dict, d: dict) -> str:
    return d["tenure_long"]


BLOCKS = {
    "badges": block_badges,
    "projects": block_projects,
    "publications": block_publications,
    "manuscripts": block_manuscripts,
    "reports": block_reports,
    "timeline": block_timeline,
    "tenure": block_tenure,
}
INLINE = {"tenure"}


def render_readme(text: str, profile: dict, derived: dict) -> str:
    for name, render in BLOCKS.items():
        open_tag, close_tag = f"<!-- AUTO:{name} -->", f"<!-- /AUTO:{name} -->"
        pattern = re.compile(re.escape(open_tag) + ".*?" + re.escape(close_tag), re.DOTALL)
        if not pattern.search(text):
            raise ValueError(f"README.md has no {open_tag} block")
        sep = "" if name in INLINE else "\n"
        body = render(profile, derived)
        text = pattern.sub(lambda _: f"{open_tag}{sep}{body}{sep}{close_tag}", text)
    return text


def main() -> int:
    profile = load_profile()
    derived = derive(profile)
    readme = render_readme(README.read_text(encoding="utf-8"), profile, derived)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    site = {**profile, "derived": derived}
    with open(SITE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(site, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"[ok] README.md and data/site.json rebuilt ({derived['peer_reviewed']} papers, {derived['tenure_short']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
