# Ansible Lab Automation
> :warning: **Deprcation Notice**: This is the last commit before a major restructure of the project!

Keeping up with technology is hard. And sometimes reading websites, blogs and occacional screenshots just don't cut it, what you need is a demo setup.

While creating VMs and configuring basic networking every time is boring, actually setting up automatic provisioning and keeping it running manually is error prone and may cost more time fixing unintended damage, than doing everything manually.

This Ansible project automates the setup of essential infrastructure services and selected open source projects, which allows to quickly spin up complete environments on-demand and tear them down, following a "Cattle instead of Pets" approach.

## Features
### Ansible
The heart piece os this project is the Ansible configuration itself. All the configuration is stored in git, including necessary credentials for external systems, which are encrypted using ansible-vault.  

### KVM Hypervisor
The virtualization layer is implemented with KVM and libvirt. While it is no full blown datacenter virtualization solution like oVirt or VMware vCenter (which is sort-of-mandatory for API integrations), it has a way smaller footprint and libvirt serves as an excellent interface to other management interfaces. For day-to-day operations this lab uses Cockpit and Foreman

### Foreman
Foreman is the provisioning tool in the environment. Configuration includes a all-in-one Foreman+SmartProxy and the necessary setup to automatically provsion new VMs. All VMs come with the latest CentOS 7 or 8 and the SSH key used by ansible for configuration. Possible compute resources are KVM/libvirt (prefered) or VMware vSphere.

> :information_source: Unfortunately the foreman ansible module assumes the Katello API, which is different from the pure Foreman API, therefore all actions have been implemented by a python wrapper around the hammer cli tool.

### Kubernetes
Kubernetes is at the center of the container revolution and no lab is complete without a Kubernetes cluster. But Kubernetes allone is no complete container platform, additional components are: 

Component | Project
---|---
CRI | Docker
CNI | WeaveNet
WebuUI | OKD Console
Registry | Docker-Registry
Storage | Local<br>NFS<br>Gluster
ServiceMesh | Istio (unused for now)
Ingress-Controller | traefik
Monitoring | Grafana<br>Prometheus<br>loki<br>Jaeger
GitOps | ArgoCD

### Storage
Storage has 3 Tiers: most storage either ephermeral or automated (e.g. VMs, K8s-Config, ...), important can be stored on NFS (not part of th lab) and everything else uses GlusterFS

GlusterFS is a network Storage, that aggregates local disks into a global namespace. It can run on almost any Filesystem and has a very small footprint, making it perfect for hyperconverged use-cases

### Internet hosting
Parts of the Lab can be exposed to the Internet. It uses the Kubernetes Cluster to deploy individual URLs (Ingress-Objects) and a traefik reverse proxy (on an isolated node) forwards the traffic, after it generates a LetsEncrypt Certificate and authenticates the user using oAuth.

### Additional features
* KVM performs deduplication on the libvirt storage pool
* Small DNS server (dnsmasq) for name resolution
* All nodes run Cockpit for GUI based remote administration
* SSH keys are managed in the background and updated automatically
* External storage can be mounted via NFS

The site.yml contains infrastructure components (currently FreeIPA and Foreman) which other plays can rely on to be present, while additional applications live in the plays directory. Applications consist of a spinup_<name>.yml which performs setup of the component from stratch (in general using the latest release) and can be disposed again with teardown_<name>.yml, while adhoc plays (play_<name>.yml) are generally smaller and are not associated with a specific component.

Additional roles:
- common: Install common packages.  
  All nodes run Cockpit for simple GUI based activities 
- config_nfs: simple NFS mount
- config_ssh_key: Enables management of SSH keys (manage key files, known_hosts and authorized_keys) 
- config_ssh_server: Hardened SSH server that only accepts PublicKey Authentication
- config_vdo: Configures Virtual-Data-Optimizer (vdo) driver for dedup and compresion on a disk


## Next
* Terraform
* Make all playbooks compatible to Ansible 2.10s colections
* Notifications (Push or Chat)
* OpenStack (Dev-Stack)
* Jenkins
* Mail Server

## Pre-Existing Infrastructure
* Any Red Hat or CentOS box (for KVM) or VMware vCenter Server
* Basic Networking
* Manualy set up one VM for Foreman 
