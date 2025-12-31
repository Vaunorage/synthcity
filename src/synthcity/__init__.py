# stdlib
import logging
import os
import sys
import warnings

# third party
import optuna
import pandas as pd

try:
    import pydantic
    if not hasattr(pydantic, "validate_arguments"):
        try:
            from pydantic.v1 import validate_arguments as _validate_arguments

            pydantic.validate_arguments = _validate_arguments
        except Exception:
            # Leave as-is; downstream imports will raise a clear error.
            pass
except Exception:
    pass

try:
    import optuna.storages

    if not hasattr(optuna.storages, "RedisStorage"):

        class RedisStorage:  # type: ignore
            def __init__(self, *args, **kwargs):
                raise NotImplementedError(
                    "optuna.storages.RedisStorage is not available in this optuna version. "
                    "Use RDBStorage/JournalStorage instead."
                )

        optuna.storages.RedisStorage = RedisStorage
except Exception:
    pass

# synthcity relative
from . import logger  # noqa: F401

optuna.logging.set_verbosity(optuna.logging.FATAL)
optuna.logging.disable_propagation()
optuna.logging.disable_default_handler()  # Stop showing logs in sys.stderr.

pd.options.mode.chained_assignment = None

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").setLevel(logging.CRITICAL)
logging.getLogger("tensorflow_hub").setLevel(logging.CRITICAL)

warnings.simplefilter(action="ignore")

logger.add(sink=sys.stderr, level="CRITICAL")
