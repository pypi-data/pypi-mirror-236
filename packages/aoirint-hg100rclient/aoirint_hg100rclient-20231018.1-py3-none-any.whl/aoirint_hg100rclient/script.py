from aoirint_hg100rclient import HG100RClient, interactive_config, remove_config

def command_login(args):
  interactive_config(skip_ifexist=False)

def command_logout(args):
  remove_config()

def command_wanipv4(args):
  interactive_config()

  hg100r = HG100RClient()

  ipv4_addr = hg100r.get_wan_ipv4()
  print(ipv4_addr)

def command_reboot(args):
  interactive_config()

  hg100r = HG100RClient()

  ret = hg100r.reboot_router()
  print(ret)

def main():
  import argparse
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  parser_login = subparsers.add_parser('login')
  parser_login.set_defaults(handler=command_login)

  parser_logout = subparsers.add_parser('logout')
  parser_logout.set_defaults(handler=command_logout)

  parser_wanipv4 = subparsers.add_parser('wanipv4')
  parser_wanipv4.set_defaults(handler=command_wanipv4)

  parser_reboot = subparsers.add_parser('reboot')
  parser_reboot.set_defaults(handler=command_reboot)

  args = parser.parse_args()

  if hasattr(args, 'handler'):
    args.handler(args)
  else:
    parser.print_help()
