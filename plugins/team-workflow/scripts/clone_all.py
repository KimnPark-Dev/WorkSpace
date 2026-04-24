import json
import sys

from workspace_workflow import clone_all


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(clone_all(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
