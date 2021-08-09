import sys
import telnetlib
import getpass
import yaml

from asrlibs.asrcommand import subscriberList, subscriberDetail, subscriberClear

config = yaml.safe_load(open("./config.yml"))

device = None
user = None
host = None

def printErrorExit(msg, exitcode=1, exitnow=True):
  print('\nERROR: {0}'.format(str(msg)))
  if exitnow is True:
    exit(exitcode)

def sendCommand(cmd):
  
  devicePrompt = "asr1002-{0}>".format(device)
  
  password = getpass.getpass()
  if password is None or len(password)<=0:
    print("ERROR: enter invalid password")
    exit(1)

  tn = telnetlib.Telnet(host)
  tn.read_until(b"Username: ")
  tn.write(user.encode('ascii') + b"\n")
  tn.read_until(b"Password: ")
  tn.write(password.encode('ascii') + b"\n")
  
  try:
    readData = tn.read_until(devicePrompt.encode('utf-8'), 10)
    if "Authentication failed" in readData.decode('utf-8'):
      printErrorExit('Authentication failed')
  except EOFError as e:
    printErrorExit(str(e))
  
  print('\n')
  # print('>>>> auth success')
  
  tn.write(b"terminal length 0\n")
  tn.read_until(devicePrompt.encode('utf-8'), 10)
  
  # print('>>>> set terminal length 0 done')
  
  tn.write(b"\n")
  tn.write(str.encode(cmd + "\n"))
  
  print(">>>> command '{0}' sent".format(cmd))
  print('\n')
  
  try:
    readData = tn.read_until(devicePrompt.encode('utf-8'), 10)
    if devicePrompt not in readData.decode('utf-8'):
      printErrorExit('unexpected {0}'.format(readData.decode('utf-8')))
  except EOFError as e:
    printErrorExit(str(e))
  
  tn.write(b"exit\n")
  
  readData = tn.read_all().decode('utf-8')
  print(readData)
  
  print('\n>>>> tool done.')
  exit(0)

if __name__ == '__main__':
  
  print('\n')
  print('--------------------------------')
  print('  Cisco ASR1000 Python Tool')
  print('--------------------------------')
  print('\n')
  
  if len(sys.argv) < 3:
    printErrorExit("insufficient arguments\n", exitnow=False)
    print('Usage:')
    print('  python asr.py <device name> <command> <command option>\n')
    print('Device name:')
    print('  asr1')
    print('  asr2')
    print('Command and option:')
    print('  list')
    print('  list <filter keyword>')
    print('  uid <subscriber uid>')
    print('  clear <subscriber uid>')
    exit(0)
  
  device = sys.argv[1]
  fn = sys.argv[2]
  opt = None
  
  if device not in config['asr']:
    printErrorExit("enter device '{0}' not found".format(device))
  else:
    host = config['asr'][device]['ip']
    user = config['asr'][device]['username']
    print(">>>> asr '{0}' ip address is '{1}'".format(device, host))
  
  if len(sys.argv) >= 4:
    opt = sys.argv[3]
    print(">>>> connect to '{0}' for command '{1}' with option '{2}'".format(device, fn, opt))
  else:
    print(">>>> connect to '{0}' for command '{1}'".format(device, fn))
    
  print("\n")
  command = None
  if fn=='list':
    command = subscriberList(opt)
  elif fn=='uid':
    command = subscriberDetail(opt)
  elif fn=='clear':
    confirmUID = input('>>>> please enter uid again as confirm: ')
    if confirmUID != opt:
      printErrorExit("uid confirm mismatch")
    print('\n')
    command = subscriberClear(opt)
  else:
    printErrorExit("not found enter function '{0}'".format(fn))
  
  if command is None:
    printErrorExit('insufficient required parameters and/or invoke function incorrectly')
  else:
    sendCommand(command)
