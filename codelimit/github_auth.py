import time
import webbrowser
from os.path import expanduser
from pathlib import Path
from typing import Union
from rich import print

import requests  # type: ignore
import yaml  # type: ignore

CLIENT_ID = "Iv1.17776fd3e9de2ba8"
SETTINGS_PATH = Path(f'{expanduser("~")}/.config/codelimit')

cached_token: Union[dict, None] = None


def get_github_token():
    global cached_token
    if cached_token is None:
        cached_token = _read_github_token()
    return cached_token


def _read_github_token():
    result = None
    yml_path = Path(f"{SETTINGS_PATH}/github.yml")
    if yml_path.exists():
        config = yaml.safe_load(open(yml_path))
        if "access_token" in config:
            result = config["access_token"]
    return result


def _write_github_token(token: str):
    yml_path = Path(f"{SETTINGS_PATH}/github.yml")
    Path(SETTINGS_PATH).mkdir(exist_ok=True)
    config = {"access_token": token}
    yaml.dump(config, open(yml_path, "w"))


def device_flow_login() -> Union[dict, None]:
    json = _device_flow_authentication(CLIENT_ID)
    device_code = json["device_code"]
    interval = json["interval"]
    result = _poll_for_token(CLIENT_ID, device_code, interval)
    if result:
        _write_github_token(result["access_token"])
    return result


def device_flow_logout():
    yml_path = Path(f"{SETTINGS_PATH}/github.yml")
    if yml_path.exists():
        yml_path.unlink()


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
    print(f"Enter this code: [cyan]{user_code}[/cyan]")
    print(f"If browser does not open, go to this page: {browser_url}")
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
