#!/usr/bin/env python
import logging
from pathlib import Path

from ruamel.yaml import YAML, CommentedMap

from sshgen.utils.file import FileUtils

log = logging.getLogger(__name__)


class AnsibleHostsParser:
    def __init__(self, hosts_file_path: Path | None = None):
        self._yaml = YAML()
        self._default_hosts_file = 'examples/hosts.yml'
        self._file_path: Path = hosts_file_path or FileUtils.as_file(self._default_hosts_file)

    def as_map(self) -> CommentedMap:
        log.debug('Loading ansible hosts file: %s', self._file_path)
        return self._yaml.load(self._file_path)
