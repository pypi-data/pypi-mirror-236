import abc
import collections
import pathlib
import re
import shutil
import uuid
from typing import Optional, TypeVar

import joblib

from gevulot import model

from . import config

UnitType = TypeVar("UnitType", bound="model.Unit")


class MetadataRepository(abc.ABC):
    @staticmethod
    def new_instance(name: Optional[str] = None) -> "MetadataRepository":

        if name is None:
            metadata_config = config.MetadataConfig.new_instance()
            name = metadata_config.default_metadata_repository
        
        if name == InProcMetadataRepository.name:
            return InProcMetadataRepository.new_instance()
        elif name == LocalMetadataRepository.name:
            return LocalMetadataRepository.new_instance()

    @abc.abstractmethod
    def set(self, unit: model.Unit) -> model.Unit:
        pass

    @abc.abstractmethod
    def get(
        self,
        id: uuid.UUID,
        unit_type: Optional[type[UnitType]] = None,
    ) -> UnitType:    
        pass

    def find(
        self,
        unit_type: type[UnitType],
        *args,
        limit: Optional[int] = None,
        **predicates,
    ) -> list[UnitType]:
        pass

    def delete(self, unit: model.Unit):
        pass

    def clean(self):
        pass


class InProcMetadataRepository(MetadataRepository):
    name = "in-proc"

    @staticmethod
    def new_instance() -> "MetadataRepository":
        return InProcMetadataRepository()
    
    def __init__(self) -> None:
        self._storage: dict[type[UnitType], dict[uuid.UUID, model.Unit]] = collections.defaultdict(dict)

    def set(self, unit: model.Unit) -> model.Unit:
        if not isinstance(unit, model.Unit):
            raise ValueError(
                f"Only instances of Unit type can be saved to repository. Was {type(unit)}."
            )
        
        storage = self._storage[type(unit)]

        storage[unit.id] = unit

        if not isinstance(unit, model.Metadata):
            metadata = model.Metadata.from_unit(unit)
            self.set(metadata)

        return unit

    def get(
        self,
        id: uuid.UUID,
        unit_type: Optional[type[UnitType]] = None,
    ) -> UnitType:
        if unit_type is None:
            metadata = self.get(id, model.Metadata)
            unit_type = metadata.to_unit_type()

        if not issubclass(unit_type, model.Unit):
            raise ValueError(f"Only instances of Unit type are supported by repository")

        storage = self._storage[unit_type]
        
        unit = storage.get(id)

        if unit is None:
            raise ValueError(f"No unit of type {unit_type} with id {id} found in repository")
        
        return unit

    def find(
        self,
        unit_type: type[UnitType],
        *args,
        limit: Optional[int] = None,
        **predicates,
    ) -> list[UnitType]:
        if not issubclass(unit_type, model.Unit):
            raise ValueError(f"Only Unit types are allowed. Was {type(unit_type)}.")

        storage = self._storage[unit_type]

        results = []

        for obj in storage.values():
            obj_matches_predicates = True

            if any(predicates):
                for attribute_name, predicate_value in predicates.items():
                    if not hasattr(obj, attribute_name):
                        raise ValueError(f"{unit_type} instance has no {attribute_name} attribute")

                    attribute_value = obj.__getattribute__(attribute_name)

                    if isinstance(predicate_value, re.Pattern):
                        if not predicate_value.match(attribute_value):
                            obj_matches_predicates = False
                            break
                    elif attribute_value != predicate_value:
                        obj_matches_predicates = False
                        break

            if obj_matches_predicates:
                results.append(obj)

            if limit is not None and len(results) == limit:
                break

        return results

    def delete(self, unit: model.Unit):
        storage = self._storage[type(unit)]
        
        storage.pop(unit.id)

        if not isinstance(unit, model.Metadata):
            metadata = self.get(unit.id, unit_type=model.Metadata)
            self.delete(metadata)

    def clean(self):
        self._storage = collections.defaultdict(dict)


