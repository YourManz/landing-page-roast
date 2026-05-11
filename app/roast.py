#!/usr/bin/env python3
"""
Landing Page Roast — automated conversion audit
Usage: python3 roast.py --url https://example.com [--output report.md]
"""

import argparse
import sys
import re
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing deps. Run: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Scoring config
# ---------------------------------------------------------------------------
MAX_SCORES = {
    "headline": 15,
    "cta": 15,
    "load_weight": 10,
    "social_proof": 15,
    "mobile": 10,
    "trust": 15,
    "word_count": 10,
    "meta_desc": 5,
    "image_alt": 5,
}
TOTAL_MAX = sum(MAX_SCORES.values())  # 100


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
def fetch_page(url: str) -> tuple[str, int]:
    """Return (html, size_kb). Raises on HTTP error."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; LandingPageRoaster/1.0; "
            "+https://github.com/YourManz/landing-page-roast)"
        )
    }
    resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
    resp.raise_for_status()
    size_kb = len(resp.content) // 1024
    return resp.text, size_kb


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_headline(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["headline"]
    h1_tags = soup.find_all("h1")
    if not h1_tags:
        return {
            "name": "Headline",
            "score": 0,
            "max": max_score,
            "verdict": "FAIL",
            "detail": "No H1 found. Every landing page needs exactly one H1 that states what you do and why it matters.",
            "fix": "Add an H1 with a benefit-first statement, e.g. 'Ship faster landing pages — no designer needed'.",
        }

    h1_text = h1_tags[0].get_text(strip=True)

    # Heuristics: benefit words vs. company-name / vague filler
    benefit_words = [
        "save", "grow", "boost", "increase", "reduce", "stop", "start",
        "get", "build", "launch", "ship", "earn", "convert", "your", "without",
        "faster", "easier", "better", "more", "free", "revenue", "profit",
        "customers", "users", "time", "money",
    ]
    filler_phrases = [
        "we are", "welcome to", "home", "untitled", "coming soon",
        "hello world", "our platform", "the platform",
    ]

    text_lower = h1_text.lower()
    benefit_hit = any(w in text_lower for w in benefit_words)
    filler_hit = any(p in text_lower for p in filler_phrases)
    word_count = len(h1_text.split())
    too_short = word_count < 3
    too_long = word_count > 20

    score = max_score
    notes = []
    fixes = []

    if filler_hit:
        score -= 8
        notes.append(f'H1 contains filler phrasing ("{h1_text[:60]}").')
        fixes.append("Rewrite to lead with the outcome the customer gets, not your company name or 'welcome'.")
    if not benefit_hit and not filler_hit:
        score -= 4
        notes.append("H1 looks feature-focused rather than benefit-focused.")
        fixes.append("Flip the framing: instead of what it *is*, say what the customer *gets*.")
    if too_short:
        score -= 3
        notes.append(f"H1 is only {word_count} word(s) — likely too vague.")
        fixes.append("Expand the H1 to at least 5 words so it communicates a full idea.")
    if too_long:
        score -= 2
        notes.append(f"H1 is {word_count} words — borderline too long for a headline.")
        fixes.append("Trim to under 15 words. Put the extra detail in a subheadline.")
    if len(h1_tags) > 1:
        score -= 2
        notes.append(f"Multiple H1s found ({len(h1_tags)}). Google and screenreaders expect exactly one.")
        fixes.append("Keep one H1 per page. Demote the rest to H2.")

    score = max(0, score)
    verdict = "PASS" if score >= max_score * 0.7 else "WARN" if score >= max_score * 0.4 else "FAIL"

    detail = f'H1 found: "{h1_text[:120]}"'
    if notes:
        detail += "\n" + " ".join(notes)

    return {
        "name": "Headline",
        "score": score,
        "max": max_score,
        "verdict": verdict,
        "detail": detail,
        "fix": " ".join(fixes) if fixes else "Solid headline. No changes needed.",
    }


def check_cta(soup: BeautifulSoup, html: str) -> dict:
    max_score = MAX_SCORES["cta"]

    cta_phrases = [
        "get started", "start free", "sign up", "try free", "buy now", "get access",
        "download", "subscribe", "join", "book a demo", "request demo", "see pricing",
        "start now", "get the report", "purchase", "checkout", "order now",
        "learn more", "view demo", "watch demo",
    ]
    buttons = soup.find_all(["a", "button"])
    cta_count = 0
    cta_texts = []
    for btn in buttons:
        text = btn.get_text(strip=True).lower()
        if any(phrase in text for phrase in cta_phrases) or (
            btn.name == "button" and len(text) > 2 and len(text) < 60
        ):
            cta_count += 1
            cta_texts.append(btn.get_text(strip=True)[:50])

    # Above-fold proxy: check first 30% of HTML for CTA phrase
    fold_html = html[: int(len(html) * 0.30)].lower()
    above_fold = any(phrase in fold_html for phrase in cta_phrases)

    score = max_score
    notes = []
    fixes = []

    if cta_count == 0:
        score = 0
        notes.append("No CTAs detected at all.")
        fixes.append("Add at least one clear CTA button in the hero section.")
    elif cta_count > 6:
        score -= 5
        notes.append(f"{cta_count} CTAs found — too many dilute focus.")
        fixes.append("Pick one primary CTA. Make everything else secondary or remove it.")
    elif cta_count == 1:
        score -= 1  # slight nudge — one CTA is often fine but consider a second lower
        notes.append("Only 1 CTA. Consider adding a second at the bottom of the page.")

    if not above_fold and cta_count > 0:
        score -= 5
        notes.append("No CTA detected in the first 30% of the page (above the fold).")
        fixes.append("Move your primary CTA into the hero section so visitors see it without scrolling.")

    score = max(0, score)
    verdict = "PASS" if score >= max_score * 0.7 else "WARN" if score >= max_score * 0.4 else "FAIL"
    detail = f"{cta_count} CTA(s) found. Above fold: {'yes' if above_fold else 'no'}."
    if cta_texts:
        detail += f" Examples: {', '.join(cta_texts[:3])}."
    if notes:
        detail += " " + " ".join(notes)

    return {
        "name": "CTA",
        "score": score,
        "max": max_score,
        "verdict": verdict,
        "detail": detail,
        "fix": " ".join(fixes) if fixes else "CTAs look solid.",
    }


def check_load_weight(size_kb: int) -> dict:
    max_score = MAX_SCORES["load_weight"]
    if size_kb < 100:
        score = max_score
        detail = f"Page HTML is {size_kb} KB — lightweight."
        fix = "Nothing to do here."
    elif size_kb < 300:
        score = max_score - 2
        detail = f"Page HTML is {size_kb} KB — acceptable."
        fix = "Look for large inline scripts or base64 images you can externalize."
    elif size_kb < 600:
        score = max_score - 5
        detail = f"Page HTML is {size_kb} KB — getting heavy."
        fix = "Defer non-critical scripts, lazy-load images below the fold, and consider a CDN."
    else:
        score = max(0, max_score - 8)
        detail = f"Page HTML is {size_kb} KB — too heavy."
        fix = "This page will feel slow on mobile. Aggressively trim inline assets and defer JS."

    verdict = "PASS" if score >= max_score * 0.7 else "WARN" if score >= max_score * 0.4 else "FAIL"
    return {"name": "Load Weight", "score": score, "max": max_score, "verdict": verdict, "detail": detail, "fix": fix}


def check_social_proof(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["social_proof"]
    text = soup.get_text(" ", strip=True).lower()
    signals = {
        "testimonials/reviews": any(w in text for w in ["testimonial", "review", "reviews", "rated", "stars", "★"]),
        "customer logos": any(w in text for w in ["trusted by", "used by", "customers include", "as seen in", "powered by"]),
        "social numbers": bool(re.search(r"\d[\d,]+\s*(users|customers|teams|companies|startups|founders)", text)),
        "press mentions": any(w in text for w in ["techcrunch", "product hunt", "featured in", "as seen on", "forbes", "hacker news"]),
        "case studies": any(w in text for w in ["case study", "success story", "how .* uses", "increased by", "reduced by"]),
    }
    hits = sum(signals.values())
    score = min(max_score, hits * (max_score // 3))
    if hits == 0:
        score = 0

    found = [k for k, v in signals.items() if v]
    missing = [k for k, v in signals.items() if not v]

    verdict = "PASS" if score >= max_score * 0.6 else "WARN" if score >= max_score * 0.3 else "FAIL"
    detail = f"Social proof signals found: {', '.join(found) if found else 'none'}."
    fix = (
        f"Add these missing signals: {', '.join(missing[:2])}. Even one real testimonial with a name and company lifts conversion significantly."
        if missing else "Strong social proof coverage."
    )
    return {"name": "Social Proof", "score": score, "max": max_score, "verdict": verdict, "detail": detail, "fix": fix}


def check_mobile(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["mobile"]
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport and "width=device-width" in (viewport.get("content") or ""):
        return {
            "name": "Mobile Readiness",
            "score": max_score,
            "max": max_score,
            "verdict": "PASS",
            "detail": f'Viewport meta tag found: "{viewport.get("content")}".',
            "fix": "Mobile-ready at the meta level. Still worth testing on real devices.",
        }
    elif viewport:
        return {
            "name": "Mobile Readiness",
            "score": max_score - 4,
            "max": max_score,
            "verdict": "WARN",
            "detail": f'Viewport meta found but content looks off: "{viewport.get("content")}".',
            "fix": 'Set to <meta name="viewport" content="width=device-width, initial-scale=1">.',
        }
    else:
        return {
            "name": "Mobile Readiness",
            "score": 0,
            "max": max_score,
            "verdict": "FAIL",
            "detail": "No viewport meta tag. Page will render as desktop on mobile — conversion killer.",
            "fix": 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> in <head>.',
        }


def check_trust(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["trust"]
    text = soup.get_text(" ", strip=True).lower()
    links = [a.get("href", "").lower() for a in soup.find_all("a", href=True)]

    privacy = any("privacy" in lnk or "privacy-policy" in lnk for lnk in links) or "privacy policy" in text
    terms = any("terms" in lnk or "tos" in lnk for lnk in links) or "terms of service" in text or "terms & conditions" in text
    contact = any(
        w in text for w in ["contact us", "contact@", "support@", "email us", "get in touch"]
    ) or any("contact" in lnk for lnk in links)
    secure = soup.find("meta", attrs={"http-equiv": "Content-Security-Policy"}) is not None or any(
        "ssl" in text or "secure" in text or "https" in text for _ in [1]
    )
    refund = any(w in text for w in ["refund", "money back", "money-back", "guarantee", "30-day"])

    signals = {"privacy policy": privacy, "terms link": terms, "contact info": contact, "refund/guarantee": refund}
    hits = sum(signals.values())
    score = min(max_score, round(hits / len(signals) * max_score))

    found = [k for k, v in signals.items() if v]
    missing = [k for k, v in signals.items() if not v]

    verdict = "PASS" if score >= max_score * 0.6 else "WARN" if score >= max_score * 0.3 else "FAIL"
    detail = f"Trust signals present: {', '.join(found) if found else 'none'}."
    fix = (
        f"Missing: {', '.join(missing)}. "
        "Add a privacy policy link in the footer at minimum — required in most jurisdictions and expected by buyers."
        if missing else "Good trust signal coverage."
    )
    return {"name": "Trust Signals", "score": score, "max": max_score, "verdict": verdict, "detail": detail, "fix": fix}


def check_word_count(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["word_count"]
    # Strip scripts/styles before counting
    for tag in soup(["script", "style", "noscript", "head"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    words = len(text.split())

    if words < 150:
        score = max(0, max_score - 6)
        detail = f"Only {words} words — page is too thin to build trust or answer objections."
        fix = "Add a benefits section, FAQ, or short testimonials to reach ~400-800 words."
        verdict = "FAIL"
    elif words < 400:
        score = max_score - 3
        detail = f"{words} words — lean but workable. Make sure every objection is addressed."
        fix = "Consider adding a short FAQ or one testimonial block to handle buyer hesitation."
        verdict = "WARN"
    elif words <= 3000:
        score = max_score
        detail = f"{words} words — solid content density."
        fix = "Word count is in the sweet spot."
        verdict = "PASS"
    else:
        score = max_score - 4
        detail = f"{words} words — long. Readers scan, they don't read."
        fix = "Cut ruthlessly. Move deep content to a blog post or FAQ page and link to it."
        verdict = "WARN"

    return {"name": "Word Count", "score": score, "max": max_score, "verdict": verdict, "detail": detail, "fix": fix}


def check_meta_desc(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["meta_desc"]
    meta = soup.find("meta", attrs={"name": "description"})
    if not meta or not meta.get("content"):
        return {
            "name": "Meta Description",
            "score": 0,
            "max": max_score,
            "verdict": "FAIL",
            "detail": "No meta description. Google will auto-generate one — usually poorly.",
            "fix": "Add a 120-160 character meta description that mirrors your H1 benefit and includes a soft CTA.",
        }
    content = meta["content"]
    length = len(content)
    if length < 70:
        score = max_score - 2
        detail = f"Meta description too short ({length} chars): '{content[:80]}'"
        fix = "Expand to 120-160 characters."
        verdict = "WARN"
    elif length > 160:
        score = max_score - 1
        detail = f"Meta description too long ({length} chars) — Google will truncate it."
        fix = "Trim to under 160 characters."
        verdict = "WARN"
    else:
        score = max_score
        detail = f"Meta description ({length} chars): '{content[:80]}...'"
        fix = "Looks good."
        verdict = "PASS"
    return {"name": "Meta Description", "score": score, "max": max_score, "verdict": verdict, "detail": detail, "fix": fix}


def check_image_alt(soup: BeautifulSoup) -> dict:
    max_score = MAX_SCORES["image_alt"]
    imgs = soup.find_all("img")
    if not imgs:
        return {"name": "Image Alt Text", "score": max_score, "max": max_score, "verdict": "PASS",
                "detail": "No images found — nothing to check.", "fix": "N/A"}
    missing_alt = [img for img in imgs if not img.get("alt")]
    ratio = len(missing_alt) / len(imgs)
    if ratio == 0:
        score = max_score
        detail = f"All {len(imgs)} image(s) have alt text."
        fix = "Great."
        verdict = "PASS"
    elif ratio < 0.4:
        score = max_score - 2
        detail = f"{len(missing_alt)}/{len(imgs)} images missing alt text."
        fix = "Add descriptive alt text to every product/screenshot image. Skip decorative images (alt='')."
        verdict = "WARN"
    else:
        score = max(0, max_score - 4)
        detail = f"{len(missing_alt)}/{len(imgs)} images missing alt text — accessibility and SEO impact."
        fix = "Add alt text to all meaningful images. Use alt='' for pure decoration."
        verdict = "FAIL"
    return {"name": "Image Alt Text", "score": score, "max": max_score, "verdict": verdict, "detail": detail, "fix": fix}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def grade(score: int, total: int) -> str:
    pct = score / total * 100
    if pct >= 85:
        return "A"
    if pct >= 70:
        return "B"
    if pct >= 55:
        return "C"
    if pct >= 40:
        return "D"
    return "F"


def build_report(url: str, results: list[dict], total_score: int) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    g = grade(total_score, TOTAL_MAX)
    lines = [
        f"# Landing Page Roast Report",
        f"",
        f"**URL:** {url}  ",
        f"**Date:** {now}  ",
        f"**Score:** {total_score}/{TOTAL_MAX} — Grade {g}",
        f"",
        "---",
        "",
    ]

    verdict_icons = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}

    for r in results:
        icon = verdict_icons[r["verdict"]]
        lines += [
            f"## {r['name']}",
            f"**{icon}** — {r['score']}/{r['max']}",
            "",
            r["detail"],
            "",
            f"> **Fix:** {r['fix']}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Summary",
        "",
        f"Total score: **{total_score}/{TOTAL_MAX}** (Grade {g})",
        "",
    ]

    fails = [r for r in results if r["verdict"] == "FAIL"]
    warns = [r for r in results if r["verdict"] == "WARN"]
    passes = [r for r in results if r["verdict"] == "PASS"]

    if fails:
        lines.append(f"**Critical issues ({len(fails)}):** {', '.join(r['name'] for r in fails)}")
    if warns:
        lines.append(f"**Warnings ({len(warns)}):** {', '.join(r['name'] for r in warns)}")
    if passes:
        lines.append(f"**Passing ({len(passes)}):** {', '.join(r['name'] for r in passes)}")

    lines += [
        "",
        "---",
        "",
        "*Generated by [Landing Page Roast](https://github.com/YourManz/landing-page-roast). "
        "For a formatted PDF report: [Get it for $12 on Gumroad](https://gumroad.com/l/landing-page-roast)*",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def roast(url: str) -> tuple[str, int]:
    print(f"Fetching {url} ...", file=sys.stderr)
    html, size_kb = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")

    results = [
        check_headline(soup),
        check_cta(soup, html),
        check_load_weight(size_kb),
        check_social_proof(soup),
        check_mobile(soup),
        check_trust(soup),
        check_word_count(BeautifulSoup(html, "html.parser")),  # fresh soup (word_count mutates)
        check_meta_desc(soup),
        check_image_alt(soup),
    ]
    total = sum(r["score"] for r in results)
    report = build_report(url, results, total)
    return report, total


def main():
    parser = argparse.ArgumentParser(description="Landing Page Roast — automated conversion audit")
    parser.add_argument("--url", required=True, help="URL to roast")
    parser.add_argument("--output", help="Write report to this file (default: stdout)")
    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url

    report, score = roast(url)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to {args.output} (score: {score}/{TOTAL_MAX})", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
