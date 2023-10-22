import pathlib
from typing import Optional

from gevulot import model

from . import indexing, repository


class MetadataGraph:
    @staticmethod
    def new_instance() -> "MetadataGraph":
        taxonomy = indexing.Taxonomy.new_instance()
        metadata_repository = repository.MetadataRepository.new_instance()

        return MetadataGraph(taxonomy, metadata_repository)
    
    def __init__(
        self,
        taxonomy: indexing.Taxonomy,
        metadata_repository: repository.MetadataRepository,
    ):
        self._taxonomy = taxonomy
        self._metadata_repository = metadata_repository
    
    def exists(self, path: pathlib.PurePosixPath) -> bool:
        return self._taxonomy.exists(path)

    def touch(self, path: pathlib.PurePosixPath, capacity: Optional[int] = None) -> model.Stream:
        if self._taxonomy.exists(path):
            stream = self._taxonomy.resolve(path)
            return stream

        stream = model.Stream.new_instance(capacity)
        
        self._metadata_repository.set(stream)
        self._taxonomy.set(path, stream)

        return stream
    
    def find(self, prefix: pathlib.PurePosixPath) -> list[model.Stream]:
        return self._taxonomy.find(prefix)

    def get_commits(self, path: pathlib.PurePosixPath) -> list[model.Commit]:
        protocol, canonical_path, _ = self._taxonomy.as_canonical_path(path)

        assert protocol == "gevulot", "Invalid path {path}. Should point to gevulot FS. Points to {protocol} instead."

        streams: list[model.Stream] = self._metadata_repository.find(
            object_type=model.Stream,
            path=canonical_path,
        )

        if not any(streams):
            raise ValueError(f"No streams found at path {canonical_path}. Expected one.")
        
        if len(streams) > 1:
            raise ValueError(f"Multiple streams found at path {canonical_path}. Expected one.")
        
        [stream] = streams

        commits: list[model.Commit] = self._metadata_repository.find(
            unit_type=model.Commit,
            stream_id=stream.id,
        )

        return commits
    
    def resolve(self, path: pathlib.PurePosixPath) -> Optional[model.Datum]:
        stream: model.Stream = self._taxonomy.resolve(path)

        commit_id = stream.head_commit_id

        if commit_id is None:
            return None

        commits: list[model.Commit] = self._metadata_repository.find(
            unit_type=model.Commit,
            id=commit_id,
        )

        [commit] = commits

        metadatas: list[model.Metadata] = self._metadata_repository.find(
            unit_type=model.Metadata,
            id=commit.datum_id,
        )

        [metadata] = metadatas

        datum = model.Datum.from_metadata(metadata)

        return datum

    def commit(self, datum: model.Datum, path: pathlib.PurePosixPath) -> model.Commit:
        assert isinstance(datum, model.Datum), f"Only Datum objects can be commited. Got {type(datum)}"

        metadata = datum.to_metadata()

        self._metadata_repository.put(metadata)

        stream = self.touch(path)

        existing_head_commit: Optional[model.Commit] = None

        if stream.head_commit_id is not None:
            commits: list[model.Commit] = self._metadata_repository.find(
                object_type=model.Commit,
                id=stream.head_commit_id,
            )

            [existing_head_commit] = commits

        new_head_commit = model.Commit.new_instance(
            stream_id=stream.id,
            datum_id=datum.id,
            previous_commit_id=existing_head_commit.id
            if existing_head_commit is not None
            else None,
        )

        self._metadata_repository.put(new_head_commit)

        if existing_head_commit is not None:
            existing_head_commit = existing_head_commit.model_copy(
                update={"next_commit_id": new_head_commit}
            )

            self._metadata_repository.update(existing_head_commit)

        stream = stream.model_copy(update={"head_commit_id": new_head_commit.id})

        self._metadata_repository.update(stream)

        return new_head_commit
    
    def update(self, datum: model.Datum) -> model.Datum:
        return self._metadata_repository.update(datum)

    def clean(self):
        self._metadata_repository.clean()

    def upstream(self, path: pathlib.PurePosixPath) -> list[model.Datum]:
        datum = self.resolve(path)

        if isinstance(datum, model.Blob):
            blob: model.Blob = datum

            messages: list[model.Message] = self._metadata_repository.find(
                object_type=model.Message,
                blob_id=blob.id,
                direction=model.MessageDirection.Egress,
            )

            upstream_runs = []
            for message in messages:
                [metadata, *_] = self._metadata_repository.find(
                    object_type=model.Metadata,
                    id=message.run_id,
                )
                run = model.Run.from_metadata(metadata)

                upstream_runs.append(run)
            
            return upstream_runs
        elif isinstance(datum, model.Run):
            run: model.Run = datum
            
            messages: list[model.Message] = self._metadata_repository.find(
                object_type=model.Message,
                run_id=run.id,
                direction=model.MessageDirection.Ingress,
            )

            upstream_blobs = []
            for message in messages:
                [metadata, *_] = self._metadata_repository.find(
                    object_type=model.Metadata,
                    id=message.blob_id,
                )
                blob = model.Blob.from_metadata(metadata)

                upstream_blobs.append(blob)
            
            return upstream_blobs
        else:
            raise ValueError(f"Unknown datum type {datum.unit_name} at {path}. Exptected Blob or Run.")
        
    def receive(self, subject_run: model.Run, blob: model.Blob) -> model.Message:
        ingress_message = model.Message.ingress(
            run_id=subject_run.id,
            blob_id=blob.id,
        )
        
        self._metadata_repository.put(ingress_message)

        return ingress_message
    
    def send(self, subject_run: model.Run, blob: model.Blob) -> model.Message:
        egress_message = model.Message.egress(
            run_id=subject_run.id,
            blob_id=blob.id,
        )
        
        self._metadata_repository.put(egress_message)

        return egress_message
    
    def downstream(self, path: pathlib.PurePosixPath) -> list[model.Metadata]:
        datum = self.resolve(path)

        if isinstance(datum, model.Blob):
            blob: model.Blob = datum

            messages: list[model.Message] = self._metadata_repository.find(
                object_type=model.Message,
                blob_id=blob.id,
                direction=model.MessageDirection.Ingress,
            )

            upstream_runs = []
            for message in messages:
                [metadata, *_] = self._metadata_repository.find(
                    object_type=model.Metadata,
                    id=message.run_id,
                )
                run = model.Run.from_metadata(metadata)

                upstream_runs.append(run)
            
            return upstream_runs
        elif isinstance(datum, model.Run):
            run: model.Run = datum
            
            messages: list[model.Message] = self._metadata_repository.find(
                object_type=model.Message,
                run_id=run.id,
                direction=model.MessageDirection.Egress,
            )

            upstream_blobs = []
            for message in messages:
                [metadata, *_] = self._metadata_repository.find(
                    object_type=model.Metadata,
                    id=message.blob_id,
                )
                blob = model.Blob.from_metadata(metadata)

                upstream_blobs.append(blob)
            
            return upstream_blobs
        else:
            raise ValueError(f"Unknown datum type {datum.unit_name} at {path}. Exptected Blob or Run.")