class LocalMetadataRepository(MetadataRepository):
    name = "local"

    @staticmethod
    def new_instance(data_dir: Optional[pathlib.Path] = None) -> "MetadataRepository":
        if data_dir is None:
            metadata_config = config.MetadataConfig.new_instance()
            data_dir = metadata_config.local_metadata_repository.data_dir
            data_dir = pathlib.Path(data_dir)

        return LocalMetadataRepository(
            data_dir=data_dir,
        )
    
    def __init__(self, data_dir: pathlib.Path) -> None:
        self._data_dir = data_dir

    def set(self, unit: model.Unit) -> model.Unit:
        if not isinstance(unit, model.Unit):
            raise ValueError(
                f"Only instances of Unit type can be saved to repository. Was {type(unit)}"
            )
        
        storage_path = self._data_dir / f"{unit.get_type_name()}.joblib"

        if storage_path.exists():
            storage = joblib.load(storage_path)
        else:
            storage = dict()

        storage[unit.id] = unit

        self._data_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(storage, storage_path)

        if not isinstance(unit, model.Metadata):
            metadata = model.Metadata.from_unit(unit)
            self.set(metadata)

        return unit

    def get(
        self,
        id: uuid.UUID,
        unit_type: Optional[type[UnitType]] = None,
    ) -> UnitType:
        if unit_type is None:
            metadata = self.get(id, model.Metadata)
            unit_type = metadata.to_unit_type()

        if not issubclass(unit_type, model.Unit):
            raise ValueError(
                f"Only instances of Unit type are supported by repository. Was {unit_type}."
            )
        
        type_name = unit_type.get_type_name()

        storage_path = self._data_dir / f"{type_name}.joblib"

        if storage_path.exists():
            storage = joblib.load(storage_path)
        else:
            storage = dict()
        
        unit = storage.get(id)

        if unit is None:
            raise ValueError(f"No unit of type {unit_type} with id {id} found at {storage_path}")
        
        return unit

    def find(
        self,
        unit_type: type[UnitType],
        *args,
        limit: Optional[int] = None,
        **predicates,
    ) -> list[UnitType]:
        if not issubclass(unit_type, model.Unit):
            raise ValueError(f"Only Unit types are allowed. Was {unit_type}")
        
        type_name = unit_type.get_type_name()

        storage_path = self._data_dir / f"{type_name}.joblib"

        if not storage_path.exists():
            return []

        storage: dict = joblib.load(storage_path)

        results = []

        for obj in storage.values():
            obj_matches_predicates = True

            if any(predicates):
                for attribute_name, predicate_value in predicates.items():
                    if not hasattr(obj, attribute_name):
                        raise ValueError(f"{unit_type} instance has no {attribute_name} attribute")

                    attribute_value = obj.__getattribute__(attribute_name)

                    if isinstance(attribute_value, str) and isinstance(predicate_value, re.Pattern):
                        if not predicate_value.match(attribute_value):
                            obj_matches_predicates = False
                            break
                    elif attribute_value != predicate_value:
                        obj_matches_predicates = False
                        break

            if obj_matches_predicates:
                results.append(obj)

            if limit is not None and len(results) == limit:
                break

        return results

    def _load_storage(self, unit_type: type[UnitType]) -> dict[uuid.UUID, UnitType]:
        type_name = unit_type.get_type_name()
        
        storage_path = self._data_dir / f"{type_name}.joblib"

        if not storage_path.exists():
            return dict()
        
        storage = joblib.load(storage_path)

        return storage
    
    def _dump_storage(self, unit_type: type[UnitType], storage: dict[uuid.UUID, UnitType]):
        type_name = unit_type.get_type_name()

        storage_path = self._data_dir / f"{type_name}.joblib"

        joblib.dump(storage, storage_path)

    def delete(self, unit: model.Unit):
        unit_type = type(unit)
        
        storage = self._load_storage(unit_type)
        
        storage.pop(id)

        self._dump_storage(unit_type, storage)

        if not isinstance(unit, model.Metadata):
            metadata = self.get(id, unit_type=model.Metadata)
            self.delete(metadata)

    def clean(self):
        if self._data_dir.exists():
            shutil.rmtree(self._data_dir) 
