#!/usr/bin/env python
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List

from utils import system, cli, stow, log


def main():
    args = cli.parse_cli_args()
    log.setup_logging(args.verbosity)
    log.DEBUG(f'Received args: {args}')
    unstow_cmd, stow_cmd = stow.generate_stow_cmd(args)

    all_packages = [Package.from_dir(p, args.stow_dir) for p in args.packages]
    # Group packages by target
    packages_by_target = defaultdict(list)
    for p in all_packages:
        packages_by_target[p.target].append(p)

    # UNSTOW
    if unstow_cmd:
        log.LOG_LINKS('Planning unstow')
        log.LOG_CD_OR_PLAN('Executing pre-unstow hooks')
        for p in all_packages:
            p.exec_pre_unstow()
        for target, packages in packages_by_target.items():
            log.LOG_CD_OR_PLAN(f'Unstowing packages with target {target}')
            system.run(unstow_cmd + ['-t', target]
                       + [p.path.as_posix() for p in packages])
        log.LOG_CD_OR_PLAN('Executing post-unstow hooks')
        for p in all_packages:
            p.exec_post_unstow()

    # STOW
    if stow_cmd:
        log.LOG_LINKS('Planning stow')
        log.LOG_CD_OR_PLAN('Executing pre-stow hooks')
        for p in all_packages:
            p.exec_pre_stow()
        for target, packages in packages_by_target.items():
            log.LOG_CD_OR_PLAN(f'Stowing packages with target {target}')
            system.run(stow_cmd + ['-t', target]
                       + [p.path.as_posix() for p in packages])
        log.LOG_CD_OR_PLAN('Executing post-stow hooks')
        for p in all_packages:
            p.exec_post_stow()


@dataclass
class Package:
    stow_dir: Path
    path: Path
    target: Path
    owner: str
    pre_stow: List[str]
    post_stow: List[str]
    pre_unstow: List[str]
    post_unstow: List[str]

    @classmethod
    def from_dir(cls, package_path: Path, stow_dir: Path):
        """Creates a Package object from a package directory and its configuration file"""
        stow.ensure_package_validity(package_path, stow_dir)

        # Load YAML into dictionary
        config_path = next((stow_dir / package_path).glob('package.yaml'), None)
        config = system.load_yaml(config_path) if config_path else {}
        if not isinstance(config, dict):
            raise ValueError('The configuration files have to be mappings')

        # Use configured or default values
        return cls(
            stow_dir=stow_dir,
            path=package_path,
            target=Path(system.expand(config.get('Target', '~'))),
            owner=system.expand(config.get('Owner', os.environ['USER'])),
            pre_stow=config.get('PreStow', []),
            post_stow=config.get('PostStow', []),
            pre_unstow=config.get('PreUnstow', []),
            post_unstow=config.get('PostUnstow', []),
        )

    def exec_pre_stow(self):
        # Recursively change the ownership of the package's files
        # to match the configured owner
        try:
            system.recursive_chown(self.stow_dir / self.path,
                                   *system.user_id_and_group_id(self.owner))
        except PermissionError:
            log.EXCEPTION('Please rerun with sudo permissions')
            exit(1)
        system.run_in_own_shells(*self.pre_stow)

    def exec_post_stow(self):
        system.run_in_own_shells(*self.post_stow)

    def exec_pre_unstow(self):
        system.run_in_own_shells(*self.pre_unstow)

    def exec_post_unstow(self):
        system.run_in_own_shells(*self.post_unstow)


if __name__ == '__main__':
    main()
