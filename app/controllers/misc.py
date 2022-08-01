from pathlib import Path
from typing import TypeAlias

from .extractor import update_data_file, get_static_data

path: TypeAlias = str | Path


def set_java(java_path: path):
    data = get_static_data()
    data.java = java_path

    update_data_file(data)
