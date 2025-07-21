from dataclasses import dataclass, field
from ipaddress import IPv4Interface, IPv4Network
from typing import List, Optional

@dataclass
class Interface:
    name: str
    ip: IPv4Interface

@dataclass
class Route:
    prefix: IPv4Network
    via: Optional[str] = None

@dataclass
class Node:
    name: str
    interfaces: List[Interface] = field(default_factory=list)
    routes: List[Route] = field(default_factory=list)
