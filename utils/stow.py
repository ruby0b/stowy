import argparse
from pathlib import Path
from typing import Tuple, List, Union, Optional


def generate_stow_cmd(args: argparse.Namespace)\
        -> Union[Tuple[List[str], Optional[List[str]]], Tuple[None, List[str]]]:
    """
    Propagate CLI arguments to Stow and return a formatted command
    for unstowing and one for stowing
    """
    stow_cmd = ('stow'
                + (' -p' if args.compat else '')
                + (' -n' if args.simulate else '')
                + (' -v' * args.verbosity)
                + (' --no-folding' if args.no_folding else '')
                + (' --adopt' if args.adopt else '')
                + ''.join(f' --ignore {regex}' for regex in args.ignores)
                + ''.join(f' --defer {regex}' for regex in args.defers)
                + ''.join(f' --override {regex}' for regex in args.overrides)
                + f' -d {args.stow_dir}'
                ).split()
    # Only return a command for unstowing
    if args.delete:
        return stow_cmd + ['-D'], None
    # Restowing is implemented as subsequently unstowing and restowing
    # to ensure that all hooks are triggered
    if args.restow:
        return stow_cmd + ['-D'], stow_cmd
    # Only return a command for stowing
    return None, stow_cmd


def ensure_package_validity(p: Path, stow_dir: Path):
    """Assert that p is an immediate relative subdirectory of stow_dir."""
    if not (stow_dir / p).exists() or (stow_dir / p).is_file():
        raise ValueError(f'The stow directory does not contain package {p}')
    elif '/' in p.as_posix():
        raise ValueError(f'Slashes are not permitted in package names')
