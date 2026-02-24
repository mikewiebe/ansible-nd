#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Mike Wiebe (@mwiebe) <mwiebe@cisco.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
# pylint: disable=wrong-import-position

from __future__ import absolute_import, annotations, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

"""
Ansible module for managing iBGP VXLAN fabrics via Nexus Dashboard.
"""

DOCUMENTATION = r"""
---
module: nd_manage_fabric
short_description: Manage iBGP VXLAN fabrics via Nexus Dashboard
description:
- Manage the lifecycle of iBGP VXLAN fabrics using Nexus Dashboard Fabric Controller (NDFC).
- Create, update, or delete fabric configurations using comprehensive Pydantic models.
- Support for multiple states including merged, replaced, overridden, and deleted.
- Idempotent operations with proper change detection and error handling.
version_added: "1.4.0"
author:
- Mike Wiebe (@mwiebe)
options:
  state:
    description:
    - The desired state of the fabric configuration.
    - C(merged) creates new fabrics or updates existing ones with provided parameters.
    - C(replaced) replaces the entire fabric configuration with the provided parameters.
    - C(overridden) replaces all fabrics with only the provided configurations.
    - C(deleted) removes the specified fabrics.
    - C(query) retrieves fabric information without making changes.
    type: str
    choices: [ merged, replaced, overridden, deleted, query ]
    default: merged
  config:
    description:
    - List of fabric configurations to be created, updated, or deleted.
    - Required when C(state) is C(merged), C(replaced), or C(overridden).
    - Optional when C(state) is C(deleted) (if not provided, deletes all fabrics).
    - Each fabric configuration must contain at minimum C(name) and C(category).
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name of the fabric.
        - Must be unique within the Nexus Dashboard.
        type: str
        required: true
      category:
        description:
        - Category of the fabric.
        - Must be "fabric" for standard VXLAN fabrics.
        type: str
        choices: [ fabric ]
        default: fabric
      security_domain:
        description:
        - Security domain for the fabric.
        type: str
        default: all
      location:
        description:
        - Geographic location of the fabric.
        type: dict
        suboptions:
          latitude:
            description:
            - Latitude coordinate (-90 to 90).
            type: float
            required: true
          longitude:
            description:
            - Longitude coordinate (-180 to 180).
            type: float
            required: true
      license_tier:
        description:
        - License tier for the fabric.
        type: str
        choices: [ essentials, premier ]
        default: essentials
      alert_suspend:
        description:
        - Alert suspension setting for the fabric.
        type: str
        choices: [ enabled, disabled ]
        default: disabled
      telemetry_collection:
        description:
        - Enable or disable telemetry collection.
        type: bool
        default: false
      management:
        description:
        - Fabric management configuration.
        - Required for fabric creation.
        type: dict
        suboptions:
          type:
            description:
            - Type of fabric management protocol.
            - Currently only supports iBGP VXLAN.
            type: str
            choices: [ vxlanIbgp ]
            required: true
          bgp_asn:
            description:
            - BGP Autonomous System Number for the fabric.
            - Must be a string representation of a valid ASN.
            type: str
            required: true
          site_id:
            description:
            - Site identifier for the fabric.
            - Must match the BGP ASN format.
            type: str
            required: true
          bgp_loopback_ip_range:
            description:
            - IP range for BGP loopback interfaces.
            type: str
            default: "10.2.0.0/22"
          nve_loopback_ip_range:
            description:
            - IP range for NVE loopback interfaces.
            type: str
            default: "10.3.0.0/22"
          anycast_rendezvous_point_ip_range:
            description:
            - IP range for anycast rendezvous point interfaces.
            type: str
            default: "10.254.254.0/24"
          intra_fabric_subnet_range:
            description:
            - IP range for intra-fabric subnets.
            type: str
            default: "10.4.0.0/16"
          l2_vni_range:
            description:
            - VNI range for L2 networks.
            type: str
            default: "30000-49000"
          l3_vni_range:
            description:
            - VNI range for L3 networks.
            type: str
            default: "50000-59000"
          network_vlan_range:
            description:
            - VLAN range for networks.
            type: str
            default: "2300-2999"
          vrf_vlan_range:
            description:
            - VLAN range for VRFs.
            type: str
            default: "2000-2299"
          overlay_mode:
            description:
            - Overlay configuration mode.
            type: str
            choices: [ cli, configProfile ]
            default: cli
          replication_mode:
            description:
            - Multicast replication mode.
            type: str
            choices: [ multicast, ingress ]
            default: multicast
          link_state_routing_protocol:
            description:
            - Underlay routing protocol.
            type: str
            choices: [ ospf, isis ]
            default: ospf
          fabric_mtu:
            description:
            - Maximum Transmission Unit for the fabric.
            type: int
            default: 9216
          vpc_peer_keep_alive_option:
            description:
            - VPC peer keep-alive option.
            type: str
            choices: [ loopback, management ]
            default: loopback
          bgp_authentication:
            description:
            - Enable BGP authentication.
            type: bool
            default: false
          bfd:
            description:
            - Enable Bidirectional Forwarding Detection.
            type: bool
            default: false
  output_level:
    description:
    - Influence the output of this module.
    - C(normal) provides standard module output.
    - C(info) provides additional informational output.
    - C(debug) provides detailed debugging information.
    type: str
    choices: [ debug, info, normal ]
    default: normal
extends_documentation_fragment:
- cisco.nd.modules
- cisco.nd.check_mode
"""

