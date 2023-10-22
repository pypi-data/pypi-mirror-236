import io
import pathlib
import shutil
from typing import Callable, Optional

from gevulot import model


class BlobIO(io.BytesIO):
    """
    Context manager with constructor accepting important initialisations
    parameters. E.g. file path, S3 object URL.
    """

    def __init__(
        self,
        blob: model.Blob,
        blob_stream: io.BytesIO,
        on_exit_callback: Optional[Callable[[model.Blob, "BlobIO"], None]] = None,
    ):
        self._blob = blob
        self._blob_stream = blob_stream

        self._on_exit_callback = on_exit_callback

        self._has_changed = False
        self._bytes_written = 0

    def __len__(self):
        if self._has_changed:
            return self._bytes_written

        if self._blob_stream.seekable():
            # getting stream length by moving cursor to the very end,
            # reading position and then reverting an original position
            current_pos = self._blob_stream.tell()
            self._blob_stream.seek(0, io.SEEK_END)
            stream_length = self._blob_stream.tell()
            self._blob_stream.seek(current_pos, io.SEEK_SET)

            return stream_length

        return -1

    def __enter__(self):
        self._blob_stream.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._on_exit_callback is not None:
                updated_blob = self._blob.model_copy(update={
                    "size": self._bytes_written
                })
                
                self._on_exit_callback(updated_blob, self)
        finally:
            if not self._blob_stream.closed:
                self._blob_stream.flush()
                self._blob_stream.close()

            return self._blob_stream.__exit__(exc_type, exc_val, exc_tb)

    def write(self, buffer: bytes) -> int:
        if not self._has_changed:
            self._has_changed = True

        self._bytes_written += len(buffer)

        return self._blob_stream.write(buffer)

    def read(self, size: int = -1) -> bytes:
        return self._blob_stream.read(size)

    def getvalue(self) -> bytes:
        return self._blob_stream.getvalue()

    def flush(self):
        self._blob_stream.flush()

    @property
    def closed(self) -> bool:
        return self._blob_stream.closed

    def close(self):
        self._blob_stream.close()

    def seekable(self) -> bool:
        return self._blob_stream.seekable()

    def seek(self, offset: int, whence: int = 0) -> int:
        return self._blob_stream.seek(offset, whence)

    def tell(self) -> int:
        return self._blob_stream.tell()

    def peek(self, size):
        return self._blob_stream.peek(size)

    @property
    def mode(self) -> str:
        return self._blob_stream.mode



class DataRepository(object):
    @staticmethod
    def new_instance() -> "DataRepository":
        return DataRepository(
            data_dir=pathlib.Path("data/blobs"),
        )
    
    def __init__(self, data_dir: pathlib.Path) -> None:
        self._data_dir = data_dir

    def open(
        self,
        blob: model.Blob,
        mode: str = "r",
        on_exit_callback: Optional[Callable[[model.Blob, "BlobIO"], None]] = None,
    ) -> BlobIO:
        physical_blob_path = self._data_dir / blob.unit_name / str(blob.id)

        if "w" in mode:
            physical_blob_path.parent.mkdir(parents=True, exist_ok=True)
        
        blob_stream = physical_blob_path.open(mode)

        return BlobIO(blob, blob_stream, on_exit_callback)

    def clean(self):
        if self._data_dir.exists():
            shutil.rmtree(self._data_dir)
