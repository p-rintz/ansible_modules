#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Pavel Korovin (@pkorovin) <p@tristero.se>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_route_target
short_description: Creates or removes route targets from Netbox
description:
  - Creates or removes route targets from Netbox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@fragmentedpacket)
requirements:
  - pynetbox
version_added: "2.0.0"
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
    type: str
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
    type: str
  cert:
    description:
      - Certificate path
    required: false
    type: raw
  data:
    type: dict
    description:
      - Defines the route target configuration
    suboptions:
      name:
        description:
          - Route target name
        required: true
        type: str
      tenant:
        description:
          - The tenant that the route target will be assigned to
        required: false
        type: raw
      description:
        description:
          - Tag description
        required: false
        type: str
      tags:
        description:
          - Any tags that the device may need to be associated with
        required: false
        type: list
      custom_fields:
        description:
          - must exist in Netbox
        required: false
        type: dict
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/netbox_utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test route target creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create Route Targets
      netbox.netbox.netbox_route_target:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: "{{ item.name }}"
          tenant: "Test Tenant"
          tags:
            - Schnozzberry
      loop:
        - { name: "65000:65001", description: "management" }
        - { name: "65000:65002", description: "tunnel" }

    - name: Update Description on Route Targets
      netbox.netbox.netbox_route_target:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: "{{ item.name }}"
          tenant: "Test Tenant"
          description: "{{ item.description }}"
          tags:
            - Schnozzberry
      loop:
        - { name: "65000:65001", description: "management" }
        - { name: "65000:65002", description: "tunnel" }

    - name: Delete Route Targets
      netbox.netbox.netbox_route_target:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: "{{ item }}"
        state: absent
      loop:
        - "65000:65001"
        - "65000:65002"
"""

RETURN = r"""
route_target:
  description: Serialized object as created/existent/updated/deleted within Netbox
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_ipam import (
    NetboxIpamModule,
    NB_ROUTE_TARGETS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    tenant=dict(required=False, type="raw"),
                    description=dict(required=False, type="str"),
                    tags=dict(required=False, type="list", elements='str'),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )

    module = NetboxAnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    netbox_route_target = NetboxIpamModule(module, NB_ROUTE_TARGETS)
    netbox_route_target.run()


if __name__ == "__main__":  # pragma: no cover
    main()
