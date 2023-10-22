import dataclasses

from gevulot.lib import config


@dataclasses.dataclass
class InProcMetadataRepositoryConfig:
    pass


@dataclasses.dataclass
class LocalMetadataRepositoryConfig:
    data_dir: str


class MetadataConfig(config.BaseConfig):
    default_metadata_repository: str
    in_proc_metadata_repository: InProcMetadataRepositoryConfig
    local_metadata_repository: LocalMetadataRepositoryConfig