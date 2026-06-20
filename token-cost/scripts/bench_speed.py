#!/usr/bin/env python3
"""Measure prefill and decode speed of an OpenAI-compatible LLM endpoint.

Sends ONE streaming chat completion and times it, so the formula in
token_cost.py gets a real tok/s instead of a guess. Works against vLLM,
llama.cpp server, NeuralDeep, or anything exposing /v1/chat/completions.

Reported:
    decode tok/s   - steady-state output speed (used for output token cost)
    prefill tok/s  - prompt_tokens / time-to-first-token (used for input cost)
    TTFT           - time to first token, seconds

stdlib only (urllib). Token counts come from the server `usage` block when
present; otherwise output tokens are approximated by counting stream chunks.
"""

import argparse
import json
import sys
import time
import urllib.request


def build_payload(args: argparse.Namespace) -> bytes:
    body = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.prompt}],
        "max_tokens": args.max_tokens,
        "temperature": 0,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    return json.dumps(body).encode("utf-8")


def bench(args: argparse.Namespace) -> dict:
    url = args.base_url.rstrip("/") + "/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"

    req = urllib.request.Request(url, data=build_payload(args), headers=headers)

    t_start = time.perf_counter()
    t_first = None
    chunk_tokens = 0
    usage = None

    with urllib.request.urlopen(req, timeout=args.timeout) as resp:
        for raw in resp:
            line = raw.decode("utf-8").strip()
            if not line.startswith("data:"):
                continue
            data = line[len("data:"):].strip()
            if data == "[DONE]":
                break
            event = json.loads(data)
            if event.get("usage"):
                usage = event["usage"]
            for choice in event.get("choices", []):
                delta = choice.get("delta", {})
                if delta.get("content"):
                    if t_first is None:
                        t_first = time.perf_counter()
                    chunk_tokens += 1

    t_end = time.perf_counter()
    if t_first is None:
        raise RuntimeError("no content tokens streamed back")

    ttft = t_first - t_start
    decode_seconds = max(t_end - t_first, 1e-9)
    completion_tokens = (usage or {}).get("completion_tokens") or chunk_tokens
    prompt_tokens = (usage or {}).get("prompt_tokens")

    # decode rate uses tokens AFTER the first one over the decode window
    decode_tok_s = max(completion_tokens - 1, 1) / decode_seconds
    prefill_tok_s = prompt_tokens / ttft if prompt_tokens and ttft > 0 else None

    return {
        "ttft_s": ttft,
        "decode_tok_s": decode_tok_s,
        "prefill_tok_s": prefill_tok_s,
        "completion_tokens": completion_tokens,
        "prompt_tokens": prompt_tokens,
        "approx_tokens": usage is None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", required=True,
                        help="e.g. http://localhost:8000 or https://api.host")
    parser.add_argument("--model", required=True, help="served model id")
    parser.add_argument("--api-key", default=None, help="bearer token if required")
    parser.add_argument("--max-tokens", type=int, default=256,
                        help="output tokens to generate (default 256)")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument(
        "--prompt",
        default=(
            "Summarize the theory of relativity in detail, covering both "
            "special and general relativity, with historical context and "
            "key equations explained step by step."
        ),
        help="use a long prompt for a meaningful prefill number",
    )
    args = parser.parse_args()

    try:
        r = bench(args)
    except Exception as exc:  # noqa: BLE001 - surface any transport/HTTP error plainly
        print(f"benchmark failed: {exc}", file=sys.stderr)
        return 1

    print(f"TTFT          : {r['ttft_s']:.3f} s")
    print(f"decode tok/s  : {r['decode_tok_s']:.1f}")
    if r["prefill_tok_s"] is not None:
        print(f"prefill tok/s : {r['prefill_tok_s']:.1f} "
              f"(prompt_tokens={r['prompt_tokens']})")
    else:
        print("prefill tok/s : unknown (server gave no prompt_tokens; "
              "use TTFT or set it manually)")
    if r["approx_tokens"]:
        print("note          : no usage block; output tokens approximated by chunks")
    print()
    print("Feed these into token_cost.py:")
    prefill = (f" --prefill-tok-s {r['prefill_tok_s']:.0f}"
               if r["prefill_tok_s"] is not None else "")
    print(f"  --decode-tok-s {r['decode_tok_s']:.0f}{prefill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
