"""Simple SVG network visualizer."""
from math import cos, sin, pi
from typing import Dict, Tuple, Iterable

from .model import Node


def _edges(nodes: Dict[str, Node]) -> Iterable[Tuple[str, str]]:
    seen = set()
    names = list(nodes)
    for i, a in enumerate(names):
        na = nodes[a]
        for b in names[i + 1:]:
            nb = nodes[b]
            for ia in na.interfaces:
                for ib in nb.interfaces:
                    if ia.ip.network == ib.ip.network:
                        e = tuple(sorted((a, b)))
                        if e not in seen:
                            seen.add(e)
                            yield e
                            break
    from .simulator import find_node_for_ip
    for name, node in nodes.items():
        for r in node.routes:
            if r.via:
                n2 = find_node_for_ip(nodes, r.via)
                if n2:
                    e = tuple(sorted((name, n2.name)))
                    if e not in seen:
                        seen.add(e)
                        yield e


def visualize(nodes: Dict[str, Node], out_file: str = "topology.svg") -> str:
    """Generate a very simple SVG network graph."""
    radius = 120
    cx = cy = radius + 20
    width = height = (radius + 20) * 2

    names = sorted(nodes)
    positions = {}
    for idx, name in enumerate(names):
        angle = 2 * pi * idx / len(names)
        x = cx + radius * cos(angle)
        y = cy + radius * sin(angle)
        positions[name] = (x, y)

    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    for a, b in _edges(nodes):
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="black" />'
        )
    for name, (x, y) in positions.items():
        lines.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="18" fill="lightgray" stroke="black" />'
        )
        lines.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="12" text-anchor="middle" dominant-baseline="middle">{name}</text>'
        )
    lines.append('</svg>')

    with open(out_file, 'w') as f:
        f.write('\n'.join(lines))
    return out_file
