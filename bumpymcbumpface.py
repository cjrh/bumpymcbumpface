#!/usr/bin/env python3
# Copyright (C) 2019  Caleb Hattingh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
bumpymcbumpface - version-bump, tag, push, deploy
"""

import os
import sys
import shlex
import argparse
import subprocess as sp

folder = os.getcwd()


def main():
    class MyHelpFormatter(
            argparse.RawDescriptionHelpFormatter,
            argparse.ArgumentDefaultsHelpFormatter):
        pass
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=MyHelpFormatter,
    )
    parser.add_argument("--debug", action="store_true", help="Print debugging messages")
    parser.add_argument("--show", action="store_true", help="Show the current version and exit")
    parser.add_argument("--dry-run", action="store_true", help="Describe what would be done, and exit")
    parser.add_argument("--push-git", action="store_true", help="Push the new commit and tag to github")
    parser.add_argument("--push-pypi", action="store_true", help="Push the new built packages to PyPI")
    parser.add_argument(
        "field",
        choices=["major", "minor", "patch"],
        default="patch",
        const="patch",
        nargs="?",
    )
    args = parser.parse_args()

    args.debug and print(args)
    args.dry_run and print("Dry run active!")

    version_filename = os.path.join(folder, "VERSION")
    version = open(version_filename, encoding="utf-8").readline().strip()

    if args.show or args.debug:
        print(version)
        return

    major, minor, patch = version.split(".")[:3]
    if "major" in args.field:
        major, minor, patch = int(major) + 1, 0, 0
    if "minor" in args.field:
        minor, patch = int(minor) + 1, 0
    if "patch" in args.field or not args.field:
        patch = int(patch) + 1
    new_version = "{major}.{minor}.{patch}".format(
        major=major, minor=minor, patch=patch)

    git_status_output = sp.check_output("git status".split())
    if args.debug:
        print(git_status_output)

    if b"Changes not staged for commit:" in git_status_output:
        print("Repo has uncommitted changes. Stopping for your own safety.")
        sys.exit(1)

    if b"Untracked files:" in git_status_output:
        print("Repo has untracked files. Stopping for your own safety.")
        sys.exit(1)

    if args.dry_run:
        print("The new version that would be written: {}".format(new_version))
        return

    with open(version_filename, "w", encoding="utf-8") as f:
        f.write(new_version)

    sp.check_call("git add {}".format(version_filename).split(), cwd=folder)
    sp.check_call(shlex.split("git commit -m 'Bump version to {}'".format(new_version)), cwd=folder)
    sp.check_call("git tag v{}".format(new_version).split(), cwd=folder)
    if args.push_git:
        sp.check_call("git push".split(), cwd=folder)
        sp.check_call("git push --tags".split(), cwd=folder)

    sp.run("{} setup.py bdist_wheel sdist".format(sys.executable).split(), cwd=folder)
    if args.push_pypi:
        sp.run("twine upload --skip-existing dist/*{}*".format(new_version), cwd=folder)


if __name__ == "__main__":
    main()
