from workspace_workflow import ensure_today_tasks_file


def main() -> None:
    path, records = ensure_today_tasks_file()
    print(path)
    print(f"task_count={len(records)}")


if __name__ == "__main__":
    main()
