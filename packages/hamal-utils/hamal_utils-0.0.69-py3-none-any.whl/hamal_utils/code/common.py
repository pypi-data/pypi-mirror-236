import os

MONITOR_TAG_TMPL = "hamal-utils-{name}-{from_percent}-{to_percent}"

IGNORE_LOG_TAG = float(os.environ.get("IGNORE_LOG_TAG", 1))
DISABLE_LOG_TAG = float(os.environ.get("ENABLE_LOG_TAG", 1))

FROM_PERCENT = float(os.environ.get("FROM_PERCENT", .0))
TO_PERCENT = float(os.environ.get("TO_PERCENT", 1.0))

BUCKET_FILES_COUNT = int(os.environ.get("BUCKET_FILES_COUNT", -1))

if FROM_PERCENT > TO_PERCENT:
    raise Exception("from_percent must be smaller than to_percent")

if FROM_PERCENT > 1 or FROM_PERCENT < 0 or TO_PERCENT > 1 or TO_PERCENT < 0:
    raise Exception("from_percent and to_percent must be in range [0,1]")

MAX_WORKERS = int(os.environ.get("MAX_WORKERS", 5))
