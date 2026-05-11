# Distribution Playbook — Landing Page Roast

## Show HN Post

**Title (79 chars):**
```
Show HN: Landing page roaster – paste a URL, get specific improvement suggestions
```

**First comment (post immediately after submission):**

```
Hey HN — here's what the script actually checks:

1. Headline: Is your H1 benefit-oriented or a company-name dump? (checks framing + word count)
2. CTA: How many? Any above the fold? (scans first 30% of HTML)
3. Load weight: Page size in KB — fast proxy for mobile bounce
4. Social proof: Testimonials, logos, user counts, press mentions
5. Mobile: Viewport meta tag present
6. Trust signals: Privacy policy link, contact info, refund/guarantee mention
7. Word count: Flags pages under 150 words (too thin) or over 3000 (wall of text)
8. Meta description: Length and presence check
9. Image alt text: Accessibility/SEO baseline

Example output from roasting Notion's landing page:

---
Score: 71/100 — Grade C

## Headline
WARN — 8/15
H1: "Your wiki, docs, & projects. Together."
Feature list rather than a single benefit statement. "Together" is vague.
> Fix: Lead with the outcome — e.g. "Stop switching apps. One workspace for your whole team."

## Social Proof
FAIL — 5/15
No testimonial text or star ratings detected in page source.
> Fix: Add 2-3 named testimonials above the fold. Even one real quote with a title lifts conversion.
---

Runs with: pip install requests beautifulsoup4 && python3 roast.py --url https://yoursite.com

Repo: https://github.com/YourManz/landing-page-roast
MIT licensed.

I built a $12 PDF version for people who want a formatted report to hand to a client or team — Gumroad link in the README. Happy to roast pages in this thread if you drop a URL.
```

---

## Response Templates

### "How is this different from Lighthouse?"

> Lighthouse measures performance, accessibility, and SEO signals — render speed, Cumulative Layout Shift, WCAG contrast, structured data. This roasts *conversion copy*: whether your headline leads with a benefit, whether your CTA is above the fold, whether you have any social proof, whether buyers can see a privacy policy before they hand over their credit card. Totally different layer. Run both.

### "Can you roast my page?"

> Drop the URL here and I'll run it and paste the output. Or clone the repo and roast it yourself in 30 seconds — no API key, no account needed.

### "Why is the PDF paid if the script is free?"

> The script is MIT — fork it, extend it, do whatever you want. The $12 covers a formatted, annotated PDF you can drop into a Notion page or hand to a client without them having to read raw Markdown. Same checks, better presentation. The code will always be free.

### "This is just heuristics, a real audit would need…"

> 100% correct — this is a fast pass, not a CRO consultant engagement. It catches the obvious stuff that most pages get wrong: no H1, CTA buried below the fold, zero social proof, no privacy policy. If you want a full user-test-and-heatmap audit, hire someone. If you want a 60-second sanity check before you submit to HN, this is the tool.

---

## Week-1 Action Checklist

- [ ] **Day 1 (Mon-Wed, 8-10am ET):** Submit to Hacker News
- [ ] **Day 1:** Post first comment immediately after submission (see template above)
- [ ] **Day 1:** Star/watch GitHub repo from a few personal accounts to show activity
- [ ] **Day 3:** If >20 upvotes, write a short post roasting a famous startup landing page (Notion, Linear, Lemon Squeezy) and post to r/startups with "I built a tool and tested it on [X]" framing
- [ ] **Day 5:** Offer a free roast in 5 relevant subreddits in exchange for feedback:
  - r/entrepreneur — "Free landing page audit — drop your URL"
  - r/SaaS — same
  - r/indiehackers — mention the script is open source
  - r/webdev — technical angle, mention the checks
  - r/startups — business angle, mention conversion impact
- [ ] **Day 7:** Review any page roasted in the thread — respond with actual output to show it works
- [ ] **Day 14:** If any sales: screenshot the Gumroad dashboard (blurred), tweet it
- [ ] **Day 30:** Check paid PDF downloads. Kill if <5. Promote if ≥5.

---

## Gumroad Listing

**Title:** Landing Page Roast — Full PDF Report

**Price:** $12 USD

**Description:**
```
Your landing page is leaving money on the table. This report tells you exactly where.

9 automated checks covering:
- Headline (benefit-framing vs. feature dump)
- CTA placement and count
- Social proof signals
- Mobile readiness
- Trust signals (privacy policy, contact, refund guarantee)
- Word count (too thin or too long)
- Meta description
- Image alt text
- Load weight

Delivered as a formatted PDF with a prioritized fix list and one-page executive summary.
Same checks as the free open-source script (github.com/YourManz/landing-page-roast) — better presentation.

30-day money-back guarantee. No questions asked.
```

**Tags:**
1. landing-page
2. conversion-rate-optimization
3. cro
4. marketing-tools
5. startup

**Suggested price note:** "Or run the free script yourself on GitHub"
