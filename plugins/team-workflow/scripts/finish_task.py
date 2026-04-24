import argparse
import json

from workspace_workflow import finish_task


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    args = parser.parse_args()
    print(json.dumps(finish_task(args.task), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