EXAMPLES = r"""
# Create a simple iBGP VXLAN fabric
- name: Create iBGP VXLAN fabric
  cisco.nd.nd_manage_fabric:
    state: merged
    config:
      - name: Fabric_VXLAN_iBGP
        category: fabric
        security_domain: all
        location:
          latitude: 37.7749
          longitude: -122.4194
        management:
          type: vxlanIbgp
          bgp_asn: "65001"
          site_id: "65001"

# Create multiple fabrics with custom settings
- name: Create multiple iBGP VXLAN fabrics
  cisco.nd.nd_manage_fabric:
    state: merged
    config:
      - name: Production_Fabric
        category: fabric
        license_tier: premier
        location:
          latitude: 37.7749
          longitude: -122.4194
        management:
          type: vxlanIbgp
          bgp_asn: "65100"
          site_id: "65100"
          replication_mode: multicast
          overlay_mode: cli
          fabric_mtu: 9216
      - name: Development_Fabric
        category: fabric
        license_tier: essentials
        location:
          latitude: 37.4419
          longitude: -122.143
        management:
          type: vxlanIbgp
          bgp_asn: "65200"
          site_id: "65200"

# Update existing fabric configuration
- name: Update fabric configuration
  cisco.nd.nd_manage_fabric:
    state: replaced
    config:
      - name: Fabric_VXLAN_iBGP
        category: fabric
        license_tier: premier
        management:
          type: vxlanIbgp
          bgp_asn: "65001"
          site_id: "65001"
          fabric_mtu: 1500

# Delete specific fabrics
- name: Delete fabrics
  cisco.nd.nd_manage_fabric:
    state: deleted
    config:
      - name: Fabric_VXLAN_iBGP
      - name: Development_Fabric

# Query fabric information
- name: Query fabric details
  cisco.nd.nd_manage_fabric:
    state: query
    config:
      - name: Fabric_VXLAN_iBGP

# Replace all fabrics (delete existing, create new)
- name: Override all fabrics
  cisco.nd.nd_manage_fabric:
    state: overridden
    config:
      - name: New_Production_Fabric
        category: fabric
        management:
          type: vxlanIbgp
          bgp_asn: "65300"
          site_id: "65300"
"""

