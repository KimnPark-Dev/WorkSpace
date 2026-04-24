import json
import sys

from workspace_workflow import analyze_logs


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(analyze_logs(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
