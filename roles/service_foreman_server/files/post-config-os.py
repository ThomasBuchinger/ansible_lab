#!/bin/python
import os
import argparse
import sys
import re
import socket
import subprocess

# Execute a command and return STDOUT and the exit code
#
def call_process(cmd, *args):
  cmd=cmd.format(*args)
  sys.stderr.write(str.format("get_call_process(): {} \n", cmd))
  out = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
  return out.communicate()[0], out.returncode

# Get the ID of an Object in Foreman
#
def get_id_of(type_name, name):
  if type_name == 'os':
    info, status=call_process("hammer os info --title '{}'", name )
  else:
    info, status=call_process("hammer {} info --name '{}'", type_name, name )
  return re.compile("Id:\\s*(\\d+)", re.MULTILINE).search(info.strip()).group(1)

# Link a partition table to a OS
#
def add_partition_table(os_id, ptable_id):
  stdout, status = call_process("hammer os add-ptable --id {} --partition-table-id {}", os_id, ptable_id)
  if status != 0:
    sys.stderr.write(stdout)
    raise RuntimeError("Failed to add partition table to OS")

# Link a config-tempate to the OS and set is as the default
#
def set_default_template(os_id, tmpl_id):
  stdout, status = call_process("hammer os add-config-template --id {} --config-template-id {}", os_id, tmpl_id)
  if status != 0:
    sys.stderr.write(stdout)
    raise RuntimeError("Failed to add Configtemplate to OS")
  stdout, status = call_process("hammer os set-default-template --id {} --config-template-id {}", os_id, tmpl_id)
  if status != 0:
    sys.stderr.write(stdout)
    raise RuntimeError("Failed to set template as default")

# Tell Foreman to rebuild the PXE menu
#
def build_pxe():
  stdout, status = call_process("hammer template build-pxe-default")
  if status != 0:
    sys.stderr.write(stdout)
    raise RuntimeError("Failed to add Configtemplate to OS")



# Imitate the Hammer CLI
#
parser = argparse.ArgumentParser(description='Configure OS for provisioning')
parser.add_argument('--os', nargs=1, help='OS')
parser.add_argument('--partition', nargs='+', help='Associate partition tables')
parser.add_argument('--provision', nargs=1 , help='Set default provision template')
parser.add_argument('--pxe', nargs=1 , help='Set default PXE template')
args = parser.parse_args()
#print args

# Validate Input by fetching the IDs
#
try: 
  os_id=get_id_of('os', args.os[0])
  ptable_ids = []
  for ptable in args.partition:
    ptable_ids.append(get_id_of('partition-table', ptable))
  prov_id=get_id_of('template', args.provision[0])
  pxe_id=get_id_of('template', args.pxe[0])

except AttributeError:
  print "Cannot find object"
  sys.exit(2) 
  
for ptable in ptable_ids:
  add_partition_table(os_id, ptable)
set_default_template(os_id, prov_id)
set_default_template(os_id, pxe_id)
