import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from netbagger.topology import load_topology


def test_load_single_file(tmp_path):
    cfg = tmp_path / "single.yaml"
    cfg.write_text(
        """
        nodes:
          R1:
            interfaces:
              - name: net1
                network: 10.0.0.1/24
        """
    )
    nodes = load_topology(str(cfg))
    assert set(nodes) == {"R1"}
    assert str(nodes["R1"].interfaces[0].network) == "10.0.0.0/24"


def test_load_directory(tmp_path):
    d = tmp_path
    (d / "a.yaml").write_text(
        """
        nodes:
          A:
            interfaces:
              - name: net1
                network: 10.0.0.1/24
        """
    )
    (d / "b.yaml").write_text(
        """
        nodes:
          B:
            interfaces:
              - name: net2
                network: 10.0.1.1/24
        """
    )
    nodes = load_topology(str(d))
    assert set(nodes) == {"A", "B"}


def test_load_with_pyyaml(monkeypatch, tmp_path):
    cfg = tmp_path / "conf.yaml"
    cfg.write_text("nodes: {}\n")

    captured = {}

    def fake_safe_load(obj):
        captured['type'] = type(obj)
        return {'nodes': {'X': {}}}

    import types, importlib
    import sys

    dummy_yaml = types.SimpleNamespace(safe_load=fake_safe_load)
    monkeypatch.setitem(sys.modules, 'yaml', dummy_yaml)

    from netbagger import topology as t
    importlib.reload(t)

    nodes = t.load_topology(str(cfg))

    assert captured['type'] is not str
    assert set(nodes) == {'X'}


def test_gateway_must_be_reachable(tmp_path):
    import importlib
    from netbagger import topology

    importlib.reload(topology)

    cfg = tmp_path / "topo.yaml"
    cfg.write_text(
        """
        nodes:
          R1:
            interfaces:
              - name: net1
                network: 10.0.0.1/24
            routes:
              - prefix: 0.0.0.0/0
                via: 10.0.1.2
          R2:
            interfaces:
              - name: net2
                network: 10.0.1.2/24
        """
    )

    with pytest.raises(ValueError):
        topology.load_topology(str(cfg))


def test_gateway_on_same_network(tmp_path):
    import importlib
    from netbagger import topology

    importlib.reload(topology)

    cfg = tmp_path / "topo.yaml"
    cfg.write_text(
        """
        nodes:
          R1:
            interfaces:
              - name: net1
                network: 10.0.0.1/24
            routes:
              - prefix: 0.0.0.0/0
                via: 10.0.0.1
        """
    )

    nodes = topology.load_topology(str(cfg))
    assert set(nodes) == {"R1"}

