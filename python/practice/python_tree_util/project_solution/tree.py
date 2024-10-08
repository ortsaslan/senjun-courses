import argparse
from pathlib import Path

import utils


def level(raw_val):
    val = int(raw_val)
    if val < 1:
        raise argparse.ArgumentTypeError(
            f"{raw_val} is an invalid value for level. It must be greater than or equal to 1"
        )
    return val


def directory(raw_path):
    if Path(raw_path).is_dir():
        return raw_path
    raise argparse.ArgumentTypeError(
        f"{raw_path} is an invalid value for directory"
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?", type=directory, default=".")
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-L", type=level, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    utils.show_tree(dir=args.dir, dirs_only=args.d, level=args.L)
