#!/usr/bin/env python
from pathlib import Path

from sshgen.generators.model import MapToHost
from sshgen.generators.sshconfig import SSHConfig
from sshgen.models.host import HostModel
from sshgen.parsers.ansible import AnsibleHostsParser


class AppUtils:
    def __init__(self, hosts_file: Path, output_file: Path):
        self._hosts_file = hosts_file
        self._output_file = output_file
        self._parsed_hosts = AnsibleHostsParser(self._hosts_file).as_map()
        self._host_models: list[HostModel] = MapToHost().convert(self._parsed_hosts)

    def generate_ssh_config(self) -> None:
        SSHConfig(models=self._host_models, output_file=self._output_file).generate()
