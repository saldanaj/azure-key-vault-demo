import json
import logging
import os

import azure.functions as func

from shared.rotator_lib import rotate_secret, rotate_key_version


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = {}
        if req.get_body():
            try:
                data = req.get_json()
            except ValueError:
                # ignore non-JSON bodies
                data = {}

        provided_value = data.get("value") if isinstance(data, dict) else None
        disable_prev = data.get("disablePrevious") if isinstance(data, dict) else None
        rotate_key_flag = data.get("rotateKey") if isinstance(data, dict) else None

        # allow query string overrides
        if provided_value is None:
            provided_value = req.params.get("value")
        if disable_prev is None:
            dp = req.params.get("disablePrevious")
            if isinstance(dp, str):
                disable_prev = dp.lower() == "true"

        if rotate_key_flag is None:
            rk = req.params.get("rotateKey") or req.params.get("key")
            if isinstance(rk, str):
                rotate_key_flag = rk.lower() == "true"

        if disable_prev is None:
            disable_prev = (os.getenv("DISABLE_PREVIOUS", "false").lower() == "true")

        if rotate_key_flag is None:
            rotate_key_flag = (os.getenv("ROTATE_KEY", "false").lower() == "true")

        result = rotate_secret(rotated_by="http", provided_value=provided_value, disable_previous=disable_prev)
        resp = {"status": "ok", **result}

        if rotate_key_flag:
            key_res = rotate_key_version(rotated_by="http")
            resp.update(key_res)

        return func.HttpResponse(status_code=200, mimetype="application/json", body=json.dumps(resp))
    except Exception as ex:
        logging.exception("HTTP rotate failed: %s", ex)
        return func.HttpResponse(status_code=500, mimetype="application/json", body=json.dumps({
            "status": "error",
            "message": str(ex)
        }))
