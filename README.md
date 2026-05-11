# Landing Page Roast

Paste a URL, get an automated roast report — headline clarity, CTAs, social proof, mobile readiness, trust signals, and more. Score out of 100 with specific "fix this" suggestions per check.

## Quick Start

```bash
pip install requests beautifulsoup4
python3 app/roast.py --url https://example.com
# or save to file:
python3 app/roast.py --url https://example.com --output report.md
```

## Checks

| Check | What it tests |
|-------|--------------|
| Headline | H1 present? Benefit-oriented or feature-dump? |
| CTA | How many? Any above the fold? |
| Load weight | Page size in KB (proxy for speed) |
| Social proof | Reviews, testimonials, logos mentioned |
| Mobile | Viewport meta tag present |
| Trust signals | Privacy policy link, contact info visible |
| Word count | Under 150 (too thin) or over 3000 (too long) |

## Output

Markdown report with a score (0-100) and per-check commentary. Example:

```
# Roast Report: stripe.com
Score: 81/100

## Headline
PASS (score: 14/15)
H1 found: "Financial infrastructure to grow your revenue"
Benefit-framing detected. No "we are a platform" opener. Good.

## CTA
PASS (score: 12/15)
3 CTAs found. "Start now" appears in first 30% of page — above the fold.
...
```

## Paid PDF Version

The script is free and open source. For a formatted, shareable PDF report with design annotations — $12 one-time via Gumroad.

**[Get the Full Roast Report — $12](https://gumroad.com/l/landing-page-roast)**

## Kill Date

2026-06-10 — if <5 paid PDF downloads by that date, this repo is archived.

## License

MIT
