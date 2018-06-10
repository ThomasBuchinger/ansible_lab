# Bootstrap Guide:  With out-of-band management
This guide assumes one temporary bootstrap VM outside the main environment, which will be used to deploy the rest of the environment and to reinstall the lab more easily later on.

## Step 0: Review variables
- Review all variables in "/inv/devel/home"! This directory contains important variables and all the default-credentials

## Step 1: Setup foreman on the bootstrap VM
- Manually install CentOS on the bootstrap VM and setup public key authentication for ansible
- Run the bootstrap/out-of-band_foreman.yml playbook against the bootstrap VM
- If you are using external DHCP. Set next-server to the IP of the external bootstrap VM.

## Step 1: Choose a compute platform
### VMware vSphere
- To use Vmware vSphere, you need vCenter server up and running. 
- To enable vSphere set the appropriate variables in '/inv/devel/group_vars/home/foreman.yml'

### KVM
- To use KVM as virtualization layer, you have to setup an ansible-enabled CentOS/RedHat machine.
- For simple disk layouts, you can use the foreman on the bootstrap VM.
- Since this will be a physical box, check partitioning and networking is set up correctly.
  - The KVM playbook will setup a VDO device on a seperate disk for VM storage (can be disabled)
  - Make sure the second disk does not have a partition table
- Run bootstrap/setup_kvm.yml playbook

## Step 1.5: Check if the compute resource
- Check if your compute environment is properly set up in foreman.
- For KVM, you have to rerun the bootstrap/out-of-band_foreman playbook again, this will exchange the SSH keys to connect to libvirt over ssh

## Step 2: Deploy the first VMs
- Create 2 new VMs on your environment and use the "provision" network in foreman
- VM 1: This will become your production Foreman host: recommended size 1vCPU, 4 GB memory
- VM 2: This will run FreeIPA and Elastic-Stack: recommended size: 1vCPU, 6 GB memory

## Step 3: Run site.yml
- If you are using external DHCP, set the next-server option to your production foreman
- Run the site.yml playbook, with the extra argument ipa_client_force=true
  ansible-playbook -i inv/production/inventory --vault-password-file vault.key site.yml -e "ipa_client_force=true" -e "ipa_server_force=true"

## Step 6: PROFIT !!!
