#!/usr/bin/env python3

import argparse
import os
import sys
from collections import Counter


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    arg_logfile = p.add_argument(
        "--logfile",
        type=argparse.FileType(mode="r"),
        help="logfile to parse; default is /var/log/pihole.log or stdin (piped)",
    )
    if sys.stdin.isatty():
        if os.path.isfile("/var/log/pihole.log"):
            arg_logfile.default = open("/var/log/pihole.log", "r")
        else:
            arg_logfile.required = True
    else:
        arg_logfile.default = sys.stdin

    group_arg_count = p.add_argument_group(title="limit results by counts")
    arg_count = group_arg_count.add_mutually_exclusive_group()
    arg_count.add_argument(
        "-t",
        "--top",
        help="show top N results (default is to show all)",
        metavar="N",
        type=int,
        required=False,
    )
    arg_count.add_argument(
        "--having-ge",
        help="show all results having greater than or equal to N",
        metavar="N",
        type=int,
        required=False,
    )
    arg_count.add_argument(
        "--having-le",
        help="show all results having less than or equal to N",
        metavar="N",
        type=int,
        required=False,
    )

    group_arg_show = p.add_argument_group(title="limit results by pihole action")
    arg_show = group_arg_show.add_mutually_exclusive_group()
    arg_show.add_argument(
        "-b",
        "--blocked",
        action="store_const",
        dest="show",
        const="blocked",
        help="show blocked results",
    )
    arg_show.add_argument(
        "-f",
        "--forwarded",
        action="store_const",
        dest="show",
        const="forwarded",
        help="show forwarded results",
    )
    arg_show.set_defaults(show="blocked")
    args = p.parse_args()
    return args


def parse_pihole_log(logfile_fh, show: str) -> Counter:
    find_str = ""
    if show == "blocked":
        find_str = " is 0.0.0.0"
    elif show == "forwarded":
        find_str = "forwarded"
    else:
        raise Exception("show must be either forwarded or blocked")
    count = Counter()
    for line in logfile_fh:
        if find_str in line:
            parts = line.split(" ")
            domain = parts[-3]
            if domain in ["is"]:
                print(f"find_str={find_str}, domain={domain}: {line.strip()}")
            count[domain] += 1
    return count


def filter_results(
    results: Counter, max_results: int, having_ge: int, having_le: int
) -> Counter:
    n_results = len(results)
    filtered_results = Counter()
    if having_ge:
        for domain, count in results.most_common(n_results):
            if count >= args.having_ge:
                filtered_results[domain] = count
    elif having_le:
        for domain, count in results.most_common(n_results):
            if count <= args.having_le:
                filtered_results[domain] = count
    else:
        for domain, count in results.most_common(max_results or n_results):
            filtered_results[domain] = count
    return filtered_results


def print_results(results: Counter):
    for domain, count in filtered_results.most_common(len(filtered_results)):
        print(f"{domain:48s} {count}")


if __name__ == "__main__":
    args = parse_args()
    comment = "# showing "
    if args.top:
        comment += f"top {args.top} {args.show} results"
    elif args.having_ge:
        comment += f"{args.show} results having {args.having_ge} or more hits"
    elif args.having_le:
        comment += f"{args.show} results having {args.having_le} or fewer hits"
    else:
        comment += f"showing all {args.show} results"
    print(comment + " from " + args.logfile.name)
    results = parse_pihole_log(args.logfile, args.show)
    filtered_results = filter_results(results, args.top, args.having_ge, args.having_le)
    print_results(filtered_results)
