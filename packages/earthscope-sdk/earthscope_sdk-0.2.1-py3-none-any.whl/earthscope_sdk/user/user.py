import requests
import os

from typing import List

API_BASE_URL = os.environ.get("API_BASE_URL", "https://www.earthscope.org/api/v0")


def get_user(access_token: str):
    r = requests.get(
        f"{API_BASE_URL}/user",
        headers={"authorization": f"Bearer {access_token}"},
    )

    try:
        rjson = r.json()
        if r.status_code == 200:
            return rjson
        error = rjson.get("detail") or rjson.get("message") or rjson
    except Exception:
        r.raise_for_status()
        error = r.text
        
    raise RuntimeError(error)
