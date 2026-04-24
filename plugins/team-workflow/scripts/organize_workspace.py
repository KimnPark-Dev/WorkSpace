import argparse
import json
import sys

from workspace_workflow import organize


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id")
    args = parser.parse_args()
    print(json.dumps(organize(args.project_id), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
