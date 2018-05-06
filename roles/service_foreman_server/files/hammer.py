#!/bin/python
import os
import argparse
import sys
import re
import socket
import subprocess

# Execute a command and return STDOUT and the return code
#
def call_process(cmd, *args):
  # Build the command from a format String
  cmd=cmd.format(*args)
  sys.stderr.write(str.format("get_call_process(): {} \n", cmd))
  out = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
  return out.communicate()[0], out.returncode

# Get the ID of an Object in Foreman
#
def get_id_of(type_name, name):
  if type_name == 'os':
    info, status=call_process("hammer os info --title {}", name )
  else:
    info, status=call_process("hammer {} info --name {}", type_name, name )
  return re.compile("Id:\\s*(\\d+)", re.MULTILINE).search(info.strip()).group(1)

# Imitate the Hammer CLI
# Configure argparse to simulate the hammer CLI while parsing the resource type and verb
#
parser = argparse.ArgumentParser(description='Run hammer with additional features')
parser.add_argument('type', help='Foreman Object type')
parser.add_argument('verb', help='Action verb')
parser.add_argument('hammer_args', nargs=argparse.REMAINDER , help='additional hammer arguments')
args = parser.parse_args()


hostname=socket.getfqdn()
resource_name=None

# loop through the Arguments and search for additional information we might need
#
for n,value in enumerate(args.hammer_args):
  # Replace AUTO vars and get the name
  # This wrapper allows to replace actual variables with AUTO_<type>_<resrouce-name> and search for the IDs in Foreman
  #
  arr=value.split('_')
  if arr[0] == "AUTO":
    id_val=get_id_of(arr[1].lower(), arr[2])
    sys.stderr.write(str.format("Found ID for {}: {} to be {} \n", arr[1], arr[2], id_val ))
    args.hammer_args[n]=id_val
  # We need to known the resource name to check if the resource already exists
  #
  if arr[0] == "--name":
    resource_name=args.hammer_args[n+1]


# Check if element exists
#
if args.type == "os":
  # Of course at least one resource type down not use a name attribute
  stdout, res_status = call_process( "hammer os info --title {}", resource_name  )
else:
  stdout, res_status = call_process( "hammer {} info --name {}", args.type, resource_name )

# Check the Exit Code of the query
if res_status == 70:
  # exit code 70 --> resource not found
  # run the hammer command and print the sub-process STDOUT to our STDOUT
  create_stdout, exit_code = call_process( "hammer {} {} '{}'", args.type, args.verb, "' '".join(args.hammer_args)  )
  print create_stdout
  if exit_code == 0:
    # success, exit with 1 to indicate we have changed something
    sys.exit(1)
  else:
    # command failed. this is bad
    sys.exit(exit_code)
elif res_status == 0:
  # exit code 0 --> Resource exists
  sys.exit(0)
else:
  # not zero and not 70. this is really bad
  sys.exit(2)
