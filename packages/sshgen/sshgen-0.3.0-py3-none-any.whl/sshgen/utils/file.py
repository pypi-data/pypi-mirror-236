#!/usr/bin/env python
import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)


class FileUtils:
    @staticmethod
    def as_file(file_path: str) -> Path:
        resolved_path = FileUtils._get_base_path() / Path(file_path)

        if FileUtils._is_yaml_file(resolved_path):
            if resolved_path.exists() and FileUtils._is_empty(resolved_path):
                log.error('Ansible hosts file %s is empty. Exiting...', resolved_path)
                sys.exit(1)
            elif not resolved_path.exists():
                log.error('Ansible hosts file does not exists at %s. Exiting...', resolved_path)
                sys.exit(1)

        FileUtils._create_file(resolved_path)

        return resolved_path

    @staticmethod
    def as_package_file(file_path: str) -> Path:
        return Path(__file__).resolve().parent.parent / Path(file_path)

    @staticmethod
    def _get_base_path() -> Path:
        return Path(__file__).cwd().resolve()

    @staticmethod
    def _is_yaml_file(file_path: Path) -> bool:
        return file_path.suffix in {'.yml', '.yaml'}

    @staticmethod
    def _is_empty(file_path: Path) -> bool:
        return file_path.is_file() and file_path.stat().st_size == 0

    @staticmethod
    def _create_file(file_path: Path) -> None:
        if not file_path.is_file():
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch(exist_ok=True)
            except OSError as e:
                log.exception('Failed to create file or directory: %s, reason: %s', file_path, e.strerror)
                sys.exit(1)
