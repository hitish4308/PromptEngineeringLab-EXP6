"""
Experiment 6 - Role-Based and Negative Prompting

Compares three prompt variants for the same core question:
  1. Baseline (no role, no constraints)
  2. Role-based only ("You are a motivational fitness coach.")
  3. Role + negative constraints ("Do not use medical jargon.
     Do not mention weight loss.")

Shows how role changes tone and how negative constraints shape output.
"""

import os
import re
import textwrap
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ---------- Setup ----------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.environ.get("NVIDIA_API_KEY")
if not api_key:
    raise SystemExit("NVIDIA_API_KEY not found. Create a .env file.")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)

MODEL = "openai/gpt-oss-20b"
TEMPERATURE = 0.5
MAX_TOKENS = 500


# ---------- Prompts ----------
BASELINE_PROMPT = "Explain the importance of exercise."

ROLE_PROMPT = (
    "You are a motivational fitness coach.\n"
    "Explain the importance of exercise."
)

ROLE_NEG_PROMPT = (
    "You are a motivational fitness coach.\n"
    "Do not use any medical jargon.\n"
    "Do not mention weight loss.\n\n"
    "Explain the importance of exercise."
)


# ---------- Forbidden Terms (to check negative constraints) ----------
FORBIDDEN_TERMS = [
    # medical jargon
    "cardiovascular", "hypertension", "metabolic", "aerobic",
    "anaerobic", "cholesterol", "insulin", "glucose",
    "mitochondria", "cortisol", "endorphins", "serotonin",
    # weight loss mentions
    "weight loss", "lose weight", "slim", "fat burning",
    "burn fat", "calorie", "calories",
]


# ---------- Helpers ----------
def ask_llm(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        content = resp.choices[0].message.content
        return (content or "").strip() or "[no content returned]"
    except Exception as e:
        return f"[API error] {type(e).__name__}: {e}"


def find_forbidden(text: str) -> list:
    """Return any forbidden terms found in the response (case-insensitive)."""
    found = []
    low = text.lower()
    for term in FORBIDDEN_TERMS:
        if term in low:
            found.append(term)
    return found


def show(label: str, prompt: str, response: str):
    width = 72
    print("=" * width)
    print(f"  {label}")
    print("=" * width)
    print("PROMPT:")
    print(textwrap.indent(prompt, "  "))
    print()
    print("RESPONSE:")
    print(textwrap.indent(response, "  "))
    print()
    print(f"  [chars: {len(response)} | words: {len(response.split())}]")
    print()


# ---------- Main ----------
if __name__ == "__main__":
    print(f"Model: {MODEL}")
    print(f"Temperature: {TEMPERATURE} | Max tokens: {MAX_TOKENS}")

    # Baseline
    base_resp = ask_llm(BASELINE_PROMPT)
    show("1. BASELINE (no role, no constraints)",
         BASELINE_PROMPT, base_resp)

    # Role-based
    role_resp = ask_llm(ROLE_PROMPT)
    show("2. ROLE-BASED (motivational fitness coach)",
         ROLE_PROMPT, role_resp)

    # Role + negative
    rn_resp = ask_llm(ROLE_NEG_PROMPT)
    show("3. ROLE + NEGATIVE (no jargon, no weight loss)",
         ROLE_NEG_PROMPT, rn_resp)

    # ---------- Analysis ----------
    print("=" * 72)
    print("  ANALYSIS")
    print("=" * 72)

    # Tone indicators
    exclam = lambda t: t.count("!")
    i_you = lambda t: t.lower().count("you")

    print(f"\nTone indicators:")
    print(f"  Exclamation marks  - Baseline: {exclam(base_resp):>3} | "
          f"Role: {exclam(role_resp):>3} | Role+Neg: {exclam(rn_resp):>3}")
    print(f"  'you' mentions     - Baseline: {i_you(base_resp):>3} | "
          f"Role: {i_you(role_resp):>3} | Role+Neg: {i_you(rn_resp):>3}")

    # Forbidden terms check
    base_forbidden = find_forbidden(base_resp)
    role_forbidden = find_forbidden(role_resp)
    rn_forbidden = find_forbidden(rn_resp)

    print(f"\nForbidden-term check (medical jargon / weight loss):")
    print(f"  Baseline   : {len(base_forbidden):>2} matches "
          f"{'(none)' if not base_forbidden else base_forbidden}")
    print(f"  Role       : {len(role_forbidden):>2} matches "
          f"{'(none)' if not role_forbidden else role_forbidden}")
    print(f"  Role+Neg   : {len(rn_forbidden):>2} matches "
          f"{'(none)' if not rn_forbidden else rn_forbidden}")

    # Summary
    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print("""
Findings:

1. ROLE EFFECT
   - The role prompt ("motivational fitness coach") shifts tone toward
     energetic, second-person address ("you"), and uses more
     exclamation marks.
   - The baseline stays neutral and encyclopedic.

2. NEGATIVE CONSTRAINTS EFFECT
   - "Do not use medical jargon" - the Role+Neg response avoids terms
     like 'cardiovascular', 'metabolic', 'endorphins'.
   - "Do not mention weight loss" - the Role+Neg response avoids
     'weight loss', 'burn fat', 'calories'.
   - Occasionally, a model may still violate one constraint; that's
     expected behavior and worth noting.

3. PRACTICAL TAKEAWAYS
   - Roles are a compact way to control tone, vocabulary, and voice.
   - Negative constraints work best when specific (name the exact terms)
     rather than vague ("don't be too technical").
   - Combining role + negative constraints gives the most targeted
     control over output style.
""")
