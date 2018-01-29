# Ansible Lab Automation
Keeping up with technology is hard. And sometimes reading websites, blogs and occacional screenshots just don't cut it, what you need is a demo setup.

While creating VMs and configuring basic networking is boring, actually setting up a state of art provisioning system and keeping it running manually is error prone and may cost more time fixing unintended damage, than doing everythingthing manually.

This Ansible project automates the setup of essential infrastructure services and selected open source projects, which allows to quickly spin up complete environments on-demand and tear them down, following a "Cattle instead of Pets" approach.

## Features
### Ansible
The heart piece os this project is the Ansible configuration itself. All the configuration is stored in git, including necessary credentials for external systems, which are encrypted using ansible-vault.  

The site.yml contains infrastructure components (currently FreeIPA and Foreman) which other plays can rely on to be present, while additional applications live in the plays directory. Applications consist of a spinup_<name>.yml which performs setup of the component from stratch (in general using the latest release) and can be disposed again with teardown_<name>.yml, while adhoc plays (play_<name>.yml) are generally smaller and are not associated with a specific component.

### Foreman
Foreman is the provisioning tool in the environment. Configuration includes a all-in-one Foreman+SmartProxy and the necessary setup to automatically provsion new VMs. All VMs come with the latest CentOS release and the SSH key used by ansible for configuration. Compute is provided by VMware vCenter (which is not part ob the project). Additionally to the WebUI, VMs can also be provisioned programatically with the provided playbooks.

Note: Unfortunately the foreman ansible module assumes the Katello API, which is different from the pure Foreman API, therefore all actions have been implemented by a python wrapper around the hammer cli tool.

### FreeIPA
FreeIPA provides DNS resulution and SSO for the environment. New Clients are enrolled automatically and a basic configuration for DNS and User is imported via configuration.

### Openshift Origin
Red Hat's Openshift is certainly worth keeping an eye on (although it is almost as unavoidable as containers themself). At the moment only a dev environment is configured here via 'oc cluster up', but maybe a more production grade setup (using the ansible installer) will be added later.

Openshift Origin is configured as an all-in-one system with only a single master, depending on the number of openshift-nodes in the inventory additional nodes can join the cluster (the first node is still a single master) [comming soon]

## Next
* OpenStack (Dev-Stack)
* Jenkins
* Mail Server
* Foreman IPA Integration
* Monitoring (Icinga, Prometheus, Hawkular?)

## Pre-Existing Infrastructure
* VMware vCenter Server 
* Basic Networking 
* 2 Ansible enabled Machines (for IPA and Foreman)
