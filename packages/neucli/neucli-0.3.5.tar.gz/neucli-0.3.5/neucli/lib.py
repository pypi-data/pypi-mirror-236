#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pathlib
import shlex
import shutil
import subprocess
import sys

DOCS_PATH = os.path.join(os.environ['NEULABS_LIB_PATH'], 'modules', 'docs')
RUNNERS_PATH = os.path.join(
    os.environ['NEULABS_LIB_PATH'], 'modules', 'runners')
ACTIONS_PATH = os.path.join(
    os.environ['NEULABS_LIB_PATH'], 'modules', 'actions')


def argsinstance():
    def _cmd_docs(parser):
        subparsers = parser.add_parser(
            'docs', help='Create docs template')

        subparsers.add_argument('-n', '--repository-name',
                                required=True, help='Name of the repository')

    def _cmd_runners(parser):
        parser.add_parser(
            'runners', help='Create runners template')

    def _cmd_actions(parser):
        release_please = parser.add_parser(
            'actions:release_please', help='Create release please workflow')

        choices_type = ['terraform-module'
                        'dart',
                        'elixir',
                        'go',
                        'helm',
                        'java',
                        'krm',
                        'maven',
                        'node',
                        'expo',
                        'ocaml',
                        'php',
                        'python',
                        'ruby',
                        'rust',
                        'sfdx',
                        'simple',
                        ]
        release_please.add_argument('--repository-type', type=str, choices=choices_type, required=True, help='Repository type')

        boring_cyborg = parser.add_parser(
            'actions:boring_cyborg', help='Create boring_cyborg files')
        boring_cyborg.add_argument('--types', type=list, default=[], help='Conventional commit types')
        boring_cyborg.add_argument('--scopes', type=list, default=[], help='Conventional commit scopes')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Help for command', dest='command')

    parser.add_argument('--branch', default='main', help='Branch name')
    parser.add_argument('-d', '--dest-path', default='',
                        help='Destination path')

    _cmd_docs(subparsers)
    _cmd_runners(subparsers)
    _cmd_actions(subparsers)

    return parser


def pull_lib(branch_name: str):
    pwd = os.getcwd()
    os.chdir(os.environ['NEULABS_LIB_PATH'])
    subprocess.call(shlex.split(f'git checkout {branch_name}'))
    subprocess.call(shlex.split(f'git pull'))
    os.chdir(pwd)


def copy_files(source_dirpath, dest_dirpath):
    if not os.path.isdir(dest_dirpath):
        os.makedirs(dest_dirpath)

    for file_name in os.listdir(source_dirpath):
        source = pathlib.Path(source_dirpath, file_name)
        destination = pathlib.Path(dest_dirpath, file_name)
        shutil.copy(source, destination)
        print(f'Copied {file_name} in {destination}')


def subsitute_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(old_string, new_string)

    with open(file_path, 'w') as file:
        file.write(filedata)


def lib_docs(base_dest_path: str, repository_name: str):
    docs_source_path = os.path.join(DOCS_PATH, 'files')
    docs_dest_path = os.path.join(base_dest_path, 'docs')
    print(
        f'Copying docs files from {docs_source_path} to {docs_dest_path}')
    shutil.copytree(docs_source_path, docs_dest_path, dirs_exist_ok=True)

    scripts_source_path = os.path.join(DOCS_PATH, 'scripts')
    scripts_dest_path = os.path.join(base_dest_path, '.github', 'scripts')
    print(
        f'Copying scripts files from {scripts_source_path} to {scripts_dest_path}')
    copy_files(scripts_source_path, scripts_dest_path)

    workflows_source_path = os.path.join(DOCS_PATH, 'workflows')
    workflows_dest_path = os.path.join(
        base_dest_path, '.github', 'workflows')
    print(
        f'Copying workflows files from {workflows_source_path} to {workflows_dest_path}')
    copy_files(workflows_source_path, workflows_dest_path)

    files = ['docs/docusaurus.config.js',
             '.github/workflows/deploy-docs.yml']
    for file in files:
        subsitute_in_file(os.path.join(base_dest_path, file),
                          '%NAME%', repository_name)


def lib_runners(base_dest_path: str):
    scripts_source_path = os.path.join(RUNNERS_PATH, 'scripts')
    scripts_dest_path = os.path.join(base_dest_path, '.github', 'scripts')
    print(
        f'Copying scripts files from {scripts_source_path} to {scripts_dest_path}')
    copy_files(scripts_source_path, scripts_dest_path)


def lib_actions_release_please(base_dest_path: str, repository_type: str):
    files_source_path = os.path.join(ACTIONS_PATH, 'release-please', 'files')
    files_dest_path = os.path.join(base_dest_path)
    print(
        f'Copying files from {files_source_path} to {files_dest_path}')
    shutil.copytree(files_source_path, files_dest_path, dirs_exist_ok=True)

    workflows_source_path = os.path.join(ACTIONS_PATH, 'release-please', 'workflows')
    workflows_dest_path = os.path.join(base_dest_path, '.github', 'workflows')
    print(
        f'Copying workflows files from {workflows_source_path} to {workflows_dest_path}')
    shutil.copytree(workflows_source_path,
                    workflows_dest_path, dirs_exist_ok=True)

    files = ['release-please-config.json']
    for file in files:
        subsitute_in_file(os.path.join(base_dest_path, file),
                          '%RELEASE_TYPE%', repository_type)


def lib_actions_boring_cyborg(base_dest_path: str, types: list, scopes: list):
    default_types = [
        'feat',
        'feat!',
        'fix',
        'fix!',
        'docs',
        'refactor',
        'refactor!',
        'test',
        'chore',
        'build',
        'ci',
        *types
    ]
    default_scopes = [
        'master',
        'main',
        'production',
        'release-please',
        'ci',
        'docs',
        *scopes
    ]

    workflows_source_path = os.path.join(ACTIONS_PATH, 'boring-cyborg')
    workflows_dest_path = os.path.join(base_dest_path, '.github')

    print(
        f'Copying workflows files from {workflows_source_path} to {workflows_dest_path}')
    shutil.copytree(workflows_source_path,
                    workflows_dest_path, dirs_exist_ok=True)

    subsitute_in_file(os.path.join(workflows_dest_path, 'boring-cyborg.yml'), '%TYPES%', '|'.join(default_types))
    subsitute_in_file(os.path.join(workflows_dest_path, 'boring-cyborg.yml'), '%SCOPES%', '|'.join(default_scopes))

    subsitute_in_file(os.path.join(workflows_dest_path, 'semantic.yml'), '%TYPES%', '  - ' + '\n  - '.join(default_types))
    subsitute_in_file(os.path.join(workflows_dest_path, 'semantic.yml'), '%SCOPES%', '  - ' + '\n  - '.join(default_scopes))


def main():
    try:
        args = argsinstance().parse_args()
        pull_lib(args.branch)

        base_dest_path = os.path.join(
            os.environ['NEULABS_EXECUTION_CLI_PATH'], args.dest_path)
        if args.command == 'docs':
            return lib_docs(base_dest_path, args.repository_name)

        if args.command == 'runners':
            return lib_runners(base_dest_path)

        if args.command == 'actions:release_please':
            return lib_actions_release_please(base_dest_path, args.repository_type)

        if args.command == 'actions:boring_cyborg':
            return lib_actions_boring_cyborg(base_dest_path, args.types, args.scopes)

    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
