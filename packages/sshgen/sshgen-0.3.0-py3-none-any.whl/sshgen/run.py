#!/usr/bin/env python
from sshgen.utils.app import AppUtils
from sshgen.utils.file import FileUtils


def run() -> None:
    hosts_file = FileUtils.as_file(file_path='../examples/hosts.yml')
    output_file = FileUtils.as_file(file_path='../config')

    AppUtils(hosts_file, output_file).generate_ssh_config()


if __name__ == '__main__':
    run()
