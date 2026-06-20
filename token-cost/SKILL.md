---
name: token-cost
version: 1.0.0
description: >
  Run when the user invokes /token-cost or asks for the real / floor / bedrock /
  self-cost price of LLM tokens on a self-hosted server (electricity plus hardware
  amortization, not market API price). The skill measures power draw and generation
  speed ON the server (nvidia-smi, a streaming benchmark) and asks for the electricity
  tariff, hardware cost and amortization period, then prints cost per 1M input/output
  tokens. Use for "сколько на самом деле стоит токен", capacity and break-even planning.
---

# Token floor cost

Estimate the **lower bound** of a self-hosted token: electricity plus hardware
amortization. This is the bedrock below which a token physically cannot cost; it
is NOT the market price (training, salaries, rent, margin are ignored on purpose).
Method from the article *"Почём нынче токен для народа?"*
([@evilfreelancer](https://t.me/evilfreelancer)).

## Formula

```
C_1M = ((P_kW * T_kWh + S / H_life) * 1e6) / (R_tok_s * 3600)
```

- `P_kW` real power draw under load (kW)   - `T_kWh` tariff (RUB/kWh)
- `S` hardware cost (RUB)                  - `H_life` lifetime hours = years*365*24
- `R_tok_s` speed (decode for output, prefill for input)

Compute input and output separately: prefill is many times faster than decode, so
the input token is that many times cheaper. Electricity is the absolute floor;
amortization is the realistic one and is usually the bigger number.

## Inputs: measure on the server vs ask the user

| Input | How to get it |
|-------|---------------|
| `P_kW` power | **Measure** while the model is generating: `token_cost.py measure-power`, or `--measure-power` on compute. Falls back to `--power-kw` if you cannot run nvidia-smi. |
| `R_tok_s` decode + prefill | **Measure** against the running endpoint: `bench_speed.py`. Or read tok/s from the serving engine logs (vLLM/llama.cpp). Else ask the user. |
| `T_kWh` tariff | **Ask** the user (regional, e.g. ~6.97 RUB/kWh for Saint Petersburg). |
| `S` hardware cost | **Ask** the user. Omit for an electricity-only floor. |
| `H_life` years | **Ask**; default 5. |
| utilization | **Ask**; default 1.0. If the GPU is idle part of the time, amortization per useful token rises (50% busy ⇒ doubles). |

## Workflow

1. **Identify the server / model.** If not given, ask which host and which served model.
2. **Power:** ensure the model is under load, then measure. Set `--overhead-w` for the
   non-GPU draw (CPU, board, PSU loss); nvidia-smi only sees the GPUs.
3. **Speed:** run `bench_speed.py` against the endpoint for decode and prefill tok/s.
4. **Ask** for tariff, hardware cost, lifetime, utilization.
5. **Compute** and present the table. State clearly it is a floor, not a sale price.
6. If the user wants a market comparison, contrast with provider prices, but never
   call the floor a "real price".

## Quick reference

```bash
# Measure real power while the model generates (sum of GPUs + overhead) -> kW
python3 scripts/token_cost.py measure-power --overhead-w 150

# Measure decode + prefill speed against an OpenAI-compatible endpoint
python3 scripts/bench_speed.py --base-url http://localhost:8000 --model gpt-oss-120b

# Full estimate (measuring power live), with amortization
python3 scripts/token_cost.py compute \
    --measure-power --overhead-w 150 \
    --tariff 6.97 --decode-tok-s 90 --prefill-tok-s 1440 \
    --hw-cost 700000 --life-years 5 --utilization 1.0

# Pure math, electricity-only (no hardware), power given
python3 scripts/token_cost.py compute --power-kw 0.5 --tariff 6.97 --decode-tok-s 90
```

Run any script with `--help` for all flags.

## Common mistakes

- **Using peak instead of real draw.** Card power-limited to 250 W draws far less than
  its 450 W rating; measure under actual inference, do not read the nameplate.
- **Charging prefill at the decode rate.** Measure both; the input row uses prefill tok/s.
- **Ignoring utilization.** A half-idle server doubles amortization per token; the tariff
  only scales the (smaller) electricity part linearly.
- **Calling it the real price.** It is the floor. Say so.
