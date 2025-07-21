try:
    import yaml

    def _safe_load(src):
        if hasattr(src, "read"):
            return yaml.safe_load(src)
        with open(src) as f:
            return yaml.safe_load(f)
except ImportError:  # fallback to bundled simple parser
    from . import simpleyaml as yaml  # type: ignore

    def _safe_load(src):
        if hasattr(src, "read"):
            src = src.name
        return yaml.load(src)
import os
from ipaddress import ip_network, ip_address
from .model import Node, Interface, Route


def _parse_nodes(data, nodes, source):
    for name, ndata in (data.get("nodes") or {}).items():
        if name in nodes:
            raise ValueError(f"Duplicate node {name} in {source}")
        node = Node(name)
        for idef in ndata.get("interfaces", []):
            net = ip_network(idef["network"], strict=False)
            node.interfaces.append(Interface(idef["name"], net))
        for rdef in ndata.get("routes", []):
            node.routes.append(
                Route(ip_network(rdef["prefix"], strict=False), rdef.get("via"))
            )
        nodes[name] = node


def load_topology(path):
    """Load topology from YAML file or directory and validate it."""
    if os.path.isdir(path):
        files = [
            os.path.join(path, f)
            for f in sorted(os.listdir(path))
            if f.endswith((".yaml", ".yml"))
        ]
    else:
        files = [path]

    nodes = {}
    for fname in files:
        data = _safe_load(fname) or {}
        _parse_nodes(data, nodes, fname)

    validate(nodes)
    return nodes


def validate(nodes):
    """Validate topology for overlaps and dangling next-hops."""
    nets = []
    for node in nodes.values():
        for iface in node.interfaces:
            for nname, nnet in nets:
                if iface.network.overlaps(nnet):
                    raise ValueError(
                        f"Network overlap: {iface.network} on {node.name} overlaps {nnet} on {nname}"
                    )
            nets.append((node.name, iface.network))

    def find_node_for_ip(ip):
        ip = ip_address(ip)
        for n in nodes.values():
            for iface in n.interfaces:
                if ip in iface.network:
                    return n
        return None

    for node in nodes.values():
        for route in node.routes:
            if route.via:
                if not find_node_for_ip(route.via):
                    raise ValueError(
                        f"Route {route.prefix} via {route.via} on {node.name} has unknown next-hop"
                    )
                via_ip = ip_address(route.via)
                if not any(via_ip in iface.network for iface in node.interfaces):
                    raise ValueError(
                        f"Route {route.prefix} via {route.via} on {node.name} is unreachable"
                    )

