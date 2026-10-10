"""Run with: python -m mamba_actuator 'lista las ventanas'."""
import argparse
import json
from .core import parse, simulate


def main() -> int:
    p = argparse.ArgumentParser(description="MAMBA ACTUATOR safe command simulator")
    p.add_argument("command", help="Spanish metacommand")
    args = p.parse_args()
    try:
        result = simulate(parse(args.command))
    except ValueError as exc:
        result = {"status": "denied", "reason": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "simulated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
