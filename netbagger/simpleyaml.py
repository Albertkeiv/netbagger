from typing import Any, List


def _parse_value(val: str) -> Any:
    if val.lower() in {"null", "none", ""}:
        return None
    if val.lower() in {"true", "false"}:
        return val.lower() == "true"
    try:
        return int(val)
    except ValueError:
        pass
    return val


def load(path: str) -> Any:
    with open(path) as f:
        lines = [l.rstrip('\n') for l in f]

    root: Any = {}
    stack: List[tuple[int, Any]] = [(0, root)]

    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith('#'):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        line = raw.strip()
        if line.startswith('- '):
            line = line[2:]
            if ':' in line:
                key, val = line.split(':', 1)
                item = {key.strip(): _parse_value(val.strip())} if val.strip() else {key.strip(): None}
            else:
                item = _parse_value(line)
            if isinstance(container, list):
                container.append(item)
            else:
                container_key = list(container.keys())[-1]
                if container[container_key] is None:
                    container[container_key] = []
                container[container_key].append(item)
            if isinstance(item, dict) and (i + 1) < len(lines):
                next_line = lines[i + 1]
                next_indent = len(next_line) - len(next_line.lstrip(' '))
                if next_indent > indent:
                    stack.append((indent + 2, item))
        else:
            if ':' in line:
                key, val = line.split(':', 1)
                val = val.strip()
                if val == '':
                    new_container = None
                    if (i + 1) < len(lines) and lines[i + 1].lstrip().startswith('- '):
                        new_container = []
                    else:
                        new_container = {}
                    if isinstance(container, list):
                        container.append({key.strip(): new_container})
                    else:
                        container[key.strip()] = new_container
                    stack.append((indent + 2, new_container))
                else:
                    if isinstance(container, list):
                        container.append({key.strip(): _parse_value(val)})
                    else:
                        container[key.strip()] = _parse_value(val)
        i += 1
    return root

