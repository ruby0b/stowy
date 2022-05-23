import argparse
import os
import sys
from pathlib import Path


def parse_cli_args():
    parser = argparse.ArgumentParser(description=f'StowY (Stow YAML extension)',
                                     formatter_class=NoUsageFormatter, add_help=False)
    parser.add_argument_group('SYNOPSIS', os.path.basename(sys.argv[0])
                              + ' [OPTIONS] [ACTION] PACKAGE ...')
    parser.add_argument('packages', metavar='PACKAGE', nargs='+', type=Path, help=argparse.SUPPRESS)

    # OPTIONS
    options = parser.add_argument_group('OPTIONS')
    options.add_argument('-d', '--dir', metavar='DIR', dest='stow_dir', type=Path,
                         default=Path(os.environ.get('STOW_DIR', os.getcwd())),
                         help='Set stow dir to DIR (default is $STOW_DIR, then current dir)')
    options.add_argument('--ignore', metavar='REGEX', dest='ignores',
                         action='append', type=str, default=[],
                         help="Ignore files ending in this Perl regex")
    options.add_argument('--defer', metavar='REGEX', dest='defers',
                         action='append', type=str, default=[],
                         help="Don't stow files beginning with this Perl regex "
                              "if the file is already stowed to another package")
    options.add_argument('--override', metavar='REGEX', dest='overrides',
                         action='append', type=str, default=[],
                         help="Force stowing files beginning with this Perl regex "
                              "if the file is already stowed to another package")
    options.add_argument('--no-folding', action='store_true',
                         help='Disable tree folding (only leaves will be symlinked)')
    options.add_argument('--adopt', action='store_true',
                         help="(Use with care!) Import existing files into stow "
                              "package from target.  Please read docs before using.")
    options.add_argument('-p', '--compat', action='store_true',
                         help='Use legacy algorithm for unstowing')
    options.add_argument('-n', '--no', '--simulate', dest='simulate', action='store_true',
                         help='Do not actually make any filesystem changes')
    options.add_argument('-v', '--verbose', action='count', default=0, dest='verbosity',
                         help='Increase verbosity by 1 (levels are from 0 to 5)')
    options.add_argument('-h', '--help', action='help', help='Show this help')

    # ACTIONS
    actions_group = parser.add_argument_group('ACTIONS')
    actions = actions_group.add_mutually_exclusive_group()
    actions.add_argument('-S', '--stow', action='store_true', help='Stow packages (default)')
    actions.add_argument('-D', '--delete', action='store_true', help='Unstow packages')
    actions.add_argument('-R', '--restow', action='store_true',
                         help='Restow packages (like stow -D followed by stow -S)')

    args = parser.parse_args()
    if not (args.delete or args.restow):
        args.stow = True
    return args


class NoUsageFormatter(argparse.HelpFormatter):
    def _format_usage(self, *_):
        return ''
