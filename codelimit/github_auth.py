import time
import webbrowser
from os.path import expanduser
from pathlib import Path
from typing import Union

import requests  # type: ignore
import yaml  # type: ignore

CLIENT_ID = "Iv1.17776fd3e9de2ba8"
SETTINGS_PATH = Path(f'{expanduser("~")}/.config/codelimit')

cached_token: Union[dict, None] = None


def get_github_token():
    global cached_token
    if cached_token is None or not _token_is_valid(cached_token):
        cached_token = _device_flow_login()
    return cached_token


def _token_is_valid(token: dict):
    return True


def _device_flow_login() -> Union[dict, None]:
    result = None
    yml_path = Path(f"{SETTINGS_PATH}/github.yml")
    config = {}
    if yml_path.exists():
        config = yaml.safe_load(open(yml_path))
        if "access_token" in config:
            result = {"access_token": config["access_token"]}
        if "refresh_token" in config:
            result = _refresh_access_token(CLIENT_ID, config["refresh_token"])
    if not result:
        json = _device_flow_authentication(CLIENT_ID)
        device_code = json["device_code"]
        interval = json["interval"]
        result = _poll_for_token(CLIENT_ID, device_code, interval)
    if result:
        Path(SETTINGS_PATH).mkdir(exist_ok=True)
        if "refresh_token" in result:
            config["refresh_token"] = result["refresh_token"]
        else:
            config["access_token"] = result["access_token"]
        yaml.dump(config, open(yml_path, "w"))
    return result


def _device_flow_authentication(client_id: str):
    res = requests.post(
        "https://github.com/login/device/code",
        headers={"Accept": "application/json"},
        params={"client_id": client_id, "scope": "repo read:org"},
    )
    json = res.json()
    user_code = json["user_code"]
    browser_url = json["verification_uri"]
    print("Device authentication required.")
    print(f"Enter this code: {user_code}")
    print(f"If browser does not open go to this page: {browser_url}")
    webbrowser.open(browser_url)
    return json


def _poll_for_token(client_id: str, device_code: str, interval: int):
    print("Waiting for authentication...")
    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    params = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    while True:
        response = requests.post(url, headers=headers, params=params)
        if response.ok:
            token = response.json()
            if "error" not in token and "access_token" in token:
                break
        time.sleep(interval + 1)
    return token


def _refresh_access_token(client_id: str, refresh_token: str):
    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    params = {
        "client_id": client_id,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "scope": "repo read:org",
    }
    result = {}
    response = requests.post(url, headers=headers, data=params)
    if response.ok:
        result = response.json()
        print(result)
    return result
