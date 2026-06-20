#!/usr/bin/env python3
"""Estimate the floor (lower-bound) cost of LLM tokens.

Based on the formula from the article "Почём нынче токен для народа?"
by Pavel Zloi (https://t.me/evilfreelancer):

    C_1M = ((P_kW * T_kWh + S / H_life) * 1e6) / (R_tok_s * 3600)

This is NOT the market price of a token. It is the physical bedrock:
electricity plus hardware amortization, below which a self-hosted token
cannot go. Training, salaries, rent, margin and the rest are ignored on
purpose.

Two sub-commands:
    compute        run the math from explicit numbers (and/or measured power)
    measure-power  sample nvidia-smi to estimate real power draw in kW

stdlib only - no third-party packages.
"""

import argparse
import subprocess
import sys
import time

SECONDS_PER_HOUR = 3600
HOURS_PER_YEAR = 365 * 24
ONE_MILLION = 1_000_000


def measure_power_kw(samples: int, interval: float, overhead_w: float) -> float:
    """Average GPU power draw over `samples` nvidia-smi reads, plus overhead.

    Sums power.draw across all visible GPUs per sample, averages the samples,
    then adds a fixed overhead in watts for CPU, board, fans and PSU losses.
    Returns kilowatts. The server is expected to be under inference load while
    this runs, otherwise the figure reflects idle draw.
    """
    query = [
        "nvidia-smi",
        "--query-gpu=power.draw",
        "--format=csv,noheader,nounits",
    ]
    totals = []
    for _ in range(samples):
        out = subprocess.run(query, capture_output=True, text=True, check=True)
        per_gpu = [float(x) for x in out.stdout.split("\n") if x.strip()]
        totals.append(sum(per_gpu))
        time.sleep(interval)
    avg_gpu_w = sum(totals) / len(totals)
    return (avg_gpu_w + overhead_w) / 1000.0


def cost_per_1m(per_hour_rub: float, rate_tok_s: float) -> float:
    """Cost of 1,000,000 tokens given a cost-per-hour and a tokens/second rate."""
    return per_hour_rub * ONE_MILLION / (rate_tok_s * SECONDS_PER_HOUR)


def fmt(value: float) -> str:
    return f"{value:.2f}"


def run_compute(args: argparse.Namespace) -> int:
    # 1. Power: measured on the server or passed explicitly.
    if args.measure_power:
        power_kw = measure_power_kw(args.samples, args.interval, args.overhead_w)
        power_src = f"measured via nvidia-smi (+{args.overhead_w:.0f} W overhead)"
    elif args.power_kw is not None:
        power_kw = args.power_kw
        power_src = "given"
    else:
        print("error: pass --power-kw N or --measure-power", file=sys.stderr)
        return 2

    elec_per_hour = power_kw * args.tariff

    # 2. Amortization per hour (optional). Idle time is charged to the tokens
    #    that DID get generated, so utilization < 1 raises the per-token cost.
    am_per_hour = 0.0
    if args.hw_cost is not None:
        life_hours = args.life_years * HOURS_PER_YEAR
        am_per_hour = (args.hw_cost / life_hours) / args.utilization

    full_per_hour = elec_per_hour + am_per_hour

    # 3. Report.
    print("# Token floor cost\n")
    print(f"Power            : {power_kw:.3f} kW ({power_src})")
    print(f"Tariff           : {args.tariff:.2f} RUB/kWh")
    print(f"Electricity/hour : {fmt(elec_per_hour)} RUB")
    if args.hw_cost is not None:
        print(
            f"Hardware         : {args.hw_cost:.0f} RUB over {args.life_years} y "
            f"= {args.life_years * HOURS_PER_YEAR} h, utilization {args.utilization:.0%}"
        )
        print(f"Amortization/hour: {fmt(am_per_hour)} RUB")
    print(f"Total/hour       : {fmt(full_per_hour)} RUB\n")

    has_am = args.hw_cost is not None
    header = f"{'Flow':<8}{'tok/s':>8}{'  electricity':>16}"
    if has_am:
        header += f"{'  +amortization':>18}"
    print(header)
    print("-" * len(header))

    rows = [("output", args.decode_tok_s)]
    if args.prefill_tok_s is not None:
        rows.append(("input", args.prefill_tok_s))

    for name, rate in rows:
        line = f"{name:<8}{rate:>8.0f}{fmt(cost_per_1m(elec_per_hour, rate)):>14} RUB"
        if has_am:
            line += f"{fmt(cost_per_1m(full_per_hour, rate)):>16} RUB"
        print(line)

    print("\nPrices are per 1,000,000 tokens. Electricity-only is the absolute")
    print("floor; the amortization column is the realistic lower bound.")
    return 0


def run_measure_power(args: argparse.Namespace) -> int:
    power_kw = measure_power_kw(args.samples, args.interval, args.overhead_w)
    print(f"{power_kw:.3f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--samples", type=int, default=20,
                        help="nvidia-smi reads to average (default 20)")
    common.add_argument("--interval", type=float, default=0.5,
                        help="seconds between reads (default 0.5)")
    common.add_argument("--overhead-w", type=float, default=150.0,
                        help="non-GPU watts to add: CPU, board, PSU loss (default 150)")

    c = sub.add_parser("compute", parents=[common],
                       help="compute floor cost per 1M tokens")
    c.add_argument("--tariff", type=float, required=True,
                   help="electricity price, RUB per kWh")
    c.add_argument("--decode-tok-s", type=float, required=True,
                   help="output (decode) generation speed, tok/s")
    c.add_argument("--prefill-tok-s", type=float, default=None,
                   help="input (prefill) speed, tok/s; omit to skip the input row")
    power = c.add_mutually_exclusive_group()
    power.add_argument("--power-kw", type=float, default=None,
                       help="real power draw, kW (skip nvidia-smi)")
    power.add_argument("--measure-power", action="store_true",
                       help="measure power draw on this server via nvidia-smi")
    c.add_argument("--hw-cost", type=float, default=None,
                   help="hardware cost in RUB; omit for electricity-only")
    c.add_argument("--life-years", type=float, default=5.0,
                   help="amortization period in years (default 5)")
    c.add_argument("--utilization", type=float, default=1.0,
                   help="useful load fraction 0..1 (default 1.0 = always busy)")
    c.set_defaults(func=run_compute)

    m = sub.add_parser("measure-power", parents=[common],
                       help="print measured power draw in kW and exit")
    m.set_defaults(func=run_measure_power)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
