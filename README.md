# Netbagger

A simple network path simulator. Topology is described in YAML format and the
`simulate` command shows how a packet would travel from source to destination.
Each hop in the output also indicates the interface the packet left from and
the interface it arrived on.

Topology may be provided as a single file or as a directory containing
multiple `*.yaml` files. When a directory is supplied, all YAML files in that
directory are merged.

Multiple nodes may use addresses from the same network. Only partially
overlapping prefixes (for example `10.0.0.0/24` and `10.0.0.0/25`) are
disallowed and produce a `Network overlap` error during loading.

Valid example with two nodes on a shared subnet:

```yaml
nodes:
  R1:
    interfaces:
      - name: net1
        network: 10.0.0.1/24
  R2:
    interfaces:
      - name: net1
        network: 10.0.0.2/24
```

## Installation

Install dependencies from `requirements.txt`:

```
pip install -r requirements.txt
```

### Example with a single topology file

```
python -m netbagger.cli simulate example-topology/r1.yaml 192.0.2.1 198.51.100.1
```

### Example with a directory of topology files

```
python -m netbagger.cli simulate example-topology/ 192.0.2.1 198.51.100.1
```

