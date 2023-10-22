import dataclasses
import os
import pathlib
from typing import Optional, Type, TypeVar

import orjson
import pyhocon
from loguru import logger


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, option=orjson.OPT_INDENT_2).decode()


TConfig = TypeVar("TConfig")


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d # Not a dataclass field


@dataclasses.dataclass
class BaseConfig:
    _config = None


    @classmethod
    def new_instance(
        cls: Type[TConfig], config_file_path: Optional[pathlib.Path] = None
    ) -> TConfig:
        if config_file_path is None:
            config_file_path = pathlib.Path(
                os.getenv("WORMHOLE__CONFIG_FILE_PATH", "wormhole.conf")
            )

        if BaseConfig._config is None:
            BaseConfig._config = pyhocon.ConfigFactory.parse_file(config_file_path)
            logger.debug(f"Loaded configuration from {config_file_path}")

        config_section_path = cls.__module__
        # for config objects module names take a form of
        # "wormhole.<parent_0>...<parent_N>.config" as by convention
        # they are defined inside config.py files
        # so by taking [1:-1] elements we strip out "wormhole" and "config" parts
        parent_config_sections = config_section_path.split(".")[1:-1]

        config_section = BaseConfig._config
        for parent_config_section in parent_config_sections:
            if parent_config_section not in config_section:
                raise ValueError(
                    f"No config section found for module '{config_section_path}' "
                    f"inside '{config_file_path}' file. "
                    f"'{parent_config_section}' parent section is missing"
                )

            config_section = config_section[parent_config_section]

        config_section = dataclass_from_dict(cls, config_section)

        return config_section