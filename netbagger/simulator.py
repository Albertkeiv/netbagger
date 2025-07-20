from ipaddress import ip_address
from typing import Dict, List, Tuple

from .model import Node, Route


class Result:
    DELIVERED = 'DELIVERED'
    UNREACHABLE = 'UNREACHABLE'
    LOOP = 'LOOP'


class Step:
    def __init__(self, node: str, info: str):
        self.node = node
        self.info = info

    def __str__(self):
        return f"{self.node}: {self.info}"


def find_node_for_ip(nodes: Dict[str, Node], ip: str) -> Node:
    ip = ip_address(ip)
    found = None
    for node in nodes.values():
        for iface in node.interfaces:
            if ip in iface.network:
                if found:
                    raise ValueError(f"IP {ip} is present on multiple nodes")
                found = node
    return found


def lpm(routes: List[Route], ip) -> List[Route]:
    matches = [r for r in routes if ip in r.prefix]
    if not matches:
        return []
    max_len = max(r.prefix.prefixlen for r in matches)
    return [r for r in matches if r.prefix.prefixlen == max_len]


def simulate(nodes: Dict[str, Node], src_ip: str, dst_ip: str, ecmp: bool = False,
             max_steps: int = 20) -> Tuple[str, List[Step]]:
    src_node = find_node_for_ip(nodes, src_ip)
    if not src_node:
        raise ValueError(f"Source {src_ip} not found in topology")
    if find_node_for_ip(nodes, dst_ip) == src_node:
        return Result.DELIVERED, []

    current = src_node
    steps: List[Step] = []
    visited = set()
    dst_ip_obj = ip_address(dst_ip)

    for _ in range(max_steps):
        # local delivery check
        for iface in current.interfaces:
            if dst_ip_obj in iface.network:
                steps.append(Step(current.name, f"deliver to {dst_ip}"))
                return Result.DELIVERED, steps

        candidates = lpm(current.routes, dst_ip_obj)
        if not candidates:
            steps.append(Step(current.name, 'no route'))
            return Result.UNREACHABLE, steps

        if not ecmp:
            candidates = [candidates[0]]

        for route in candidates:
            key = (current.name, str(route.prefix))
            if key in visited:
                steps.append(Step(current.name, f'loop on {route.prefix}'))
                return Result.LOOP, steps
            visited.add(key)

            if route.via is None:
                if dst_ip_obj in route.prefix:
                    steps.append(Step(current.name, f'direct {route.prefix}'))
                    return Result.DELIVERED, steps
                else:
                    steps.append(Step(current.name, f'no via for {route.prefix}'))
                    return Result.UNREACHABLE, steps
            next_node = find_node_for_ip(nodes, route.via)
            if not next_node:
                steps.append(Step(current.name, f'no next hop {route.via}'))
                return Result.UNREACHABLE, steps
            steps.append(Step(current.name, f'via {route.via} -> {next_node.name}'))
            current = next_node
            break
    steps.append(Step(current.name, 'max steps exceeded'))
    return Result.LOOP, steps