RETURN = r"""
changed:
  description: Whether any changes were made
  returned: always
  type: bool
  sample: true
failed:
  description: Whether the operation failed
  returned: always
  type: bool
  sample: false
diff:
  description: List of differences between desired and actual state
  returned: always
  type: list
  elements: dict
  sample:
    - operation: "create"
      fabric_name: "Fabric_VXLAN_iBGP"
      before: {}
      after:
        name: "Fabric_VXLAN_iBGP"
        category: "fabric"
        management:
          type: "vxlanIbgp"
          bgp_asn: "65001"
response:
  description: List of API responses from Nexus Dashboard
  returned: always
  type: list
  elements: dict
  sample:
    - RETURN_CODE: 200
      METHOD: "POST"
      REQUEST_PATH: "/api/v1/manage/fabrics"
      MESSAGE: "OK"
      DATA: {}
result:
  description: List of operation results
  returned: always
  type: list
  elements: dict
  sample:
    - success: true
      found: true
      fabric_name: "Fabric_VXLAN_iBGP"
metadata:
  description: List of operation metadata
  returned: always
  type: list
  elements: dict
  sample:
    - action: "create_fabric"
      state: "merged"
      fabric_name: "Fabric_VXLAN_iBGP"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nd.plugins.module_utils.enums import HttpVerbEnum, OperationType
from ansible_collections.cisco.nd.plugins.module_utils.ep.ep_api_v1_manage_fabrics import (
    EpApiV1ManageFabricsDelete,
    EpApiV1ManageFabricsGet,
    EpApiV1ManageFabricsListGet,
    EpApiV1ManageFabricsPost,
    EpApiV1ManageFabricsPut,
)
from ansible_collections.cisco.nd.plugins.module_utils.log import Log
from ansible_collections.cisco.nd.plugins.module_utils.models.manage_fabric import (
    FabricModel,
    FabricDeleteModel,
)
from ansible_collections.cisco.nd.plugins.module_utils.nd_v2 import (
    NDModule,
    NDModuleError,
    nd_argument_spec,
)
from ansible_collections.cisco.nd.plugins.module_utils.results import Results


class NDFabricManager:
    """
    # Summary

    Manage iBGP VXLAN fabric lifecycle operations via Nexus Dashboard.

    Provides methods for creating, updating, querying, and deleting fabrics
    using Pydantic models for validation and the NDModule framework for
    API communication.
    """

    def __init__(self, module: AnsibleModule):
        """
        # Summary

        Initialize the fabric manager with Ansible module.

        ## Parameters

        - module: Ansible module instance

        ## Raises

        - `NDModuleError` if initialization fails
        """
        self.module = module
        self.results = Results()
        self.results.state = module.params["state"]
        self.results.check_mode = module.check_mode
        self.nd = NDModule(module)

    def _query_fabric(self, fabric_name: str) -> dict:
        """
        # Summary

        Query a specific fabric and return the response data.

        ## Parameters

        - fabric_name: Name of the fabric to query

        ## Returns

        - Dictionary containing fabric data or empty dict if not found

        ## Raises

        - `NDModuleError` on API request failure
        """
        ep = EpApiV1ManageFabricsGet()
        ep.fabric_name = fabric_name

        self.results.action = "query_fabric"
        self.results.operation_type = OperationType.QUERY

        try:
            self.nd.request(ep.path, ep.verb)
            response = self.nd.rest_send.response_current
            result = self.nd.rest_send.result_current

            self.results.response_current = response
            self.results.result_current = result
            self.results.diff_current = {}
            self.results.register_task_result()

            if result.get("found", False):
                return response.get("DATA", {})
            return {}

        except NDModuleError:
            # Fabric not found - return empty dict
            return {}

    def _list_all_fabrics(self) -> list:
        """
        # Summary

        List all fabrics in the system.

        ## Returns

        - List of fabric dictionaries

        ## Raises

        - `NDModuleError` on API request failure
        """
        ep = EpApiV1ManageFabricsListGet()
        ep.endpoint_params.category = "fabric"

        self.nd.request(ep.path, ep.verb)
        response = self.nd.rest_send.response_current

        fabrics_data = response.get("DATA", {})
        if isinstance(fabrics_data, dict) and "fabrics" in fabrics_data:
            return fabrics_data["fabrics"]
        return []

    def _create_fabric(self, fabric_config: dict) -> None:
        """
        # Summary

        Create a new fabric using Pydantic model validation.

        ## Parameters

        - fabric_config: Fabric configuration dictionary

        ## Raises

        - `NDModuleError` on API request failure
        - `ValueError` on invalid fabric configuration
        """
        # Validate and generate API payload using Pydantic model
        try:
            fabric_model = FabricModel(**fabric_config)
            payload = fabric_model.model_dump(by_alias=True, exclude_none=True)
        except Exception as error:
            raise NDModuleError(f"Invalid fabric configuration: {error}") from error

        ep = EpApiV1ManageFabricsPost()

        self.results.action = "create_fabric"
        self.results.operation_type = OperationType.CREATE

        self.nd.request(ep.path, ep.verb, data=payload)

        response = self.nd.rest_send.response_current
        result = self.nd.rest_send.result_current

        self.results.response_current = response
        self.results.result_current = result
        self.results.diff_current = {
            "before": {},
            "after": payload,
            "operation": "create",
            "fabric_name": fabric_config["name"]
        }
        self.results.register_task_result()

    def _update_fabric(self, fabric_name: str, fabric_config: dict) -> None:
        """
        # Summary

        Update an existing fabric using Pydantic model validation.

        ## Parameters

        - fabric_name: Name of the fabric to update
        - fabric_config: Updated fabric configuration dictionary

        ## Raises

        - `NDModuleError` on API request failure
        - `ValueError` on invalid fabric configuration
        """
        # Get current fabric state for diff
        current_fabric = self._query_fabric(fabric_name)

        # Validate and generate API payload using Pydantic model
        try:
            fabric_model = FabricModel(**fabric_config)
            payload = fabric_model.model_dump(by_alias=True, exclude_none=True)
        except Exception as error:
            raise NDModuleError(f"Invalid fabric configuration: {error}") from error

        ep = EpApiV1ManageFabricsPut()
        ep.fabric_name = fabric_name

        self.results.action = "update_fabric"
        self.results.operation_type = OperationType.UPDATE

        self.nd.request(ep.path, ep.verb, data=payload)

        response = self.nd.rest_send.response_current
        result = self.nd.rest_send.result_current

        self.results.response_current = response
        self.results.result_current = result
        self.results.diff_current = {
            "before": current_fabric,
            "after": payload,
            "operation": "update",
            "fabric_name": fabric_name
        }
        self.results.register_task_result()

    def _delete_fabric(self, fabric_name: str) -> None:
        """
        # Summary

        Delete a fabric by name.

        ## Parameters

        - fabric_name: Name of the fabric to delete

        ## Raises

        - `NDModuleError` on API request failure
        """
        # Get current fabric state for diff
        current_fabric = self._query_fabric(fabric_name)

        if not current_fabric:
            # Fabric doesn't exist - nothing to delete
            return

        ep = EpApiV1ManageFabricsDelete()
        ep.fabric_name = fabric_name

        self.results.action = "delete_fabric"
        self.results.operation_type = OperationType.DELETE

        self.nd.request(ep.path, ep.verb)

        response = self.nd.rest_send.response_current
        result = self.nd.rest_send.result_current

        self.results.response_current = response
        self.results.result_current = result
        self.results.diff_current = {
            "before": current_fabric,
            "after": {},
            "operation": "delete",
            "fabric_name": fabric_name
        }
        self.results.register_task_result()

    def process_state_merged(self, config: list) -> None:
        """
        # Summary

        Process merged state - create new fabrics or update existing ones.

        ## Parameters

        - config: List of fabric configurations

        ## Raises

        - `NDModuleError` on API request failure
        """
        for fabric_config in config:
            fabric_name = fabric_config["name"]
            existing_fabric = self._query_fabric(fabric_name)

            if existing_fabric:
                self._update_fabric(fabric_name, update_config)
            else:
                # Create new fabric
                self._create_fabric(fabric_config)

    def process_state_replaced(self, config: list) -> None:
        """
        # Summary

        Process replaced state - replace entire fabric configurations.

        ## Parameters

        - config: List of fabric configurations

        ## Raises

        - `NDModuleError` on API request failure
        """
        for fabric_config in config:
            fabric_name = fabric_config["name"]
            existing_fabric = self._query_fabric(fabric_name)

            if existing_fabric:
                self._update_fabric(fabric_name, update_config)
            else:
                # Create new fabric
                self._create_fabric(fabric_config)

    def process_state_overridden(self, config: list) -> None:
        """
        # Summary

        Process overridden state - replace all fabrics with provided configurations.

        ## Parameters

        - config: List of fabric configurations

        ## Raises

        - `NDModuleError` on API request failure
        """
        # Get list of existing fabrics
        existing_fabrics = self._list_all_fabrics()
        existing_names = {fabric["name"] for fabric in existing_fabrics}

        # Get names of fabrics to keep
        desired_names = {fabric_config["name"] for fabric_config in config}

        # Delete fabrics not in desired state
        for fabric_name in existing_names - desired_names:
            self._delete_fabric(fabric_name)

        # Create or update desired fabrics
        for fabric_config in config:
            fabric_name = fabric_config["name"]
            if fabric_name in existing_names:
                self._update_fabric(fabric_name, update_config)
            else:
                self._create_fabric(fabric_config)

    def process_state_deleted(self, config: list) -> None:
        """
        # Summary

        Process deleted state - delete specified fabrics.

        ## Parameters

        - config: List of fabric configurations (only name is required)

        ## Raises

        - `NDModuleError` on API request failure
        """
        if not config:
            # Delete all fabrics
            existing_fabrics = self._list_all_fabrics()
            for fabric in existing_fabrics:
                self._delete_fabric(fabric["name"])
        else:
            # Delete specified fabrics
            for fabric_config in config:
                fabric_name = fabric_config["name"]
                self._delete_fabric(fabric_name)

    def process_state_query(self, config: list) -> None:
        """
        # Summary

        Process query state - retrieve fabric information.

        ## Parameters

        - config: List of fabric configurations (only name is required)

        ## Raises

        - `NDModuleError` on API request failure
        """
        if not config:
            # Query all fabrics
            existing_fabrics = self._list_all_fabrics()
            for fabric in existing_fabrics:
                self._query_fabric(fabric["name"])
        else:
            # Query specified fabrics
            for fabric_config in config:
                fabric_name = fabric_config["name"]
                self._query_fabric(fabric_name)


def main():
    """
    # Summary

    Main entry point for the nd_manage_fabric module.

    Handles argument parsing, state processing, and result formatting
    for iBGP VXLAN fabric management operations.

    ## Raises

    - None
    """
    # Define argument specification
    argument_spec = nd_argument_spec()
    argument_spec.update(
        state=dict(
            type="str",
            default="merged",
            choices=["merged", "replaced", "overridden", "deleted", "query"]
        ),
        config=dict(type="list", elements="dict", default=[]),
    )

    # Define required parameters based on state
    required_if = [
        ["state", "merged", ["config"]],
        ["state", "replaced", ["config"]],
        ["state", "overridden", ["config"]],
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    # Initialize logging
    try:
        log = Log()
        log.commit()
    except ValueError as error:
        module.fail_json(msg=str(error))

    # Get module parameters
    state = module.params["state"]
    config = module.params["config"]
    output_level = module.params.get("output_level", "normal")

    # Initialize fabric manager
    try:
        fabric_manager = NDFabricManager(module)

        # Process based on state
        if state == "merged":
            fabric_manager.process_state_merged(config)
        elif state == "replaced":
            fabric_manager.process_state_replaced(config)
        elif state == "overridden":
            fabric_manager.process_state_overridden(config)
        elif state == "deleted":
            fabric_manager.process_state_deleted(config)
        elif state == "query":
            fabric_manager.process_state_query(config)

        # Build final result
        fabric_manager.results.build_final_result()
        final_result = fabric_manager.results.final_result

        # Add debug information if requested
        if output_level == "debug":
            final_result["debug_info"] = {
                "method": fabric_manager.nd.method,
                "path": fabric_manager.nd.path,
                "status": fabric_manager.nd.status,
                "url": fabric_manager.nd.url,
                "state": state,
                "config_count": len(config),
            }

        # Check for failures
        if True in fabric_manager.results.failed:
            module.fail_json(**final_result)

        module.exit_json(**final_result)

    except NDModuleError as error:
        try:
            fabric_manager.results.response_current = fabric_manager.nd.rest_send.response_current
            fabric_manager.results.result_current = fabric_manager.nd.rest_send.result_current
        except (ValueError, AttributeError):
            fabric_manager.results.response_current = {
                "RETURN_CODE": error.status if error.status else -1,
                "MESSAGE": error.msg,
                "DATA": error.response_payload if error.response_payload else {},
            }
            fabric_manager.results.result_current = {
                "success": False,
                "found": False,
            }

        fabric_manager.results.diff_current = {}
        fabric_manager.results.register_task_result()
        fabric_manager.results.build_final_result()
        final_result = fabric_manager.results.final_result

        # Add required msg field for fail_json
        final_result["msg"] = str(error)

        if output_level == "debug":
            final_result["error_details"] = error.to_dict()

        module.fail_json(**final_result)

    except (TypeError, ValueError) as error:
        module.fail_json(msg=str(error))


if __name__ == "__main__":
    main()