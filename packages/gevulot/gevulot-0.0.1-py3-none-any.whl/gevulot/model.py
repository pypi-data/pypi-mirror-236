import dataclasses
import datetime
import enum
import importlib
import pathlib
import uuid
from typing import Optional


@dataclasses.dataclass
class Unit:
    id: uuid.UUID

    @classmethod
    def get_module_name(cls) -> str:
        return cls.__module__
    
    @classmethod
    def get_type_name(cls) -> str:
        return cls.__name__
    

@dataclasses.dataclass
class Metadata(Unit):
    id: uuid.UUID
    module_name: str
    type_name: str

    @staticmethod
    def from_unit(unit: Unit) -> "Metadata":
        return Metadata(
            id=unit.id,
            module_name=unit.get_module_name(),
            type_name=unit.get_type_name(),
        )

    def to_unit_type(self) -> type[Unit]:
        module = importlib.import_module(self.module_name)
        unit_type = getattr(module, self.type_name)

        return unit_type


@dataclasses.dataclass
class Node(Unit):
    unit_id: uuid.UUID
    path: pathlib.PurePosixPath

    @staticmethod
    def new_instance(unit_id: uuid.UUID, path: pathlib.PurePosixPath) -> "Node":
        return Node(
            id=unit_id,
            unit_id=unit_id,
            path=path,
        )


@dataclasses.dataclass
class Stream(Unit):
    capacity: Optional[int]
    head_commit_id: Optional[uuid.UUID]

    @staticmethod
    def new_instance(capacity: Optional[int]) -> "Stream":
        return Stream(
            id=uuid.uuid4(),
            capacity=capacity,
            head_commit_id=None
        )


@dataclasses.dataclass
class Commit(Unit):
    stream_id: uuid.UUID
    datum_id: uuid.UUID
    previous_commit_id: Optional[uuid.UUID]
    next_commit_id: Optional[uuid.UUID]
    created_at: datetime.datetime

    @staticmethod
    def new_instance(
        stream_id: uuid.UUID,
        datum_id: uuid.UUID,
        previous_commit_id: Optional[uuid.UUID]
    ) -> "Commit":
        return Commit(
            id=uuid.uuid4(),
            stream_id=stream_id,
            datum_id=datum_id,
            previous_commit_id=previous_commit_id,
            next_commit_id=None,
            created_at=datetime.datetime.utcnow()
        )


@dataclasses.dataclass
class Datum(Unit):
    pass


@dataclasses.dataclass
class Blob(Datum):
    size: int

    @staticmethod
    def new_instance(size: int) -> "Blob":
        return Blob(
            id=uuid.uuid4(),
            size=size,
        )
    

class MessageDirection(enum.Enum):
    Ingress = 0
    Egress = 1


class RunStatus(enum.Enum):
    Running = 0
    Finished = 1
    Failed = 2


@dataclasses.dataclass
class Run(Datum):
    status: RunStatus
    error: Optional[str]

    @staticmethod
    def new_instance(
        status: RunStatus = RunStatus.Running,
        error: Optional[str] = None,
    ) -> "Run":
        return Run(
            id=uuid.uuid4(),
            status=status,
            error=error,
        )


@dataclasses.dataclass
class Message(Unit):
    run_id: uuid.UUID
    blob_id: uuid.UUID
    direction: MessageDirection

    @staticmethod
    def new_instance(
        run_id: uuid.UUID, 
        blob_id: uuid.UUID,
        direction: MessageDirection,
    ) -> "Message":
        return Message(
            id=uuid.uuid4(),
            run_id=run_id,
            blob_id=blob_id,
            direction=direction,
        )
    
    @staticmethod
    def ingress(run_id: uuid.UUID, blob_id: uuid.UUID) -> "Message":
        return Message.new_instance(run_id, blob_id, MessageDirection.Ingress)

    @staticmethod
    def egress(run_id: uuid.UUID, blob_id: uuid.UUID) -> "Message":
        return Message.new_instance(run_id, blob_id, MessageDirection.Egress)