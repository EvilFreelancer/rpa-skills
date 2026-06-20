# token-cost

**`/token-cost`** — estimate the **floor cost** of a self-hosted LLM token: electricity
plus hardware amortization. This is the physical lower bound (the "bedrock"), not the
market API price. Based on the article
[*Почём нынче токен для народа?*](https://t.me/evilfreelancer) by Pavel Zloi.

The skill gathers the formula inputs by **querying the server** where it can and
**asking the user** for the rest, then prints cost per 1M input/output tokens.

## Formula

```
C_1M = ((P_kW * T_kWh + S / H_life) * 1e6) / (R_tok_s * 3600)
```

| Symbol | Meaning | Source |
|--------|---------|--------|
| `P_kW` | real power draw under load (kW) | measured (`nvidia-smi`) |
| `T_kWh` | electricity tariff (RUB/kWh) | asked |
| `R_tok_s` | speed, decode for output / prefill for input (tok/s) | measured (benchmark) |
| `S` | hardware cost (RUB) | asked |
| `H_life` | lifetime hours = years × 365 × 24 | asked (default 5 y) |

Input and output are computed separately; idle utilization raises the amortization
share per useful token.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions (frontmatter `name`, `version`, `description`). |
| `scripts/token_cost.py` | Math + `measure-power` (samples `nvidia-smi`). stdlib only. |
| `scripts/bench_speed.py` | Measures decode/prefill tok/s against an OpenAI-compatible endpoint. stdlib only. |

## Usage

```bash
# Measure real power while the model is generating
python3 scripts/token_cost.py measure-power --overhead-w 150

# Measure speed against the running endpoint (vLLM / llama.cpp / NeuralDeep)
python3 scripts/bench_speed.py --base-url http://localhost:8000 --model gpt-oss-120b

# Full estimate with amortization
python3 scripts/token_cost.py compute \
    --measure-power --tariff 6.97 \
    --decode-tok-s 90 --prefill-tok-s 1440 \
    --hw-cost 700000 --life-years 5 --utilization 1.0
```

Reference example (2×RTX 4090 48 GB, GPT-OSS-120B, Saint Petersburg tariff) reproduces
the article: ≈10.76 RUB/1M output by electricity, ≈60 RUB/1M output with 5-year
amortization.

## Install

Copy or symlink this `token-cost/` folder into a skill root, e.g.:

- Claude Code — `~/.claude/skills/token-cost/`
- Cursor — `~/.cursor/skills/token-cost/`
- Codex — `~/.codex/skills/token-cost/`

The directory name must match the `name` field in `SKILL.md`.
