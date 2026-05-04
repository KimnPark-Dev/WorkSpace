import sys, json, os
from datetime import datetime, timezone

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace = os.path.dirname(os.path.dirname(script_dir))

try:
    with open(os.path.join(workspace, 'config.local.json')) as f:
        member = json.load(f).get('member', 'unknown')
except Exception:
    member = 'unknown'

d = json.load(sys.stdin)
entry = {
    'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'type': 'user_prompt',
    'member': member,
    'session_id': d.get('session_id', ''),
    'content': d.get('prompt', '')
}

log_path = os.path.join(workspace, 'logs', f'conv-{member}.jsonl')
with open(log_path, 'a') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
