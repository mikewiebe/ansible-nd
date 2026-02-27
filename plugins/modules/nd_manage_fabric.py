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

import inspect
import logging

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
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"nd.{self.class_name}")

        self.module = module
        self.results = Results()
        self.results.state = module.params["state"]
        self.results.check_mode = module.check_mode
        self.nd = NDModule(module)

        msg = f"ENTERED {self.class_name}(): "
        msg += f"state: {self.results.state}, "
        msg += f"check_mode: {self.results.check_mode}"
        self.log.debug(msg)

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
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with fabric_name: {fabric_name}"
        self.log.debug(msg)

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
                self.log.debug(f"Fabric {fabric_name} found in current state")
                return response.get("DATA", {})
            else:
                self.log.debug(f"Fabric {fabric_name} not found in current state")
                return {}

        except NDModuleError:
            # Fabric not found - return empty dict
            self.log.debug(f"Fabric {fabric_name} not found (caught NDModuleError)")
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
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name}"
        self.log.debug(msg)

        ep = EpApiV1ManageFabricsListGet()
        ep.endpoint_params.category = "fabric"

        self.nd.request(ep.path, ep.verb)
        response = self.nd.rest_send.response_current

        fabrics_data = response.get("DATA", {})
        if isinstance(fabrics_data, dict) and "fabrics" in fabrics_data:
            fabrics_list = fabrics_data["fabrics"]
            self.log.debug(f"Found {len(fabrics_list)} fabrics in system")
            return fabrics_list
        else:
            self.log.debug("No fabrics found in system")
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
        method_name = inspect.stack()[0][3]
        fabric_name = fabric_config.get("name", "unknown")
        msg = f"ENTERED: {self.class_name}.{method_name} with fabric_name: {fabric_name}"
        self.log.debug(msg)

        # Validate and generate API payload using Pydantic model
        try:
            fabric_model = FabricModel(**fabric_config)
            payload = fabric_model.model_dump(by_alias=True, exclude_none=True)
            self.log.debug(f"Generated payload for fabric {fabric_name}")
        except Exception as error:
            self.log.error(f"Invalid fabric configuration for {fabric_name}: {error}")
            raise NDModuleError(f"Invalid fabric configuration: {error}") from error

        self._create_fabric_with_payload(payload)

    def _create_fabric_with_payload(self, payload: dict) -> None:
        """
        # Summary

        Create a new fabric with a pre-prepared payload.

        ## Parameters

        - payload: Pre-validated payload dictionary

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        fabric_name = payload.get("name", "unknown")
        msg = f"ENTERED: {self.class_name}.{method_name} with fabric_name: {fabric_name}"
        self.log.debug(msg)

        ep = EpApiV1ManageFabricsPost()

        self.results.action = "create_fabric"
        self.results.operation_type = OperationType.CREATE

        self.log.debug(f"Creating fabric {fabric_name} with POST request")
        self.nd.request(ep.path, ep.verb, data=payload)

        response = self.nd.rest_send.response_current
        result = self.nd.rest_send.result_current

        self.results.response_current = response
        self.results.result_current = result
        self.results.diff_current = {
            "before": {},
            "after": payload,
            "operation": "create",
            "fabric_name": fabric_name
        }
        self.results.register_task_result()

        if result.get("success", False):
            self.log.debug(f"Successfully created fabric {fabric_name}")
        else:
            self.log.error(f"Failed to create fabric {fabric_name}: {result}")

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
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with fabric_name: {fabric_name}"
        self.log.debug(msg)

        # Get current fabric state for diff
        current_fabric = self._query_fabric(fabric_name)

        # Validate and generate API payload using Pydantic model
        try:
            fabric_model = FabricModel(**fabric_config)
            payload = fabric_model.model_dump(by_alias=True, exclude_none=True)
            self.log.debug(f"Generated payload for fabric {fabric_name} update")
        except Exception as error:
            self.log.error(f"Invalid fabric configuration for {fabric_name}: {error}")
            raise NDModuleError(f"Invalid fabric configuration: {error}") from error

        self._update_fabric_with_payload(fabric_name, payload, current_fabric)

    def _update_fabric_with_payload(self, fabric_name: str, payload: dict, current_fabric: dict) -> None:
        """
        # Summary

        Update an existing fabric with a pre-prepared payload.

        ## Parameters

        - fabric_name: Name of the fabric to update
        - payload: Pre-validated payload dictionary
        - current_fabric: Current fabric state for diff generation

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with fabric_name: {fabric_name}"
        self.log.debug(msg)

        ep = EpApiV1ManageFabricsPut()
        ep.fabric_name = fabric_name

        self.results.action = "update_fabric"
        self.results.operation_type = OperationType.UPDATE

        self.log.debug(f"Updating fabric {fabric_name} with PUT request")
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

        if result.get("success", False):
            self.log.debug(f"Successfully updated fabric {fabric_name}")
        else:
            self.log.error(f"Failed to update fabric {fabric_name}: {result}")

    def _delete_fabric(self, fabric_name: str) -> None:
        """
        # Summary

        Delete a fabric by name.

        ## Parameters

        - fabric_name: Name of the fabric to delete

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with fabric_name: {fabric_name}"
        self.log.debug(msg)

        # Get current fabric state for diff
        current_fabric = self._query_fabric(fabric_name)

        if not current_fabric:
            # Fabric doesn't exist - nothing to delete
            self.log.debug(f"Fabric {fabric_name} does not exist, skipping deletion")
            return

        ep = EpApiV1ManageFabricsDelete()
        ep.fabric_name = fabric_name

        self.results.action = "delete_fabric"
        self.results.operation_type = OperationType.DELETE

        self.log.debug(f"Deleting fabric {fabric_name} with DELETE request")
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

        if result.get("success", False):
            self.log.debug(f"Successfully deleted fabric {fabric_name}")
        else:
            self.log.error(f"Failed to delete fabric {fabric_name}: {result}")

    def _fabrics_equal(self, fabric1: dict, fabric2: dict) -> bool:
        """
        # Summary

        Compare two fabric dictionaries for equality.

        ## Parameters

        - fabric1: First fabric configuration dictionary
        - fabric2: Second fabric configuration dictionary

        ## Returns

        - Boolean indicating whether the fabrics are equal

        ## Raises

        - None
        """
        method_name = inspect.stack()[0][3]

        if not fabric1 and not fabric2:
            self.log.debug(f"{method_name}: Both fabrics are None/empty - equal")
            return True
        if not fabric1 or not fabric2:
            self.log.debug(f"{method_name}: One fabric is None/empty - not equal")
            return False

        # For fabric comparison, we need to handle the fact that API responses
        # contain additional fields not defined in our Pydantic model.
        # We'll use a more flexible comparison approach.

        try:
            # First, try to validate the desired fabric (fabric2) with the model
            # This should work since it's coming from user configuration
            if isinstance(fabric2, dict):
                fabric_model = FabricModel(**fabric2)
                normalized_fabric2 = fabric_model.model_dump(by_alias=True, exclude_none=True)
            else:
                normalized_fabric2 = fabric2

            # For the current fabric (fabric1), we can't use strict model validation
            # because it contains extra fields from the API response.
            # Instead, we'll normalize it by extracting only the fields that exist in fabric2
            normalized_fabric1 = self._normalize_api_response(fabric1, normalized_fabric2)

            # Now compare the normalized fabrics
            equal = normalized_fabric1 == normalized_fabric2
            self.log.debug(f"{method_name}: Fabric comparison result: {equal}")
            return equal

        except Exception as error:
            # Fallback to direct dictionary comparison
            self.log.debug(f"{method_name}: Model validation failed ({error}), using direct comparison")
            return fabric1 == fabric2

    def _normalize_api_response(self, api_response: dict, reference_config: dict) -> dict:
        """
        # Summary

        Normalize an API response to match the structure of a reference configuration.

        This method extracts only the fields that exist in the reference configuration
        from the API response, and applies any necessary transformations to handle
        differences in field naming or format between API responses and user configuration.

        ## Parameters

        - api_response: Dictionary from API response (may contain extra fields)
        - reference_config: Dictionary with desired structure (usually from user config)

        ## Returns

        - Dictionary containing only matching fields from api_response

        ## Raises

        - None
        """
        if not api_response or not reference_config:
            return api_response or {}

        normalized = {}

        for key, ref_value in reference_config.items():
            if key in api_response:
                api_value = api_response[key]

                # Handle nested dictionaries recursively
                if isinstance(ref_value, dict) and isinstance(api_value, dict):
                    normalized[key] = self._normalize_api_response(api_value, ref_value)
                else:
                    # Handle specific field transformations
                    normalized[key] = self._normalize_field_value(key, api_value)
            # If the field doesn't exist in API response, we don't include it
            # This handles cases where user config has new fields not yet in the API response

        return normalized

    def _normalize_field_value(self, field_name: str, api_value):
        """
        # Summary

        Normalize a specific field value from API response to match expected format.

        ## Parameters

        - field_name: Name of the field being normalized
        - api_value: Value from API response

        ## Returns

        - Normalized value

        ## Raises

        - None
        """
        # Handle specific field transformations that are known to differ
        # between API responses and user configuration

        # Handle overlayMode field: API returns 'config-profile', model expects 'configProfile'
        if field_name == "overlayMode" and api_value == "config-profile":
            return "configProfile"

        # Add other known transformations here as needed
        # if field_name == "someOtherField" and api_value == "api_format":
        #     return "expected_format"

        return api_value

    def _calculate_fabric_diff(self, current: dict, desired: dict) -> dict:
        """
        # Summary

        Calculate the differences between current and desired fabric states.

        ## Parameters

        - current: Current fabric configuration dictionary
        - desired: Desired fabric configuration dictionary

        ## Returns

        - Dictionary containing only the changed values from desired state

        ## Raises

        - None
        """
        method_name = inspect.stack()[0][3]

        if not current:
            # If no current state, return the complete desired state
            self.log.debug(f"{method_name}: No current state, returning complete desired state")
            return desired

        try:
            # Validate and normalize the desired configuration
            desired_model = FabricModel(**desired)
            desired_dict = desired_model.model_dump(by_alias=True, exclude_none=True)

            # Normalize the current fabric data to match the desired structure
            # This handles extra fields in API responses and field format differences
            current_dict = self._normalize_api_response(current, desired_dict)

            # Calculate only the changed values
            diff_dict = {}
            self._deep_diff_extract(current_dict, desired_dict, diff_dict)

            result = diff_dict if diff_dict else desired_dict
            self.log.debug(f"{method_name}: Calculated diff with {len(result)} changed fields")
            return result

        except Exception as error:
            # Fallback to desired state if model validation fails
            self.log.debug(f"{method_name}: Model validation failed ({error}), returning desired state")
            return desired

    def _deep_diff_extract(self, current: dict, desired: dict, result: dict) -> None:
        """
        # Summary

        Recursively extract differences between current and desired dictionaries.

        ## Parameters

        - current: Current dictionary state
        - desired: Desired dictionary state
        - result: Dictionary to store the differences

        ## Returns

        - None (modifies result dictionary in place)

        ## Raises

        - None
        """
        for key, desired_value in desired.items():
            if key not in current:
                # New key - add it
                result[key] = desired_value
            elif isinstance(desired_value, dict) and isinstance(current.get(key), dict):
                # Nested dictionary - recurse
                nested_result = {}
                self._deep_diff_extract(current[key], desired_value, nested_result)
                if nested_result:
                    result[key] = nested_result
            elif current[key] != desired_value:
                # Value changed - add the new value
                result[key] = desired_value

    def _should_skip_fabric(self, current: dict, desired: dict) -> bool:
        """
        # Summary

        Determine if a fabric should be skipped (no changes needed).

        ## Parameters

        - current: Current fabric configuration dictionary
        - desired: Desired fabric configuration dictionary

        ## Returns

        - Boolean indicating whether the fabric should be skipped

        ## Raises

        - None
        """
        skip = self._fabrics_equal(current, desired)
        fabric_name = desired.get("name", "unknown") if desired else "unknown"

        if skip:
            self.log.debug(f"Fabric {fabric_name} is already in desired state, skipping")
        else:
            self.log.debug(f"Fabric {fabric_name} requires changes")

        return skip

    def _create_merged_payload(self, current: dict, desired: dict) -> dict:
        """
        # Summary

        Create an optimized payload for merged state operations.

        ## Parameters

        - current: Current fabric configuration dictionary
        - desired: Desired fabric configuration dictionary

        ## Returns

        - Dictionary containing optimized payload with only changed values

        ## Raises

        - None
        """
        method_name = inspect.stack()[0][3]
        fabric_name = desired.get("name", "unknown")
        self.log.debug(f"{method_name}: Creating merged payload for fabric {fabric_name}")

        # For merged operations, we want to preserve existing values
        # and only send the changes
        diff_payload = self._calculate_fabric_diff(current, desired)

        # Ensure we always include the fabric name
        if 'name' not in diff_payload and 'name' in desired:
            diff_payload['name'] = desired['name']

        self.log.debug(f"{method_name}: Generated merged payload for {fabric_name} with {len(diff_payload)} fields")
        return diff_payload

    def _create_replaced_payload(self, desired: dict) -> dict:
        """
        # Summary

        Create a complete payload for replaced state operations.

        ## Parameters

        - desired: Desired fabric configuration dictionary

        ## Returns

        - Dictionary containing complete fabric configuration

        ## Raises

        - None
        """
        method_name = inspect.stack()[0][3]
        fabric_name = desired.get("name", "unknown")
        self.log.debug(f"{method_name}: Creating replaced payload for fabric {fabric_name}")

        # For replaced operations, we send the complete desired configuration
        try:
            fabric_model = FabricModel(**desired)
            payload = fabric_model.model_dump(by_alias=True, exclude_none=True)
            self.log.debug(f"{method_name}: Generated replaced payload for {fabric_name} with {len(payload)} fields")
            return payload
        except Exception as error:
            self.log.error(f"{method_name}: Invalid fabric configuration for {fabric_name}: {error}")
            raise NDModuleError(f"Invalid fabric configuration: {error}") from error

    def process_state_merged(self, config: list) -> None:
        """
        # Summary

        Process merged state - create new fabrics or intelligently update existing ones.

        This implementation uses smart merging logic that:
        - Compares current vs desired state to detect changes
        - Preserves existing values not specified in desired state
        - Only sends changed/new values to minimize API calls
        - Skips fabrics that are already in desired state

        ## Parameters

        - config: List of fabric configurations

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with {len(config)} fabric configurations"
        self.log.debug(msg)

        for fabric_config in config:
            fabric_name = fabric_config["name"]
            self.log.debug(f"Processing fabric {fabric_name} for merged state")
            current_fabric = self._query_fabric(fabric_name)

            # Skip if fabric is already in desired state
            if self._should_skip_fabric(current_fabric, fabric_config):
                continue

            if not current_fabric:
                # Create new fabric
                self.log.debug(f"Creating new fabric {fabric_name}")
                self._create_fabric(fabric_config)
            else:
                # Update existing fabric with optimized payload
                self.log.debug(f"Updating existing fabric {fabric_name} with merged payload")
                merged_payload = self._create_merged_payload(current_fabric, fabric_config)
                self._update_fabric_with_payload(fabric_name, merged_payload, current_fabric)

        self.log.debug(f"Completed {method_name} processing")

    def process_state_replaced(self, config: list) -> None:
        """
        # Summary

        Process replaced state - completely replace fabric configurations.

        This implementation uses full replacement logic that:
        - Always sends complete desired configuration regardless of current state
        - Uses full model validation and dumps for consistency
        - Creates new fabrics if they don't exist
        - Completely replaces existing fabrics with desired configuration

        ## Parameters

        - config: List of fabric configurations

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with {len(config)} fabric configurations"
        self.log.debug(msg)

        for fabric_config in config:
            fabric_name = fabric_config["name"]
            self.log.debug(f"Processing fabric {fabric_name} for replaced state")
            current_fabric = self._query_fabric(fabric_name)

            # Skip if fabric is already in exact desired state
            if self._should_skip_fabric(current_fabric, fabric_config):
                continue

            # Use complete desired configuration for replacement
            replaced_payload = self._create_replaced_payload(fabric_config)

            if not current_fabric:
                # Create new fabric
                self.log.debug(f"Creating new fabric {fabric_name} with complete payload")
                self._create_fabric_with_payload(replaced_payload)
            else:
                # Replace existing fabric completely
                self.log.debug(f"Replacing existing fabric {fabric_name} with complete payload")
                self._update_fabric_with_payload(fabric_name, replaced_payload, current_fabric)

        self.log.debug(f"Completed {method_name} processing")

    def process_state_overridden(self, config: list) -> None:
        """
        # Summary

        Process overridden state - replace all fabrics with provided configurations.

        This implementation follows a two-phase approach:
        1. Delete fabrics that exist in current state but not in desired state
        2. Create or replace fabrics specified in desired state

        ## Parameters

        - config: List of fabric configurations

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with {len(config)} fabric configurations"
        self.log.debug(msg)

        # Get list of existing fabrics
        existing_fabrics = self._list_all_fabrics()
        existing_names = {fabric["name"] for fabric in existing_fabrics}

        # Get names of fabrics to keep
        desired_names = {fabric_config["name"] for fabric_config in config}

        self.log.debug(f"Found {len(existing_names)} existing fabrics, {len(desired_names)} desired fabrics")

        # Phase 1: Delete fabrics not in desired state
        fabrics_to_delete = existing_names - desired_names
        if fabrics_to_delete:
            self.log.debug(f"Phase 1: Deleting {len(fabrics_to_delete)} unwanted fabrics: {list(fabrics_to_delete)}")
            for fabric_name in fabrics_to_delete:
                self._delete_fabric(fabric_name)
        else:
            self.log.debug("Phase 1: No fabrics to delete")

        # Phase 2: Create or replace desired fabrics
        self.log.debug(f"Phase 2: Processing {len(config)} desired fabrics")
        for fabric_config in config:
            fabric_name = fabric_config["name"]
            current_fabric = self._query_fabric(fabric_name) if fabric_name in existing_names else {}

            # Skip if fabric is already in exact desired state
            if self._should_skip_fabric(current_fabric, fabric_config):
                continue

            # Use complete configuration for overridden operations
            overridden_payload = self._create_replaced_payload(fabric_config)

            if fabric_name in existing_names:
                # Replace existing fabric
                self.log.debug(f"Replacing existing fabric {fabric_name}")
                self._update_fabric_with_payload(fabric_name, overridden_payload, current_fabric)
            else:
                # Create new fabric
                self.log.debug(f"Creating new fabric {fabric_name}")
                self._create_fabric_with_payload(overridden_payload)

        self.log.debug(f"Completed {method_name} processing")

    def process_state_deleted(self, config: list) -> None:
        """
        # Summary

        Process deleted state - delete specified fabrics.

        ## Parameters

        - config: List of fabric configurations (only name is required)

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with config length: {len(config) if config else 0}"
        self.log.debug(msg)

        if not config:
            # Delete all fabrics
            self.log.debug("No config provided - deleting all fabrics")
            existing_fabrics = self._list_all_fabrics()
            for fabric in existing_fabrics:
                fabric_name = fabric["name"]
                self.log.debug(f"Deleting fabric {fabric_name}")
                self._delete_fabric(fabric_name)
        else:
            # Delete specified fabrics
            self.log.debug(f"Deleting {len(config)} specified fabrics")
            for fabric_config in config:
                fabric_name = fabric_config["name"]
                self.log.debug(f"Deleting fabric {fabric_name}")
                self._delete_fabric(fabric_name)

        self.log.debug(f"Completed {method_name} processing")

    def process_state_query(self, config: list) -> None:
        """
        # Summary

        Process query state - retrieve fabric information.

        ## Parameters

        - config: List of fabric configurations (only name is required)

        ## Raises

        - `NDModuleError` on API request failure
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED: {self.class_name}.{method_name} with config length: {len(config) if config else 0}"
        self.log.debug(msg)

        if not config:
            # Query all fabrics
            self.log.debug("No config provided - querying all fabrics")
            existing_fabrics = self._list_all_fabrics()
            for fabric in existing_fabrics:
                fabric_name = fabric["name"]
                self.log.debug(f"Querying fabric {fabric_name}")
                self._query_fabric(fabric_name)
        else:
            # Query specified fabrics
            self.log.debug(f"Querying {len(config)} specified fabrics")
            for fabric_config in config:
                fabric_name = fabric_config["name"]
                self.log.debug(f"Querying fabric {fabric_name}")
                self._query_fabric(fabric_name)

        self.log.debug(f"Completed {method_name} processing")


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

    # Setup main function logger
    main_logger = logging.getLogger("nd.main")

    # Get module parameters
    state = module.params["state"]
    config = module.params["config"]
    output_level = module.params.get("output_level", "normal")

    main_logger.debug(f"ENTERED main(): state={state}, config_count={len(config)}, output_level={output_level}")

    # Initialize fabric manager
    try:
        main_logger.debug("Initializing NDFabricManager")
        fabric_manager = NDFabricManager(module)

        # Process based on state
        main_logger.debug(f"Processing state: {state}")
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

        main_logger.debug("Building final results")
        # Build final result
        fabric_manager.results.build_final_result()
        final_result = fabric_manager.results.final_result

        # Add debug information if requested
        if output_level == "debug":
            main_logger.debug("Adding debug information to results")
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
            main_logger.error("Operation failed - calling fail_json")
            module.fail_json(**final_result)

        main_logger.debug("Operation completed successfully - calling exit_json")
        module.exit_json(**final_result)

    except NDModuleError as error:
        main_logger.error(f"NDModuleError caught: {error}")
        try:
            fabric_manager.results.response_current = fabric_manager.nd.rest_send.response_current
            fabric_manager.results.result_current = fabric_manager.nd.rest_send.result_current
        except (ValueError, AttributeError) as attr_error:
            main_logger.debug(f"Could not get response/result from fabric_manager: {attr_error}")
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
            main_logger.debug("Adding error details to debug info")
            final_result["error_details"] = error.to_dict()

        main_logger.error(f"Module failed with NDModuleError: {error}")
        module.fail_json(**final_result)

    except (TypeError, ValueError) as error:
        main_logger.error(f"Module failed with {type(error).__name__}: {error}")
        module.fail_json(msg=str(error))


if __name__ == "__main__":
    main()