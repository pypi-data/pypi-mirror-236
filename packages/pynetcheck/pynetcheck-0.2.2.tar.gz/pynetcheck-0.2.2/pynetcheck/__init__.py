import argparse
import os
from pathlib import Path

import pytest

EXTRA = dict()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pytest-help", help="Print pytest help.", action="store_true")
    parser.add_argument(
        "--testpaths", help="Test path directory.", action="extend", nargs="+", type=str
    )
    parser.add_argument("--config-dir", help="Device Configuration directory.")
    parser.add_argument("args", nargs="*")
    parsed, extra = parser.parse_known_args()

    cwd = Path(os.getcwd())
    if parsed.testpaths:
        pytest_args = [(cwd / Path(p)).resolve() for p in parsed.testpaths]
    else:
        pytest_args = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
        ]

    if parsed.pytest_help:
        EXTRA["help"] = True
        pytest_args.append("--help")
        pytest.main(args=pytest_args)
        exit(0)

    if parsed.config_dir:
        cfg_dir = (cwd / Path(parsed.config_dir)).resolve()
        EXTRA["configs"] = [cfg_dir / f for f in os.listdir(cfg_dir)]

    pytest_args.extend(extra)
    pytest.main(args=pytest_args)


if __name__ == "__main__":
    main()
