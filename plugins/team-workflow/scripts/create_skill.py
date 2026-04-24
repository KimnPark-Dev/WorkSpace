import argparse
import json
import sys

from workspace_workflow import create_skill


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    print(json.dumps(create_skill(args.name), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
