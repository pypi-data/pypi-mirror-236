import hashlib
import json
from urllib.parse import urljoin
import requests
from typing import Dict, Any

from .config import Config, load_config

class HG100RClient:
  def __init__(self, config: Config = None):
    if config is None:
      config = load_config()
    self.config = config

  def get_wan_ipv4(self):
    api_url = urljoin(self.config.router_url, '/api')

    token = get_token_with_raw_password(
      api_url=api_url,
      password=self.config.password,
    )

    return get_wan_ipv4(
      api_url=api_url,
      token=token,
    )

  def reboot_router(self):
    api_url = urljoin(self.config.router_url, '/api')

    token = get_token_with_raw_password(
      api_url=api_url,
      password=self.config.password,
    )

    return reboot_router(
      api_url=api_url,
      token=token,
    )


def get_hashed_password(
  password: str,
  salt: str,
) -> str:
  dk = hashlib.pbkdf2_hmac(
    hash_name='sha1',
    password=password.encode('ascii'),
    salt=salt.encode('ascii'),
    iterations=2048,
    dklen=16,
  )

  return dk.hex()


def get_salt(
  api_url: str,
  timeout: float = 3.0,
) -> str:
  payload = {
    'method': 'Device.getDBInfo',
    'id': 90,
    'jsonrpc': '2.0',
    'params': {
      'WEB_KEY': '',
    },
  }

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  }

  res = requests.post(api_url,
    headers=headers,
    data=json.dumps(payload),
    timeout=timeout,
  )
  response = res.json()

  result = response['result']
  webkey = result['WEB_KEY']

  return webkey


def get_token(
  api_url: str,
  hashed_password: str,
  timeout: float = 3.0,
) -> str:
  payload = {
    'method': 'login',
    'id': 1,
    'jsonrpc': '2.0',
    'params': {
      'id': 'admin',
      'password': hashed_password,
    },
  }

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  }

  res = requests.post(api_url,
    headers=headers,
    data=json.dumps(payload),
    timeout=timeout,
  )
  response = res.json()

  token = response['token']
  return token


def get_token_with_raw_password(
  api_url: str,
  password: str,
  timeout: float = 3.0,
) -> str:
  salt = get_salt(api_url=api_url)
  hashed_password = get_hashed_password(password=password, salt=salt)

  token = get_token(
    api_url=api_url,
    hashed_password=hashed_password,
    timeout=timeout
  )

  return token


def get_wan_ipv4(
  api_url: str,
  token: str,
  timeout: float = 3.0,
) -> str:
  payload = {
    'method': 'QuickSetupInfo',
    'id': 90,
    'jsonrpc': '2.0',
    'token': token,
  }

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  }

  res = requests.post(api_url,
    headers=headers,
    data=json.dumps(payload),
    timeout=timeout,
  )
  response = res.json()

  result = response['result']

  ipv4_addr = result['NET_WAN_IPv4_Address']
  return ipv4_addr


def reboot_router(
  api_url: str,
  token: str,
  timeout: float = 3.0,
) -> Dict[str, Any]:
  payload = {
    'method': 'System.reboot',
    'id': 24,
    'jsonrpc': '2.0',
    'token': token,
  }

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  }

  res = requests.post(api_url,
    headers=headers,
    data=json.dumps(payload),
    timeout=timeout,
  )
  response = res.json()

  # result = response['result']

  return response
