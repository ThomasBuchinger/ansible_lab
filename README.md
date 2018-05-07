# Ansible Lab Automation
Keeping up with technology is hard. And sometimes reading websites, blogs and occacional screenshots just don't cut it, what you need is a demo setup.

While creating VMs and configuring basic networking is boring, actually setting up a state of art provisioning system and keeping it running manually is error prone and may cost more time fixing unintended damage, than doing everything manually.

This Ansible project automates the setup of essential infrastructure services and selected open source projects, which allows to quickly spin up complete environments on-demand and tear them down, following a "Cattle instead of Pets" approach.

[Overview](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=lab_overview.xml#R1Vtbc5s4FP41fmzH3PFjbk06SbaZcafdPmKQbTYYsUJO4v31KxkJ0MUOsYVN8hI4SEIcfec7F8kj52r1douiYvkIE5CN7HHyNnKuR7ZtubZP%2FlHJppL4YVAJFihNWKNGME3%2FA0w4ZtJ1moBSaIghzHBaiMIY5jmIsSCLEIKvYrM5zMS3FtECKIJpHGWq9Hea4GUlDe2gkd%2BBdLHkb7b8SfVkFsXPCwTXOXvfyHbm27%2Fq8SriY7EPLZdRAl9bIudm5FwhCHF1tXq7AhnVLVdb1e%2Fbjqf1vBHIcZcOdtXhJcrW7NPvfz0Swd2mAOglLSEa2X5Ghrqc0asFvWIzxxuure33AjrimDx%2BXaYYTIsopk9fCT6IbIlXGbmz6t7tGbJJvwCEwVtLxGZ8C%2BAKYLQhTdhTe8y0x9DlhOz%2BtVkrn7dZttbJZ7KIwWNRD92oiFwwLek15igay9LZS4pwouiFLG5BLwsEY1CWg9GN5Wt0YxvQjavo5htEYBXlnwBE9X1bUaFGUa4BRfmKor4%2FXRDBlBgdGKLJuZK2NKiydRZnQlmhoixFHSBPLijtk7s4i8oyjUUN1DRLtVViBJ%2FBFcwIudHejh%2BHYDYnTxqt0k5EW2jzN%2B301eO3f9gY4C3FrUfk7g%2FrNU%2BzrDV2EoFwHu9bhBKuUSz5PxyhBcAC4YBEcFnqSrWWwtOsBJchkEU4fREdnW552BueYEom3JiNK5lNKK1w9TmsV9vzSANZ7w1U6UAZiKxztGk1K2iDsvuEHdkjyu3Dve3JRTWDBrr1GnRC86RvNM9Cz%2FXGKpq1iB3vwXltA08ApeQLAWIdJIjPwxjE3SHuqRDnjmMoGPckaHoHYtwOJCxNesL4RHwPd%2FC75uV6e9sfjXFOYy2QX8FVscZAwfoQYqSaIlrw0nl%2BEyGS5ajmTlA%2FZbcQ4SVcwDzKbhrppejtW8pojNqW%2FVDLqm3FrAUG%2BQdgvGE5WLTGkIiaaTxAWPBOMtOMt3%2FH%2BDYue9fwO1t053XwFIj%2BBjMi%2BJ4ToptT9A0RqpYunO8Lq7Zqxr8eX8nnUNkVoIrqLWZFEJMFhzm5%2FTKh7ZOoXNbOzIBmLTlR0sX%2FtkazJkLaerr9x7S7I9V9fl%2BMHYzHtHZXuz%2BNw5djUc860OFbE08ElWyGpwlqj3bgmkz%2BHqAZQLAcBC3K6WhtqG3j1eWjRmhRdR0P1xdPg1CMd07FuIFKYh%2BIbSx9bGO1aKsdy1TMFfQU24T2zPF9Dfd5IEzcrtzHC8Zt7nO7JjvGYx4%2BmxZwb0FOkruYCGnZ9xiH3QN4nbGlgFdXujRS1rWUzzeA3Y8l22aQW%2Bf%2FR6XpvOp2UJpuHrlqDXA6vTuecZUo04Rv8i3JN3dDsQkGdmxFTz8KkJfLdE6jhx8oXaQ5ufgLJmp%2Bc2pz9633zd2a9GXvfi%2F2Lvgq7xPZu3NMWc64vTtqiHUPNnEGo%2Bezw9YNbTHE8tUQywt7Qq3qwX9crMlbB8mEni0Fo9p92n6Y0D2uztbZn5%2FIhvfRSDf71vhz1zZt3%2FpsNZBx0DErPiBxdU9N61Z7NapnQ0pAtMt%2BPlpXw7gmAbkoirNzu4xU3c6AjttN1ASd0%2B0M7t3x24n5o%2BILzjXCznbQEYinqQIG8i6avFvXvQooDuTKrt9QFdCXeXW8f9tPaT8xWzV0T5BDv3cwwwz51tXzoyrfnBWEmDo8F%2Fny2bT45THK6UHIo4NHA8wrH7vQMW9%2FhUs1bb77%2BfNpuwrkE0q64fWE4Nvm7A7Kd8Xigm47sC8H5Xr9mHfwWWtkPJA6QUz9UdfgBSJO%2BC7cLtegBD6WYdegbijdkAAGbyO%2FKY7i4eX1WgayerIt73McR5D33TSlD%2B0xUBMk7amHZoeoIpmhNSrSMrQRFanlIX4uI0lfBN34%2F67pbwwuyVfhL1GWLvKRQ08gZ4BWivnT5ixHNUpZbM9yb2W07kTUlMZV3Yi1IFNsN2qJtzMQpeYnVUU0K7p8w5jQA1yUH5yKBGL6binLE9xZDnMgeTImYhO%2BjqujOs4lRTFZr%2ByCPVilSbL10jqzEPl3hxlojGV3iOe%2BSx6WpSEPI%2Fza%2ByHyXcdu61hGLBTZ72fUUgih5aV26FFZ%2F7myZ%2FmkWiCtWuczs579VTxE0zF7PiAq8SYqCI6IaHcstbmaYMe01BRwDCPi4F8KBJ6ECMuvJeZBweHWLyiCk1eKB4qKg4tsPKXg6JoYAgS5bX5%2FWTVvfuTq3PwP)

## Features
### Ansible
The heart piece os this project is the Ansible configuration itself. All the configuration is stored in git, including necessary credentials for external systems, which are encrypted using ansible-vault.  

### KVM Hypervisor
The virtualization layer is implemented with KVM and libvirt. While it is no full blown datacenter virtualization solution like oVirt or VMware vCenter (which is sort-of-mandatory for API integrations), it has a way smaller footprint and libvirt serves as an excellent interface to other management interfaces. For day-to-day operations this lab uses WebVirtManager and new VMs are created via Foreman

### Foreman
Foreman is the provisioning tool in the environment. Configuration includes a all-in-one Foreman+SmartProxy, with IPA as authentication provider and the necessary setup to automatically provsion new VMs. All VMs come with the latest CentOS release and the SSH key used by ansible for configuration. Possible compute resources are KVM/libvirt (prefered) or VMware vSphere. Additionally to the WebUI, VMs can also be provisioned programatically with the provided playbooks.

Note: Unfortunately the foreman ansible module assumes the Katello API, which is different from the pure Foreman API, therefore all actions have been implemented by a python wrapper around the hammer cli tool.

### FreeIPA
FreeIPA provides DNS resulution and SSO for the environment. All Clients are automatically enrolled, DNS Records and Users are imported from via configuration. The password policy is relaxed to allow never expiring passwords.

Note: Additional IPA modules are included, since the original modules do not cover the whole API (yet)

### Elatic-Stack
A small Elastic-Stack (only Beats, elasticsearch and Kibana) is responsible for log and status monitoring. The push architecture makes it a perfect match for a lab, where services come and go and the dashboards shipped by Elastic cover most monitoring needs

### Openshift Origin
The Upstream project Red Hat's Kubernetes distribution Openshift Enterprise. The setup is a single node development setup configured via 'oc cluster up', maybe a more production grade, multi-node setup will be added later

### Additional features
* All nodes run Cockpit for GUI based remote administration
* SSH keys are managed in the background and updated automatically
* External storage can be mounted via NFS

The site.yml contains infrastructure components (currently FreeIPA and Foreman) which other plays can rely on to be present, while additional applications live in the plays directory. Applications consist of a spinup_<name>.yml which performs setup of the component from stratch (in general using the latest release) and can be disposed again with teardown_<name>.yml, while adhoc plays (play_<name>.yml) are generally smaller and are not associated with a specific component.

Additional roles:
- common: Install common packages.  
  All nodes run Cockpit for simple GUI based activities 
- config_ipa_client: Enrolles a client in FreeIPA
- config_nfs: simple NFS mount
- config_ssh_key: Enables management of SSH keys (manage key files, known_hosts and authorized_keys) 
- service_docker_daemon: Configures Docker daemon (used by Openshift)


## Next
* Gluster Storage and VDO for KVM
* Push Notifications
* Keycloak and reverse proxy for webapps
* OpenStack (Dev-Stack)
* Jenkins
* Mail Server
* Monitoring (Icinga, Prometheus, Hawkular?)

## Pre-Existing Infrastructure
* Any CentOS box (for KVM) or VMware vCenter Server
* Basic Networking 
* 2 Ansible enabled Machines (for IPA and Foreman)
