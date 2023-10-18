from getpass import getpass
import json
import os
from pathlib import Path
from pydantic import BaseModel, parse_obj_as

CONFIG_PATH = Path(os.path.expanduser('~/.hg100rclientrc'))

class ConfigNotExistError(Exception):
  pass

class Config(BaseModel):
  router_url: str
  password: str

def load_config() -> Config:
  env_router_url = os.environ.get('HG100R_ROUTER_URL')
  env_password = os.environ.get('HG100R_PASSWORD')
  if env_router_url or env_password:
    assert env_router_url and env_password
    return Config(
      router_url=env_router_url,
      password=env_password,
    )

  if not CONFIG_PATH.exists():
    raise ConfigNotExistError('Config not exist. Call interactive_config()')

  with open(CONFIG_PATH, 'r', encoding='utf-8') as fp:
    return parse_obj_as(Config, json.load(fp))

def save_config(config: Config):
  with open(CONFIG_PATH, 'w', encoding='utf-8') as fp:
    fp.write(config.json())

def remove_config():
  CONFIG_PATH.unlink(missing_ok=True)

def interactive_config(skip_ifexist: bool=True):
  try:
    load_config()
    if skip_ifexist:
      return
  except ConfigNotExistError:
    pass

  router_url = input('Router URL (e.g. http://192.168.0.1): ')
  password = getpass(prompt='Password: ')

  save_config(Config(
    router_url=router_url,
    password=password,
  ))
