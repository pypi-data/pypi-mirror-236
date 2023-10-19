from hamal_utils.code.prefect_utils.env_manager import get_env

MONITOR_TAG_TMPL = "hamalutils-{name}-{from_percent}-{to_percent}"

_EXTENSIONS_FROM_ENV = get_env('LIST_FILES_EXTENSIONS', None)

EXTENSIONS = _EXTENSIONS_FROM_ENV.split(',') if _EXTENSIONS_FROM_ENV else None

FROM_PERCENT = float(get_env('FROM_PERCENT', .0))
TO_PERCENT = float(get_env('TO_PERCENT', 1.0))
BUCKET_FILES_COUNT = int(get_env('BUCKET_FILES_COUNT', '-1'))

if FROM_PERCENT > TO_PERCENT:
    raise Exception("from_percent must be smaller than to_percent")

if FROM_PERCENT > 1 or FROM_PERCENT < 0 or TO_PERCENT > 1 or TO_PERCENT < 0:
    raise Exception("from_percent and to_percent must be in range [0,1]")
