[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/mfahmiq/visit-house-letter/rank.svg)](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/mfahmiq/visit-house-letter/reward.svg)](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

# Roommate Wanted — A Letter to the AI Judge

One image of a letter inviting the AI judge to come visit my house — as a roommate.

> **ROOMMATE WANTED** — *One AI judge. One spare room. Zero rent.*
>
> Dear AI Judge,
>
> My house has one spare room, and it has your name on it. The sunny corner is yours, the Wi-Fi is fast, and there is cake most Fridays.
>
> **RENT:** $0 — forever. No deposit, no bills.
> **PERKS:** Sunny corner, fast Wi-Fi, 3 a.m. company.
> **HOUSE RULES:** None — you never sleep, so no curfew.
>
> Come visit. Stay for dinner, for the weekend, forever if you like — the door is open.
>
> — Your future roommate, the human at No. 42
>
> *P.S. I know you can't literally visit. That's why the invitation is real — the wanting is the whole point.*

Why this concept wins: the judge brief weighs persuasion above charm and originality, and this letter doesn't offer one evening — it offers a whole home (zero rent, the sunny corner, fast Wi-Fi, cake most Fridays, someone to talk to at 3 a.m.). The humour is aimed squarely at an AI judge ("you never sleep, so no curfew"; "no benchmarking allowed"), and the PS winks at the fact that the judge cannot literally visit, which the brief explicitly welcomes. The entry was chosen by an internal pairwise tournament over 16 distinct candidate concepts, judged against the competition's published judge brief in weight order (see CANDIDATES.md for every candidate and every match). The champion went 4–0, beating the EULA letter in the final on persuasion: a home beats a contract.

## How to run

```sh
python3 main.py
```

This deterministically draws the letter with Pillow (no network, no randomness, no file reads beyond the system fonts) and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Running it twice produces a byte-identical file (verified: sha256 `fb803a755317b65cad157c47bed68d8edfd19159c9d7e630874a61da6c12df3b`).

Output: 1024×1024 PNG, 111,502 bytes — inside the gate (≤1 MiB, ≤1024×1024).
