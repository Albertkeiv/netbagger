import argparse
from .topology import load_topology
from .simulator import simulate, Result


def main():
    parser = argparse.ArgumentParser(description="Netbagger simulator")
    sub = parser.add_subparsers(dest="cmd")

    sim = sub.add_parser("simulate", help="simulate packet")
    sim.add_argument("topology", help="topology YAML file")
    sim.add_argument("src", help="source IP")
    sim.add_argument("dst", help="destination IP")
    sim.add_argument("--ecmp", action="store_true", help="show all ECMP branches")

    vis = sub.add_parser("visualize", help="render topology to SVG")
    vis.add_argument("topology", help="topology YAML file or directory")
    vis.add_argument("--output", "-o", default="topology.svg", help="output SVG file")

    args = parser.parse_args()

    if args.cmd == "simulate":
        nodes = load_topology(args.topology)
        res, steps = simulate(nodes, args.src, args.dst, args.ecmp)
        for s in steps:
            print(s)
        print(res)
    elif args.cmd == "visualize":
        nodes = load_topology(args.topology)
        from .visualize import visualize
        path = visualize(nodes, args.output)
        print(path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
