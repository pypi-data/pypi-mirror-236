import functools
import inspect
import io
import pathlib
from typing import Optional

from gevulot import data, metadata, model


class Gevulot(object):
    @staticmethod
    def new_instance() -> "Gevulot":
        metadata_graph = metadata.MetadataGraph.new_instance()
        data_repository = data.DataRepository.new_instance()

        return Gevulot(metadata_graph, data_repository)
    
    def __init__(
        self,
        metadata_graph: metadata.MetadataGraph,
        data_repository: data.DataRepository,
    ) -> None:
        self._metadata_graph = metadata_graph
        self._data_repository = data_repository

        self._active_run_path: Optional[str] = None
        self._active_run: Optional[model.Run] = None

    def exists(self, path: pathlib.PurePosixPath) -> bool:
        return self._metadata_graph.exists(path)

    def touch(self, path: pathlib.PurePosixPath, capacity: Optional[int] = None) -> model.Stream:
        return self._metadata_graph.touch(path, capacity=capacity)

    def log(self, path: pathlib.PurePosixPath) -> list[model.Commit]:
        return self._metadata_graph.get_commits(path)

    def resolve(self, path: pathlib.PurePosixPath) -> Optional[model.Datum]:
        return self._metadata_graph.resolve(path)
    
    def find(self, prefix: pathlib.PurePosixPath) -> list[model.Stream]:
        return self._metadata_graph.find(prefix)

    def start(self, path: Optional[pathlib.PurePosixPath] = None) -> "Gevulot":
        if path is None:
            caller_frame = inspect.stack()[1]
            file_name = caller_frame.filename
            function = caller_frame.function
            path = f"{file_name}:{function}"

        self._active_run_path = path

        return self

    def __enter__(self):
        if self._active_run_path is not None:
            self._active_run = model.Run.new_instance()
            self._metadata_graph.commit(self._active_run, self._active_run_path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._active_run is not None:
            if exc_type is None:
                self._active_run = self._active_run.model_copy(update={
                    "status": model.RunStatus.Finished
                })
            else:
                self._active_run = self._active_run.model_copy(update={
                    "status": model.RunStatus.Failed,
                    "error": str(exc_val)
                })

            self._metadata_graph.update(self._active_run)

        self._active_run_path = None
        self._active_run = None

    def open(self, path: pathlib.PurePosixPath, mode: str = "r") -> io.BytesIO:
        if str(path).startswith("file:"):
            path = str(path).lstrip("file:")
            blob_stream = open(path, mode)

            return data.BlobIO(blob, blob_stream)

        if "w" in mode:
            blob = model.Blob.new_instance(size=0)
            on_sent_callback = functools.partial(self._on_sent, path=path)

            return self._data_repository.open(blob, mode, on_sent_callback)
        
        blob: model.Blob = self.resolve(path)
        on_received_callback = functools.partial(self._on_received)

        return self._data_repository.open(blob, mode, on_received_callback)

    def _on_received(self, blob: model.Blob):
        self._metadata_graph.receive(
            subject_run=self._active_run,
            blob=blob,
        )

    def _on_sent(
        self,
        blob: model.Blob,
        path: pathlib.PurePosixPath,
    ):
        self._metadata_graph.commit(blob, path)

        self._metadata_graph.send(
            subject_run=self._active_run,
            blob=blob,
        )

    def upstream(self, path: pathlib.PurePosixPath) -> list[model.Datum]:
        return self._metadata_graph.upstream(path)

    def downstream(self, path: pathlib.PurePosixPath) -> list[model.Metadata]:
        return self._metadata_graph.downstream(path)

    def clean(self):
        self._metadata_graph.clean()
        self._data_repository.clean()

    def which(self, datum: model.Datum) -> Optional[pathlib.PurePosixPath]:
        commits: list[model.Commit] = self._metadata_graph.find(
            object_type=model.Commit,
            datum_id=datum.id,
        )

        if not any(commits):
            return None
        
        [commit, *_] = commits

        streams: list[model.Stream] = self._metadata_graph.find(
            object_type=model.Stream,
            id=commit.stream_id,
        )

        [stream] = streams

        return stream.path
    