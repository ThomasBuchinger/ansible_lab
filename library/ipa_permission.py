ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: ipa_permission
author: Thomas Buchinger (thomas.buchinger@outlook.com)
short_description: Manage FreeIPA permission
description:
- Add, modify and delete an IPA permissions using IPA API
options:
  cn:
    description:
    - Name of permission.
    - Can not be changed as it is the unique identifier.
    required: true
    aliases: ["name"]
  right:
    description:
      - Rights to grant
      - Values: read, search, compare, write, add, delete, all
    required: true
    aliases: ["perm_right", "ipapermright"]
  attributes:
    description:
      - Effective Attributes
    required: true
    aliases: ["attrs"]
  type:
    description:
      - Object type
    required: true
    aliases: ["object_type"]

  state:
    description:
    - State to ensure.
    required: false
    default: "present"
    choices: ["present", "absent"]
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
permission:
  description: Permission object as returned by IPA API.
  returned: always
  type: dict
'''

from ansible.module_utils.ipa import IPAClient

class PermissionIPAClient(IPAClient):

    def __init__(self, module, host, port, protocol):
        super(PermissionIPAClient, self).__init__(module, host, port, protocol)

    def permission_find(self, name):
        return self._post_json(method='permission_find', name=None, item={'all': True, 'cn': name})

    def permission_add(self, name, item):
        return self._post_json(method='permission_add', name=name, item=item)

    def permission_mod(self, name, item):
        return self._post_json(method='permission_mod', name=name, item=item)

    def permission_del(self, name):
        return self._post_json(method='permission_del', name=name)

    def permission_add_member(self, name, item):
        return self._post_json(method='permission_add_member', name=name, item=item)
    
    def permission_remove_member(self, name, item):
        return self._post_json(method='permission_remove_member', name=name, item=item)

def get_params_dict(params=None):
    data = {}
    if params is None:
      return data

    if params['right'] is not None:
        data['ipapermright'] = params['right']
    if params['attributes'] is not None:
        data['attrs'] = params['attributes']
    if params['object_type'] is not None:
        data['type'] = params['object_type']
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


#def modify_if_diff(module, name, ipa_list, module_list, add_method, remove_method):
#    changed = False
#    diff = list(set(ipa_list) - set(module_list))
#    if len(diff) > 0:
#        changed = True
#        if not module.check_mode:
#            remove_method(name=name, item=diff)
#
#    diff = list(set(module_list) - set(ipa_list))
#    if len(diff) > 0:
#        changed = True
#        if not module.check_mode:
#            add_method(name=name, item=diff)
#    return changed

def ensure(module, client):
    name = module.params['name']
    state = module.params['state']
    permission = module.params['cn']

    ipa_permission = client.permission_find(name=name)
    module_params = get_params_dict(params=module.params)

    changed = False
    if state == 'present':
        if not ipa_permission:
            # Object does not yet exist
            changed = True
            if not module.check_mode:
                ipa_permission = client.permission_add(name=name, item=module_params)
        else:
            # Object exists --> modify
            diff = get_diff(ipa_permission, module_params)
            if len(diff) > 0:
                changed = True
                if not module.check_mode:
                    data = {}
                    for key in diff:
                        data[key] = module_params.get(key)
                    client.permission_mod(name=name, item=data)
    else:
        if ipa_permission:
            changed = True
            if not module.check_mode:
                client.permission_del(name=name)

    return changed, client.permission_find(name=name)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cn=dict(type='str', required=True, aliases=['name']),
            right=dict(type='str', required=True, aliases=['ipapermright', 'perm_right'],
                       choices=['read', 'search', 'compare', 'write', 'add', 'delete', 'all']),
            attributes=dict(type='list', required=True, aliases=['attrs']),
            object_type=dict(type='str', required=True, aliases=['type']),
          
            state=dict(type='str', required=False, default='present',
                       choices=['present', 'absent', 'enabled', 'disabled']),
            ipa_prot=dict(type='str', required=False, default='https', choices=['http', 'https']),
            ipa_host=dict(type='str', required=False, default='ipa.example.com'),
            ipa_port=dict(type='int', required=False, default=443),
            ipa_user=dict(type='str', required=False, default='admin'),
            ipa_pass=dict(type='str', required=True, no_log=True),
            validate_certs=dict(type='bool', required=False, default=True),
        ),
        supports_check_mode=True,
    )

    client = PermissionIPAClient(module=module,
                                host=module.params['ipa_host'],
                                port=module.params['ipa_port'],
                                protocol=module.params['ipa_prot'])

    try:
        client.login(username=module.params['ipa_user'],
                     password=module.params['ipa_pass'])
        changed, permission = ensure(module, client)
        module.exit_json(changed=changed, permission=permission)
    except Exception:
        e = get_exception()
        module.fail_json(msg=str(e))


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception

if __name__ == '__main__':
    main()


