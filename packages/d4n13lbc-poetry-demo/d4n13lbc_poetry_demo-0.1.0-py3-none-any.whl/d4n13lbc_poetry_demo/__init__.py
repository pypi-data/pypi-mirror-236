from wakeonlan import send_magic_packet

def send_package():
  print("Sending package")
  send_magic_packet('74:78:27:09:22:1c')
  print("Package sent")
  return True
