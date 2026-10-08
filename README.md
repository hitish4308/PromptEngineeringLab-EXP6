# Prompt Engineering Lab - Experiment 6

## Role-Based and Negative Prompting

Demonstrates how a role assignment changes tone and how negative
constraints shape the content of LLM output.

## Task

Explain the importance of exercise, under three conditions:

| # | Variant | What it adds |
|---|---------|--------------|
| 1 | Baseline | Nothing - plain question |
| 2 | Role-based | "You are a motivational fitness coach." |
| 3 | Role + negative | Role + "Do not use medical jargon. Do not mention weight loss." |

## Model and Parameters

- Model: openai/gpt-oss-20b
- Temperature: 0.5 (identical for all three prompts)
- Max tokens: 500

## Setup

Reuse the environment from Experiment 1:

    Copy-Item ..\EXP_1\.env .
    python -m pip install -r requirements.txt

## Run

    python role_vs_negative.py

## Expected Output

- Three labelled response blocks (baseline, role-based, role+negative)
- A tone analysis (exclamation marks, second-person mentions)
- A forbidden-term check (medical jargon + weight-loss vocabulary)
- A summary of findings

## Key Findings

1. **Role effect**
   - Shifts tone toward energetic, conversational, second-person voice
   - Increases exclamation marks and "you" mentions
   - Makes the writing feel like advice rather than reference material

2. **Negative constraint effect**
   - Removes named terms reliably when they are specific
   - Broader bans ("don't be technical") work less well

3. **Combined approach**
   - Role + negative constraints give the most precise control over
     tone and vocabulary
   - The forbidden-term counter in the script verifies compliance

## When to Use

| Goal | Technique |
|------|-----------|
| Control tone / personality | Role prompt |
| Exclude specific terms | Negative constraint (name them) |
| Precise style for a brand/audience | Both together |

## Security

- Never commit .env
- Never paste API keys in chat, logs, or screenshots

## License

For educational / lab use only.
