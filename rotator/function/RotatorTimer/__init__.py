import logging
import os
from datetime import datetime

import azure.functions as func

from shared.rotator_lib import rotate_secret


def main(timer: func.TimerRequest) -> None:
    logging.info("RotatorTimer triggered at %s", datetime.utcnow().isoformat())
    disable_previous = (os.getenv("DISABLE_PREVIOUS", "false").lower() == "true")
    try:
        result = rotate_secret(rotated_by="timer", disable_previous=disable_previous)
        logging.info("Rotated secret '%s' to version '%s' (prev: %s, disabled_prev=%s)",
                     result["secret_name"], result["new_version"], result["previous_version"], result["disabled_previous"]) 
    except Exception as ex:
        logging.exception("Rotation failed: %s", ex)
