from ipaddress import ip_interface, ip_network
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from netbagger.model import Node, Interface, Route
from netbagger.simulator import simulate, Result


def test_simulate_interfaces():
    r1 = Node('R1', [Interface('net1', ip_interface('192.0.2.1/24'))], [Route(ip_network('198.51.100.0/24'), '192.0.2.2')])
    r2 = Node('R2', [Interface('net1', ip_interface('192.0.2.2/24')), Interface('net2', ip_interface('198.51.100.1/24'))])

    result, steps = simulate({'R1': r1, 'R2': r2}, '192.0.2.1', '198.51.100.1')

    assert result == Result.DELIVERED
    assert str(steps[0]) == 'R1: via 192.0.2.2 out net1 -> R2 in net1'
    assert str(steps[1]) == 'R2: deliver to 198.51.100.1 on net2'
