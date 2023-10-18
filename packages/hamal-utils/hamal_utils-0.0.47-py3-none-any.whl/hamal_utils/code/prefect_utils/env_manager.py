import os

from prefect.blocks.system import String

env_type = os.environ.get('IRON_ENV')

_sentinel = object()


def get_env(name, default=_sentinel):
    try:
        if env_type is None:
            prefect_name = name.lower().replace('_', '-')
            return String.load(prefect_name).value

        os_env_name = name.upper().replace('-', '_')
        return os.environ[os_env_name]
    except Exception as e:
        if default is not _sentinel:
            return default
        raise e
