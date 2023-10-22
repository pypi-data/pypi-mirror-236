import fnmatch
import pathlib
import re
import uuid
from typing import Optional

from gevulot import model

from . import repository


class Taxonomy:
    @staticmethod
    def new_instance() -> "Taxonomy":
        metadata_repository = repository.MetadataRepository.new_instance()

        return Taxonomy(metadata_repository)
    
    def __init__(self, metadata_repository: repository.MetadataRepository):
        self._metadata_repository = metadata_repository
    
    def exists(self, pattern: str) -> bool:
        pattern_regex = fnmatch.translate(pattern)
        pattern_regex = re.compile(pattern_regex)

        nodes = self._metadata_repository.find(
            object_type=model.Node,
            path=pattern_regex,
        )

        return any(nodes)
    
    def set(self, path: pathlib.PurePosixPath, unit: model.Unit) -> model.Node:
        if self.exists(path):
            raise ValueError(f"Path {path} is already in use. Cannot index another object to it.")
        
        node = model.Node.new_instance(
            unit_id=unit.id,
            path=path,
        )

        self._metadata_repository.set(node)

        return node

    def find(self, pattern: str) -> list[model.Unit]:
        pattern_regex = fnmatch.translate(pattern)
        pattern_regex = re.compile(pattern_regex)

        nodes = self._metadata_repository.find(
            unit_type=model.Node,
            path=pattern_regex,
        )

        units = []
        for node in nodes:
            unit = self._metadata_repository.get(node.unit_id)
            units.append(unit)

        return nodes
    
    def delete(self, path: pathlib.PurePosixPath):
        nodes = self.find(path)

        self._metadata_repository.delete(nodes)
