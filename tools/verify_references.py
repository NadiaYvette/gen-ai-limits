#!/usr/bin/env python3
"""Verify references.bib entries against DBLP / arXiv / Unpaywall.

For every entry:
  1. match on DBLP (canonical authors, venue, volume, pages, DOI, ee link);
  2. if an arXiv candidate ID is known, cross-check via the arXiv API;
  3. if a DOI exists, ask Unpaywall for an open-access PDF location.

Outputs:
  - references_verified.json   canonical metadata + status per entry
  - pdfs/<key>.pdf             downloaded OA copies (gitignored)
  - pdfs/manifest.json         source URL + sha256 per downloaded file
  - VERIFICATION.md            human-readable report

Usage: python3 tools/verify_references.py [--download]
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDFS = ROOT / "pdfs"
CACHE = ROOT / "cache"
UA = {"User-Agent": "gen-ai-limits-reference-verifier/1.0 "
                     "(mailto:nadia.yvette.chambers@ik.me)"}
EMAIL = "nadia.yvette.chambers@ik.me"  # Unpaywall requires a contact address
DONE_STATUSES = {"dblp-matched", "crossref-matched", "verified",
                 "arxiv-matched", "manual"}

ENTRIES = [
    dict(key="vaswani2017attention", arxiv="1706.03762",
         dblp="Attention is all you need"),
    dict(key="bender2021stochastic", doi="10.1145/3442188.3445922",
         dblp="On the Dangers of Stochastic Parrots"),
    dict(key="bender2020climbing",
         crossref_doi="10.18653/v1/2020.acl-main.463",
         pdf="https://aclanthology.org/2020.acl-main.463.pdf",
         dblp="Climbing towards NLU meaning form understanding data models"),
    dict(key="ji2023survey",
         dblp="Survey of hallucination in natural language generation"),
    dict(key="dziri2023faith",
         pdf="https://proceedings.neurips.cc/paper_files/paper/2023/file/"
             "deb3c28192f979302c157cb653c15e90-Paper-Conference.pdf",
         dblp="Faith and fate limits of transformers on compositionality"),
    dict(key="valmeekam2023planning", arxiv="2302.06706",
         pdf="https://proceedings.neurips.cc/paper_files/paper/2023/file/"
             "efb2072a358cefb75886a315a6fcf880-Paper-Conference.pdf",
         dblp="planning abilities of large language models critical investigation"),
    dict(key="kambhampati2024llms", reject=("benchmark", "comment"),
         dblp="LLMs can't plan but can help planning LLM-Modulo frameworks"),
    dict(key="mccoy2019right",
         dblp="Right for the wrong reasons syntactic heuristics natural language inference"),
    dict(key="mallen2023trust",
         dblp="When not to trust language models parametric non-parametric memories"),
    dict(key="kadavath2022language", arxiv="2207.05221",
         dblp="Language models mostly know what they know"),
    dict(key="bommasani2021opportunities", arxiv="2108.07258",
         dblp="On the opportunities and risks of foundation models"),
    dict(key="weidinger2021ethical", arxiv="2112.04359",
         dblp="Ethical and social risks of harm from Language Models"),
    dict(key="gao2023rag", arxiv="2312.10997",
         dblp="Retrieval-augmented generation for large language models survey"),
    dict(key="baird1995residual",
         dblp="Residual algorithms reinforcement learning function approximation Baird"),
    dict(key="tsitsiklis1997analysis",
         dblp="analysis temporal-difference learning function approximation Tsitsiklis"),
    dict(key="vanhasselt2018deadly", arxiv="1812.02648",
         dblp="Deep reinforcement learning and the deadly triad"),
    dict(key="nikishin2022primacy",
         pdf="https://proceedings.mlr.press/v162/nikishin22a/nikishin22a.pdf",
         dblp="primacy bias in deep reinforcement learning"),
    dict(key="french1999catastrophic", crossref_doi="10.1016/S1364-6613(99)01294-2",
         reject=("error surfaces", "noise to compute"),
         dblp="Catastrophic forgetting in connectionist networks"),
    dict(key="dohare2024plasticity",
         dblp="Loss of plasticity in deep continual learning"),
    dict(key="janner2019trust",
         pdf="https://proceedings.neurips.cc/paper/2019/file/"
             "5faf461eff3099671ad63c6f3f094f7f-Paper.pdf",
         dblp="When to trust your model model-based policy optimization"),
    dict(key="wittenmark1995adaptive",
         crossref_doi="10.1016/b978-0-08-042375-3.50010-x",
         dblp="Adaptive dual control methods overview Wittenmark"),
    dict(key="borkar1997stochastic",
         crossref_doi="10.1016/S0167-6911(97)90015-3",
         dblp="Stochastic approximation with two time scales Borkar"),
    dict(key="liu2024lost",
         pdf="https://aclanthology.org/2024.tacl-1.9.pdf",
         reject=("in-between", "multi-hop"),
         dblp="Lost in the middle language models long contexts"),
    dict(key="hsieh2024ruler", arxiv="2404.06654",
         dblp="RULER real context size long-context language models"),
    dict(key="nie2025llada", arxiv="2502.09992",
         dblp="Large language diffusion models"),
    dict(key="inception2025mercury", arxiv="2506.17298",
         dblp="Mercury ultra-fast language models diffusion"),
    dict(key="barth2006privacy",
         dblp="Privacy and contextual integrity framework applications"),
    dict(key="nissenbaum2009privacy", manual="book"),
    dict(key="garcez2023neurosymbolic", arxiv="2012.05876",
         crossref_doi="10.1007/s10462-023-10448-w",
         dblp="Neurosymbolic AI 3rd wave"),
    dict(key="trinh2024alphageometry", crossref_doi="10.1038/s41586-024-07403-2",
         dblp="Solving olympiad geometry without human demonstrations"),
    dict(key="hubert2026alphaproof", crossref_doi="10.1038/s41586-025-09833-y",
         dblp="Olympiad-level formal mathematical reasoning AlphaProof"),
    dict(key="arkin2009governing", manual="book"),
    dict(key="bommasani2023fmti", arxiv="2310.12941",
         dblp="Foundation Model Transparency Index"),
    dict(key="ahmed2020dedemocratization", arxiv="2010.15581",
         dblp="de-democratization of AI deep learning compute divide"),
    dict(key="pozzobon2023blackbox",
         dblp="challenges using black-box APIs toxicity evaluation research"),
    dict(key="kapoor2023leakage", arxiv="2207.07048",
         dblp="Leakage reproducibility crisis machine-learning-based science"),
    dict(key="patel2023nomoat", manual="web"),
]


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def similarity(a: str, b: str) -> float:
    na, nb = norm(a), norm(b)
    base = difflib.SequenceMatcher(None, na, nb).ratio()
    if na and nb:
        # containment, symmetric in argument order
        for x, y in ((na, nb), (nb, na)):
            tokens = set(x.split())
            if tokens:
                contained = sum(1 for t in tokens if t in y) / len(tokens)
                base = max(base, contained * 0.95)
    return base


def fetch(url: str, timeout: int = 60, tries: int = 3) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            request = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except Exception as error:  # noqa: BLE001 - backoff and retry
            last = error
            time.sleep(3 * (attempt + 1))
    raise last  # type: ignore[misc]


def fetch_json_cached(url: str, tag: str) -> dict:
    """GET a JSON URL with an on-disk cache so reruns never re-request."""
    CACHE.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", url.lower())[:150]
    path = CACHE / f"{tag}_{slug}.json"
    if path.exists():
        return json.loads(path.read_text())
    data = fetch_json(url)
    path.write_text(json.dumps(data))
    time.sleep(1.0)
    return data


def fetch_json(url: str) -> dict:
    return json.loads(fetch(url).decode("utf-8"))


def dblp_search(query: str) -> list[dict]:
    url = ("https://dblp.org/search/publ/api?q="
           + urllib.parse.quote(query) + "&format=json&h=8")
    try:
        hits = fetch_json_cached(url, "dblp")["result"]["hits"].get("hit", [])
    except Exception as error:  # noqa: BLE001 - report and continue
        print(f"  dblp error: {error}")
        return []
    if isinstance(hits, dict):  # DBLP returns a dict for a single hit
        hits = [hits]
    return [hit["info"] for hit in hits if isinstance(hit, dict) and "info" in hit]


def dblp_authors(info: dict) -> list[str]:
    authors = info.get("authors", {}).get("author", [])
    if isinstance(authors, dict):
        authors = [authors]
    return [a.get("text", "").strip() for a in authors if a.get("text")]


def crossref_by_doi(doi: str) -> dict | None:
    """Exact metadata lookup for a known DOI."""
    url = ("https://api.crossref.org/works/" + urllib.parse.quote(doi)
           + "?mailto=" + EMAIL)
    try:
        item = fetch_json_cached(url, "crdoi")["message"]
    except Exception as error:  # noqa: BLE001
        print(f"  crossref-doi error: {error}")
        return None
    years = (item.get("issued", {}).get("date-parts") or [[None]])[0]
    return {
        "doi": item.get("DOI", ""),
        "title": " ".join(item.get("title") or []),
        "authors": [
            f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
            for a in item.get("author", [])
        ],
        "venue": " ".join(item.get("container-title") or []),
        "volume": item.get("volume", ""),
        "number": item.get("issue", ""),
        "pages": item.get("page", ""),
        "year": str(years[0] or ""),
    }


def crossref_search(title: str) -> dict | None:
    url = ("https://api.crossref.org/works?rows=3&select=DOI,title,author,"
           "container-title,volume,issue,page,issued,type&mailto=" + EMAIL
           + "&query.bibliographic=" + urllib.parse.quote(title))
    try:
        items = fetch_json_cached(url, "crossref")["message"]["items"]
    except Exception as error:  # noqa: BLE001
        print(f"  crossref error: {error}")
        return None
    best, best_score = None, 0.0
    for item in items:
        cr_title = " ".join(item.get("title") or [])
        score = similarity(cr_title, title)
        if score > best_score:
            best, best_score = item, score
    if best is None or best_score < 0.85:
        return None
    years = (best.get("issued", {}).get("date-parts") or [[None]])[0]
    return {
        "doi": best.get("DOI", ""),
        "title": " ".join(best.get("title") or []),
        "authors": [
            f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
            for a in best.get("author", [])
        ],
        "venue": " ".join(best.get("container-title") or []),
        "volume": best.get("volume", ""),
        "number": best.get("issue", ""),
        "pages": best.get("page", ""),
        "year": str(years[0] or ""),
        "crossref_score": round(best_score, 3),
    }


def arxiv_fetch(arxiv_id: str) -> dict | None:
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        root = ET.fromstring(fetch(url))
    except Exception as error:  # noqa: BLE001
        print(f"  arxiv error: {error}")
        return None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entry = root.find("a:entry", ns)
    if entry is None:
        return None
    title = re.sub(r"\s+", " ", entry.findtext("a:title", "", ns)).strip()
    authors = [
        re.sub(r"\s+", " ", a.findtext("a:name", "", ns)).strip()
        for a in entry.findall("a:author", ns)
    ]
    doi = entry.findtext("{http://arxiv.org/schemas/atom}doi", "", ns)
    return {"title": title, "authors": authors, "doi": doi.strip()}


def unpaywall(doi: str) -> dict | None:
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        data = fetch_json(url)
    except Exception:  # noqa: BLE001
        return None
    best = data.get("best_oa_location") or {}
    return {
        "url_for_pdf": best.get("url_for_pdf"),
        "url": best.get("url"),
        "is_oa": data.get("is_oa", False),
        "license": best.get("license"),
    }


def pdf_candidates(entry: dict, dblp_hit: dict | None, upw: dict | None) -> list[str]:
    candidates: list[str] = []
    if entry.get("pdf"):  # hand-picked OA location
        candidates.append(entry["pdf"])
    if entry.get("arxiv"):
        candidates.append(f"https://arxiv.org/pdf/{entry['arxiv']}")
    ee = (dblp_hit or {}).get("ee", "")
    if ee:
        if ee.endswith(".pdf"):
            candidates.append(ee)
        elif "aclanthology.org" in ee:
            candidates.append(ee.rstrip("/") + ".pdf")
        elif "proceedings.mlr.press" in ee and not ee.endswith(".pdf"):
            candidates.append(ee + ".pdf")
        elif "proceedings.neurips.cc" in ee and ee.endswith("-Abstract.html"):
            candidates.append(ee.replace("-Abstract.html", "-Paper.pdf"))
        elif ee.endswith((".html", "/")):
            candidates.append(ee)  # last resort; validated by %PDF check
    if upw and upw.get("url_for_pdf"):
        candidates.append(upw["url_for_pdf"])
    seen: set[str] = set()
    return [c for c in candidates if not (c in seen or seen.add(c))]


def download(url: str) -> bytes | None:
    try:
        data = fetch(url, timeout=120)
    except Exception as error:  # noqa: BLE001
        print(f"  download failed ({url.split('/')[2]}): {error}")
        return None
    if data[:5] != b"%PDF-":
        print(f"  not a PDF: {url.split('/')[2]}")
        return None
    return data


def main() -> int:
    want_download = "--download" in sys.argv
    force = "--force" in sys.argv
    if want_download:
        PDFS.mkdir(exist_ok=True)
    report_path = ROOT / "references_verified.json"
    report: dict[str, dict] = {}
    if report_path.exists() and not force:
        report = json.loads(report_path.read_text())
    manifest: dict[str, dict] = {}
    manifest_path = PDFS / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    for entry in ENTRIES:
        key = entry["key"]
        previous = report.get(key, {})
        previous_status = previous.get("status")
        if previous_status in DONE_STATUSES and not force and (
                not want_download or previous.get("pdf")):
            print(f"== {key}: already {previous_status}; skipping")
            report[key] = previous
            continue
        print(f"== {key}")
        time.sleep(0.5)
        if previous_status in DONE_STATUSES and not force:
            # keep the verified metadata, only retry the download
            record = dict(previous)
            record["_resume"] = True
        else:
            record: dict = {"status": "unverified", "sources": {}}

        if entry.get("manual"):
            record["status"] = "manual"
            report[key] = record
            continue

        dblp_hit = None
        if entry.get("dblp") and not record.get("_resume"):
            hits = dblp_search(entry["dblp"])
            best, best_score = None, 0.0
            for hit in hits:
                lowered = hit.get("title", "").lower()
                if any(rj in lowered for rj in entry.get("reject", ())):
                    continue
                score = similarity(hit.get("title", ""), entry["dblp"])
                if score > best_score:
                    best, best_score = hit, score
            if best is not None and best_score >= 0.82:
                dblp_hit = best
                record["sources"]["dblp"] = best.get("ee", "")
                record["title"] = best.get("title", "")
                record["authors"] = dblp_authors(best)
                record["venue"] = best.get("venue", "")
                record["year"] = best.get("year", "")
                record["volume"] = best.get("volume", "")
                record["number"] = best.get("number", "")
                record["pages"] = best.get("pages", "")
                record["doi"] = best.get("doi", "")
                record["dblp_score"] = round(best_score, 3)
                record["status"] = "dblp-matched"
                print(f"  dblp match ({best_score:.2f}): {best.get('title')}")
            else:
                record["status"] = "dblp-ambiguous"
                if hits:
                    record["dblp_candidates"] = [
                        {"title": h.get("title", ""), "year": h.get("year", ""),
                         "ee": h.get("ee", "")} for h in hits[:4]
                    ]
                print("  NO confident dblp match")

        if entry.get("arxiv") and not record.get("_resume"):
            time.sleep(3.1)  # arXiv API rate limit
            ax = arxiv_fetch(entry["arxiv"])
            if ax:
                record["sources"]["arxiv"] = entry["arxiv"]
                ax_score = similarity(ax["title"], entry["dblp"])
                if dblp_hit is None and ax_score >= 0.82:
                    record.update({
                        "status": "arxiv-matched",
                        "title": ax["title"],
                        "authors": ax["authors"],
                        "venue": "arXiv",
                        "year": entry["arxiv"][:2],
                    })
                    print(f"  arxiv match ({ax_score:.2f}): {ax['title']}")
                elif dblp_hit is not None and ax_score >= 0.82:
                    if not record.get("authors"):
                        record["authors"] = ax["authors"]
                    if ax.get("doi") and not record.get("doi"):
                        record["doi"] = ax["doi"]
                    record["status"] = "verified"
                    print("  dblp+arxiv agree")
                else:
                    print(f"  arxiv title mismatch ({ax_score:.2f}); "
                          "flagged for manual check")
                    record["arxiv_flag"] = ax["title"]

        doi = record.get("doi") or entry.get("doi")
        if entry.get("crossref_doi") and not record.get("crossref_doi_used"):
            crd = crossref_by_doi(entry["crossref_doi"])
            if crd:
                record["sources"]["crossref-doi"] = crd["doi"]
                for field in ("title", "authors", "venue", "volume",
                              "number", "pages", "year"):
                    if crd.get(field):
                        record[field] = crd[field]
                record["doi"] = crd["doi"]
                record["crossref_doi_used"] = True
                if record["status"] in {"unverified", "dblp-ambiguous"}:
                    record["status"] = "crossref-matched"
                print(f"  crossref-doi: {crd['title'][:60]}")
        upw = None
        if doi:
            upw = unpaywall(doi)
            if upw and upw.get("is_oa"):
                record["sources"]["unpaywall"] = upw.get("url_for_pdf") or upw.get("url")
                record["oa_license"] = upw.get("license")
                print(f"  OA: {upw.get('license')} via unpaywall")

        if record["status"] in {"unverified", "dblp-ambiguous"}:
            cr = crossref_search(entry["dblp"])
            if cr:
                record["sources"]["crossref"] = cr["doi"]
                for field in ("title", "authors", "venue", "volume",
                              "number", "pages", "year"):
                    if cr.get(field) and not record.get(field):
                        record[field] = cr[field]
                if not record.get("doi"):
                    record["doi"] = cr["doi"]
                record["status"] = "crossref-matched"
                print(f"  crossref match ({cr['crossref_score']:.2f}): "
                      f"{cr['title'][:60]}")

        if dblp_hit and entry.get("arxiv") and record["status"] != "verified":
            record["status"] = "dblp-matched"
        if dblp_hit and not entry.get("arxiv"):
            record["status"] = "dblp-matched"

        if want_download and not entry.get("manual"):
            path = PDFS / f"{key}.pdf"
            if path.exists():
                record["pdf"] = f"pdfs/{key}.pdf"
            else:
                for url2 in pdf_candidates(entry, dblp_hit, upw):
                    data = download(url2)
                    if data:
                        path.write_bytes(data)
                        manifest[key] = {
                            "source_url": url2,
                            "sha256": hashlib.sha256(data).hexdigest(),
                            "bytes": len(data),
                        }
                        record["pdf"] = f"pdfs/{key}.pdf"
                        print(f"  saved {len(data) // 1024} KiB from "
                              f"{url2.split('/')[2]}")
                        break

        record.pop("_resume", None)
        report[key] = record

    (ROOT / "references_verified.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    if want_download:
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for record in report.values():
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    print("\n== summary:", json.dumps(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
