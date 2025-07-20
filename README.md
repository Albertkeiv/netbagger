# Netbagger

A simple network path simulator. Topology is described in YAML format and the
`simulate` command shows how a packet would travel from source to destination.

```
python -m netbagger.cli simulate topology.yaml 192.0.2.1 198.51.100.1
```

