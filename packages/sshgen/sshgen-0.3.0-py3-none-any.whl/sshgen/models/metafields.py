#!/usr/bin/env python
from dataclasses import dataclass


@dataclass
class MetaFieldsModel:
    auth_type: str | None = None
    auth_path: str | None = None
    aliases: list[str] | None = None
    skip: bool | None = None
