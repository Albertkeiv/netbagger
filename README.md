# Netbagger

A simple network path simulator. Topology is described in YAML format and the
`simulate` command shows how a packet would travel from source to destination.

Topology may be provided as a single file or as a directory containing
multiple `*.yaml` files. When a directory is supplied, all YAML files in that
directory are merged.

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

