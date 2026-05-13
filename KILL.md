# Kill File — landing-page-roast

**Kill date:** 2026-06-10
**Kill signal:** <5 paid roasts by 2026-06-10
**Today:** 2026-05-12

---

## Kill Action

If kill signal is met on 2026-06-10:

```bash
cd ~/Work/ventures/landing-page-roast
git tag killed/landing-page-roast
mkdir -p ~/Work/ventures/_killed
mv ~/Work/ventures/landing-page-roast ~/Work/ventures/_killed/
```

Then update the vault note at `~/Documents/Brainstorm/Factory/landing-page-roast.md`:
- Change `status: live` → `status: killed`
- Add `killed-date: 2026-06-10`

---

## Promote Action

If kill signal NOT met by day 30 and trajectory is upward:
1. Update vault note: `status: optimizing`
2. Bundle: roast + rewrite, raise price to $79

---

## Week-by-Week Check-in

| Day | Check | Action if red |
|-----|-------|---------------|
| 7   | Any sales/clients? | If 0: try alternate distribution angle |
| 14  | 1+ sale/client?    | If 0: rewrite headline, repost |
| 21  | 2+ sales/clients?  | If 1: get testimonial, use as social proof |
| 30  | Kill signal check  | If met: run kill action above |
