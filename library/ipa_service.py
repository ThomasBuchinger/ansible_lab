ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: ipa_privilege
author: Thomas Buchinger (thomas.buchinger@outlook.com)
short_description: Manage FreeIPA privileges
description:
- Add, modify and delete an IPA privileges using IPA API
options:
  cn:
    description:
    - Name of privilege.
    - Can not be changed as it is the unique identifier.
    required: true
    aliases: ["name"]
  description:
    description:
      - Rights to grant
    required: false
  permissions:
    description:
      - Permissions this Privilege should have
    required: true
    aliases: ["object_type"]
  mode:
    description:
      - What to do with the permissions
      -   add: add to existing permissions
      -   remove: remove from existing permissions
      -   set: set permissions 
    required: true
    default: "add"

  state:
    description:
    - State to ensure.
    required: false
    default: "present"
    choices: ["present", "absent", "set"]
  ipa_port:
    description: Port of IPA server
    required: false
    default: 443
  ipa_host:
    description: IP or hostname of IPA server
    required: false
    default: "ipa.example.com"
  ipa_user:
    description: Administrative account used on IPA server
    required: false
    default: "admin"
  ipa_pass:
    description: Password of administrative user
    required: true
  ipa_prot:
    description: Protocol used by IPA server
    required: false
    default: "https"
    choices: ["http", "https"]
  validate_certs:
    description:
    - This only applies if C(ipa_prot) is I(https).
    - If set to C(no), the SSL certificates will not be validated.
    - This should only set to C(no) used on personally controlled sites using self-signed certificates.
    required: false
    default: true
version_added: "2.5"
'''

#EXAMPLES = '''
## Ensure host-group databases is present
#- ipa_hostgroup:
#    name: databases
#    state: present
#    host:
#    - db.example.com
#    hostgroup:
#    - mysql-server
#    - oracle-server
#    ipa_host: ipa.example.com
#    ipa_user: admin
#    ipa_pass: topsecret
#
## Ensure host-group databases is absent
#- ipa_hostgroup:
#    name: databases
#    state: absent
#    ipa_host: ipa.example.com
#    ipa_user: admin
#    ipa_pass: topsecret
#'''

RETURN = '''
privilege:
  description: privilege object as returned by IPA API.
  returned: always
  type: dict
'''

from ansible.module_utils.ipa import IPAClient

class ServiceIPAClient(IPAClient):

    def __init__(self, module, host, port, protocol):
        super(ServiceIPAClient, self).__init__(module, host, port, protocol)

    def service_find(self, name):
        return self._post_json(method='service_find', name=None, item={'all': True, 'krbprincipalname': name})

    def service_add(self, name, item):
        return self._post_json(method='service_add', name=name, item=item)

    def service_mod(self, name, item):
        return self._post_json(method='service_mod', name=name, item=item)

    def service_del(self, name):
        return self._post_json(method='service_del', name=name)
    
    def service_add_host(self, name, item):
        return self._post_json(method='service_add_host', name=name, item={'host': item})
    
    def service_remove_host(self, name, item):
        return self._post_json(method='service_remove_host', name=name, item={'host': item})

def get_params_dict(params=None):
    data = {}
    if params is None:
      return data

    if params['force'] is not None:
        data['force'] = params['force']
#    if params['member'] is not None:
#        data['member'] = params['member']
#    if params['permissions'] is not None:
#        data['permission'] = params['permissions']
    return data

def get_diff(ipa_object, module_object):
    data = []
    for key in module_object.keys():
        ipa_value = ipa_object.get(key, None)
        module_value = module_object.get(key, None)

        # if ipa_value is a list, but module_value not, 
        if isinstance(ipa_value, list) and not isinstance(module_value, list):
            module_value = [module_value]
        # If we are dealing with lists, sorted them
        if isinstance(ipa_value, list) and isinstance(module_value, list):
            ipa_value = sorted(ipa_value)
            module_value = sorted(module_value)

        # if the values differ, use the new value
        if ipa_value != module_value:
            data.append(key)
    return data


def modify_if_diff(module, name, ipa_list, module_list, add_method, remove_method):
    changed = False
    state = module.params['mode']

    if state is 'remove' or state is 'set':
        diff = list(set(ipa_list) - set(module_list))
        if len(diff) > 0:
            changed = True
            if not module.check_mode:
                for host in diff:
                    remove_method(name=name, item=host)

    if state is 'add' or state is 'set':
        diff = list(set(module_list) - set(ipa_list))
        if len(diff) > 0:
            changed = True
            if not module.check_mode:
                for host in diff:
                    add_method(name=name, item=host)
    return changed

def ensure(module, client):
    name = module.params['name']
    state = module.params['state']
    force = module.params['force']
    hosts = module.params['hosts']

    ipa_object = client.service_find(name=name)
    module_params = get_params_dict(params=module.params)

    changed = False
    if state == 'present':
        if not ipa_object:
            # Object does not yet exist
            changed = True
            if not module.check_mode:
                ipa_object = client.service_add(name=name, item=module_params)
        else:
            # Services have nothing to update
            pass
        # Privilege is present, now add permissions

        if hosts is not None:
            changed = client.modify_if_diff(name, ipa_object.get('host', []), [item.lower() for item in hosts],
                                            client.service_add_host, client.service_remove_host) or changed 
    else:
        if ipa_object:
            changed = True
            if not module.check_mode:
                client.service_del(name=name)

    return changed, client.service_find(name=name)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cn=dict(type='str', required=True, aliases=['name']),
            force=dict(type='str', required=False, default='false'),
            mode=dict(type='str', required=True,
                       choices=['add', 'remove', 'set']),
            hosts=dict(type='list', required=False),
          
            state=dict(type='str', required=False, default='present',
                       choices=['present', 'absent']),
            ipa_prot=dict(type='str', required=False, default='https', choices=['http', 'https']),
            ipa_host=dict(type='str', required=False, default='ipa.example.com'),
            ipa_port=dict(type='int', required=False, default=443),
            ipa_user=dict(type='str', required=False, default='admin'),
            ipa_pass=dict(type='str', required=True, no_log=True),
            validate_certs=dict(type='bool', required=False, default=True),
        ),
        supports_check_mode=True,
    )

    client = ServiceIPAClient(module=module,
                                host=module.params['ipa_host'],
                                port=module.params['ipa_port'],
                                protocol=module.params['ipa_prot'])

    try:
        client.login(username=module.params['ipa_user'],
                     password=module.params['ipa_pass'])
        changed, service = ensure(module, client)
        module.exit_json(changed=changed, service=service)
    except Exception:
        e = get_exception()
        module.fail_json(msg=str(e))


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception

if __name__ == '__main__':
    main()


