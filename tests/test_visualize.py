import os
import sys
from ipaddress import ip_interface

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from netbagger.model import Node, Interface
from netbagger.visualize import visualize


def test_visualize_creates_file(tmp_path):
    nodes = {
        'A': Node('A', [Interface('net1', ip_interface('10.0.0.1/24'))]),
        'B': Node('B', [Interface('net1', ip_interface('10.0.0.2/24'))]),
    }
    out = tmp_path / 'g.svg'
    visualize(nodes, str(out))
    assert out.exists() and out.stat().st_size > 0
