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

    args = parser.parse_args()

    if args.cmd == "simulate":
        nodes = load_topology(args.topology)
        res, steps = simulate(nodes, args.src, args.dst, args.ecmp)
        for s in steps:
            print(s)
        print(res)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
