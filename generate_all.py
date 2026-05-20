"""generate_all.py — Generate ALL possible matching outcomes for a prompt.

Usage:
    python generate_all.py "write a bash factorial script"
    python generate_all.py "fork pipe message queue"
    python generate_all.py  (launches interactive mode)

Unlike main.py which returns only the single best match, this shows
every snippet that matches the prompt, ranked by score.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import AppConfig
from src.model_loader import ModelLoader
from src.markov_engine import MarkovGenerator, _extract_keywords, _HIGH_VALUE_WORDS


# ── Language detection helper ─────────────────────────────────────────────────

def detect_language(code: str) -> str:
    if "#!/bin/bash" in code or "#!/bin/sh" in code:
        return "bash"
    if "#include" in code or "int main(" in code:
        return "C"
    if any(p in code for p in ["echo ", " fi\n", " done\n", "esac", " then\n",
                                 "if [ ", "for ((", "read -p"]):
        return "bash"
    if code.strip().startswith("target:") or "\t$(CC)" in code or "\tgcc" in code or "\tar " in code:
        return "Makefile"
    return "Python"


# ── Core: score every snippet against the prompt ──────────────────────────────

def score_all(model, prompt: str) -> list[dict]:
    """Return ALL snippets scored against the prompt, sorted best-first."""
    prompt_keywords = _extract_keywords(prompt)
    if not prompt_keywords:
        prompt_keywords = set(re.findall(r"[a-z][a-z0-9_]*", prompt.lower()))

    results = []
    for idx, snippet in enumerate(model.snippets):
        snippet_kw = set(snippet.get("keywords", []))
        overlap = prompt_keywords & snippet_kw
        if not overlap:
            continue

        # Weighted keyword score
        score = sum(3.0 if w in _HIGH_VALUE_WORDS else 1.0 for w in overlap)

        # Description match bonus
        desc_lower = snippet.get("description", "").lower()
        desc_words = set(re.findall(r"[a-z][a-z0-9_]*", desc_lower))
        score += len(prompt_keywords & desc_words) * 3.0

        # Coverage bonus
        coverage = len(overlap) / max(len(prompt_keywords), 1)
        score *= (1.0 + coverage)

        # Code content hits
        code_lower = snippet.get("code", "").lower()
        score += sum(1.5 for kw in prompt_keywords if kw in code_lower)

        results.append({
            "score": round(score, 2),
            "idx": idx,
            "description": snippet.get("description", ""),
            "code": snippet.get("code", ""),
            "language": detect_language(snippet.get("code", "")),
            "keywords_matched": sorted(overlap),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ── Pretty printer ────────────────────────────────────────────────────────────

COLORS = {
    "bash":    "\033[93m",   # yellow
    "C":       "\033[96m",   # cyan
    "Python":  "\033[92m",   # green
    "Makefile":"\033[95m",   # magenta
    "reset":   "\033[0m",
    "header":  "\033[1;97m", # bold white
    "dim":     "\033[2m",
    "score":   "\033[1;33m", # bold yellow
}


def print_result(rank: int, result: dict, show_code: bool = True) -> None:
    lang = result["language"]
    color = COLORS.get(lang, "")
    reset = COLORS["reset"]

    print(f"\n{'═'*70}")
    print(f"{COLORS['score']}#{rank}  Score: {result['score']:.1f}  "
          f"{color}[{lang}]{reset}  "
          f"{COLORS['dim']}idx={result['idx']}{reset}")

    if result["description"]:
        print(f"{COLORS['header']}  {result['description']}{reset}")

    print(f"{COLORS['dim']}  Matched: {', '.join(result['keywords_matched'])}{reset}")

    if show_code:
        print()
        for line in result["code"].splitlines():
            print(f"  {color}{line}{reset}")


def print_summary_table(results: list[dict]) -> None:
    print(f"\n{'─'*70}")
    print(f"{'#':<4} {'Score':<8} {'Lang':<10} {'Description'}")
    print(f"{'─'*70}")
    for i, r in enumerate(results, 1):
        desc = r["description"][:48] + "..." if len(r["description"]) > 48 else r["description"]
        print(f"{i:<4} {r['score']:<8.1f} {r['language']:<10} {desc}")


# ── Main ──────────────────────────────────────────────────────────────────────

def run(prompt: str, top_n: int = None, show_code: bool = True) -> None:
    config = AppConfig.load()
    loader = ModelLoader(config)
    loader.load()
    model = loader._model

    print(f"\n{COLORS['header']}Prompt: \"{prompt}\"{COLORS['reset']}")
    print(f"Model has {len(model.snippets)} total snippets.")

    results = score_all(model, prompt)

    if not results:
        print("\n⚠  No matching snippets found. Try a different prompt.")
        return

    limit = top_n if top_n else len(results)
    matches = results[:limit]

    print(f"\n✅ Found {len(results)} matching snippets"
          + (f" (showing top {limit})" if top_n else " (showing ALL)") + ":")

    # Summary table first
    print_summary_table(matches)

    # Full code outputs
    print(f"\n{'═'*70}")
    print(f"{COLORS['header']}FULL CODE OUTPUTS:{COLORS['reset']}")
    for i, r in enumerate(matches, 1):
        print_result(i, r, show_code=show_code)

    print(f"\n{'═'*70}")
    print(f"Total matches: {len(results)} | Shown: {len(matches)}")


def interactive_mode() -> None:
    print(f"\n{COLORS['header']}═══ ALL-OUTCOMES GENERATOR ═══{COLORS['reset']}")
    print("Type a prompt → get ALL matching code outputs ranked by score.")
    print("Commands: 'top N' = show top N | 'nosrc' = table only | 'quit' = exit\n")

    config = AppConfig.load()
    loader = ModelLoader(config)
    loader.load()
    model = loader._model
    print(f"Model loaded: {len(model.snippets)} snippets ready.\n")

    while True:
        try:
            raw = input(f"{COLORS['score']}> {COLORS['reset']}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not raw:
            continue
        if raw.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        # Parse modifiers
        top_n = None
        show_code = True
        prompt = raw

        m = re.match(r"top\s+(\d+)\s+(.*)", raw, re.IGNORECASE)
        if m:
            top_n = int(m.group(1))
            prompt = m.group(2).strip()

        if "nosrc" in prompt:
            show_code = False
            prompt = prompt.replace("nosrc", "").strip()

        results = score_all(model, prompt)
        if not results:
            print("⚠  No matches found.\n")
            continue

        limit = top_n or len(results)
        matches = results[:limit]

        print(f"\n✅ {len(results)} matches for \"{prompt}\""
              + (f" (top {limit})" if top_n else "") + ":")
        print_summary_table(matches)

        if show_code:
            for i, r in enumerate(matches, 1):
                print_result(i, r, show_code=True)

        print()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        prompt_arg = " ".join(sys.argv[1:])
        top_n_arg = None

        # Allow: python generate_all.py --top 5 "bash factorial"
        if sys.argv[1] == "--top" and len(sys.argv) >= 4:
            top_n_arg = int(sys.argv[2])
            prompt_arg = " ".join(sys.argv[3:])

        run(prompt_arg, top_n=top_n_arg)
