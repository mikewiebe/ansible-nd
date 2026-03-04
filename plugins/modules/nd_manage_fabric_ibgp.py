#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Mike Wiebe (@mwiebe) <mwiebe@cisco.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, annotations, division, print_function

__metaclass__ = type
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__author__ = "Mike Wiebe"

DOCUMENTATION = """

---
module: nd_manage_fabric
short_description: Manage fabrics in Cisco Nexus Dashboard.
version_added: "1.0.0"
author: Mike Wiebe (@mikewiebe)
description:
- Create, update, delete, override, and query fabrics in Cisco Nexus Dashboard.
- Supports Pydantic model validation for fabric configurations.
- Provides utility functions for merging models and handling default values.
- Uses state-based operations with intelligent diff calculation for optimal API calls.
options:
    state:
        choices:
        - merged
        - replaced
        - deleted
        - overridden
        - query
        default: merged
        description:
        - The state of the fabric configuration after module completion.
        type: str
    config:
        description:
        - A list of fabric configuration dictionaries.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                - Name of the fabric. Must start with a letter and contain only alphanumeric characters, underscores, or hyphens.
                required: true
                type: str
            alert_suspend:
                description:
                - Alert suspension setting for the fabric.
                type: str
                default: disabled
            category:
                description:
                - Category of the fabric.
                type: str
                default: fabric
            security_domain:
                description:
                - Security domain for the fabric.
                type: str
                default: all
            location:
                description:
                - Geographic location settings for the fabric.
                type: dict
                suboptions:
                    latitude:
                        description:
                        - The latitude coordinate.
                        type: float
                        default: 0.0
                    longitude:
                        description:
                        - The longitude coordinate.
                        type: float
                        default: 0.0
            management:
                description:
                - Management configuration for the fabric.
                type: dict
                suboptions:
                    type:
                        description:
                        - Management type for the fabric.
                        type: str
                        choices:
                        - vxlanIbgp
                        - vxlanEbgp
                        - vxlanCampus
                        - aimlVxlanIbgp
                        - aimlVxlanEbgp
                        - aimlRouted
                        - routed
                        - classicLan
                        - classicLanEnhanced
                        - ipfm
                        - ipfmEnhanced
                        - externalConnectivity
                        - vxlanExternal
                        - aci
                        - meta
                        default: vxlanIbgp
                    bgp_asn:
                        description:
                        - BGP autonomous system number. Must be a valid ASN string (plain or dotted notation).
                        required: true
                        type: str
                    anycast_gateway_mac:
                        description:
                        - Anycast gateway MAC address in Cisco format (XXXX.XXXX.XXXX).
                        type: str
                        default: 2020.0000.00aa
                    replication_mode:
                        description:
                        - Replication mode for the fabric.
                        type: str
                        choices:
                        - multicast
                        - ingress
                        default: multicast
                    vrf_lite_auto_config:
                        description:
                        - VRF Lite Inter-Fabric Connection Deployment mode.
                        type: str
                        choices:
                        - manual
                        - back2Back&ToExternal
                        default: manual
                    bgp_authentication_key_type:
                        description:
                        - BGP Authentication Key Type for encryption.
                        type: str
                        choices:
                        - 3des
                        - type6
                        - type7
                        default: 3des
                    fabric_interface_type:
                        description:
                        - Fabric interface type for numbered (Point-to-Point) or unnumbered interfaces.
                        type: str
                        choices:
                        - p2p
                        - unNumbered
                        default: p2p
                    link_state_routing_protocol:
                        description:
                        - Underlay routing protocol for Spine-Leaf connectivity.
                        type: str
                        choices:
                        - ospf
                        - is-is
                        default: ospf
                    overlay_mode:
                        description:
                        - Overlay mode for VRF/Network configuration.
                        type: str
                        choices:
                        - configProfile
                        - cli
                        default: cli
                    power_redundancy_mode:
                        description:
                        - Default power supply mode for NX-OS switches.
                        type: str
                        choices:
                        - redundant
                        - combined
                        - inputSrcRedundant
                        default: redundant
                    rendezvous_point_mode:
                        description:
                        - Multicast rendezvous point mode. For IPv6 underlay, use ASM only.
                        type: str
                        choices:
                        - asm
                        - bidir
                        default: asm
                    isis_level:
                        description:
                        - IS-IS level configuration.
                        type: str
                        choices:
                        - level-1
                        - level-2
                        default: level-2
                    stp_root_option:
                        description:
                        - Protocol for configuring root bridge.
                        type: str
                        choices:
                        - rpvst+
                        - mst
                        - unmanaged
                        default: unmanaged
                    vpc_peer_keep_alive_option:
                        description:
                        - vPC peer keep alive option using loopback or management interfaces.
                        type: str
                        choices:
                        - loopback
                        - management
                        default: management
                    allow_vlan_on_leaf_tor_pairing:
                        description:
                        - Trunk allowed VLAN setting for leaf-tor pairing port-channels.
                        type: str
                        choices:
                        - none
                        - all
                        default: none
                    aiml_qos_policy:
                        description:
                        - Queuing policy based on predominant fabric link speed for AI/ML network loads.
                        type: str
                        choices:
                        - 800G
                        - 400G
                        - 100G
                        - 25G
                        default: 400G
                    greenfield_debug_flag:
                        description:
                        - Allow switch configuration to be cleared without a reload when preserveConfig is false.
                        type: str
                        choices:
                        - enable
                        - disable
                        default: disable
                    copp_policy:
                        description:
                        - Fabric wide CoPP (Control Plane Policing) policy. Customized CoPP policy should be provided when 'manual' is selected.
                        type: str
                        choices:
                        - dense
                        - lenient
                        - moderate
                        - strict
                        - manual
                        default: strict
                    # VPC and peering settings
                    vpc_layer3_peer_router:
                        description:
                        - Enable vPC layer 3 peer router functionality.
                        type: bool
                        default: true
                    vpc_peer_link_port_channel_id:
                        description:
                        - vPC peer link port channel ID.
                        type: str
                        default: "500"
                    vpc_peer_link_vlan:
                        description:
                        - vPC peer link VLAN.
                        type: str
                        default: "3600"
                    vpc_domain_id_range:
                        description:
                        - vPC domain ID range.
                        type: str
                        default: "1-1000"
                    vpc_delay_restore_timer:
                        description:
                        - vPC delay restore timer in seconds.
                        type: int
                        default: 150
                    vpc_auto_recovery_timer:
                        description:
                        - vPC auto recovery timer in seconds.
                        type: int
                        default: 360
                    vpc_tor_delay_restore_timer:
                        description:
                        - vPC ToR delay restore timer in seconds.
                        type: int
                        default: 30
                    vpc_ipv6_neighbor_discovery_sync:
                        description:
                        - Enable vPC IPv6 neighbor discovery sync.
                        type: bool
                        default: true
                    vpc_peer_link_enable_native_vlan:
                        description:
                        - Enable native VLAN on vPC peer link.
                        type: bool
                        default: false
                    fabric_vpc_qos:
                        description:
                        - Enable fabric vPC QoS.
                        type: bool
                        default: false
                    fabric_vpc_qos_policy_name:
                        description:
                        - Fabric vPC QoS policy name.
                        type: str
                        default: spine_qos_for_fabric_vpc_peering
                    fabric_vpc_domain_id:
                        description:
                        - Enable fabric vPC domain ID.
                        type: bool
                        default: false
                    # VNI and VLAN ranges
                    l3_vni_range:
                        description:
                        - Layer 3 VNI range.
                        type: str
                        default: "50000-59000"
                    l2_vni_range:
                        description:
                        - Layer 2 VNI range.
                        type: str
                        default: "30000-49000"
                    vrf_vlan_range:
                        description:
                        - VRF VLAN range.
                        type: str
                        default: "2000-2299"
                    network_vlan_range:
                        description:
                        - Network VLAN range.
                        type: str
                        default: "2300-2999"
                    service_network_vlan_range:
                        description:
                        - Service network VLAN range.
                        type: str
                        default: "3000-3199"
                    # BGP settings
                    bgp_loopback_id:
                        description:
                        - BGP loopback interface ID.
                        type: int
                        default: 0
                    bgp_loopback_ip_range:
                        description:
                        - BGP loopback IP range.
                        type: str
                        default: "10.2.0.0/22"
                    bgp_authentication:
                        description:
                        - Enable BGP authentication.
                        type: bool
                        default: false
                    auto_bgp_neighbor_description:
                        description:
                        - Enable automatic BGP neighbor description.
                        type: bool
                        default: true
                    # NVE settings
                    nve_loopback_id:
                        description:
                        - NVE loopback interface ID.
                        type: int
                        default: 1
                    nve_loopback_ip_range:
                        description:
                        - NVE loopback IP range.
                        type: str
                        default: "10.3.0.0/22"
                    nve_hold_down_timer:
                        description:
                        - NVE hold down timer in seconds.
                        type: int
                        default: 180
                    # IPv6 settings
                    underlay_ipv6:
                        description:
                        - Enable IPv6 underlay.
                        type: bool
                        default: false
                    ipv6_link_local:
                        description:
                        - Enable IPv6 link local addressing.
                        type: bool
                        default: true
                    ipv6_subnet_target_mask:
                        description:
                        - IPv6 subnet target mask length.
                        type: int
                        default: 126
                    # VRF settings
                    vrf_template:
                        description:
                        - VRF template name.
                        type: str
                        default: Default_VRF_Universal
                    vrf_extension_template:
                        description:
                        - VRF extension template name.
                        type: str
                        default: Default_VRF_Extension_Universal
                    vrf_lite_subnet_range:
                        description:
                        - VRF lite subnet range.
                        type: str
                        default: "10.33.0.0/16"
                    vrf_lite_subnet_target_mask:
                        description:
                        - VRF lite subnet target mask length.
                        type: int
                        default: 30
                    vrf_lite_ipv6_subnet_range:
                        description:
                        - VRF lite IPv6 subnet range.
                        type: str
                        default: "fd00::a33:0/112"
                    vrf_lite_ipv6_subnet_target_mask:
                        description:
                        - VRF lite IPv6 subnet target mask length.
                        type: int
                        default: 126
                    vrf_lite_macsec:
                        description:
                        - Enable VRF lite MACSec.
                        type: bool
                        default: false
                    auto_unique_vrf_lite_ip_prefix:
                        description:
                        - Enable automatic unique VRF lite IP prefix.
                        type: bool
                        default: false
                    auto_symmetric_vrf_lite:
                        description:
                        - Enable automatic symmetric VRF lite.
                        type: bool
                        default: false
                    auto_symmetric_default_vrf:
                        description:
                        - Enable automatic symmetric default VRF.
                        type: bool
                        default: false
                    auto_vrf_lite_default_vrf:
                        description:
                        - Enable automatic VRF lite default VRF.
                        type: bool
                        default: false
                    vrf_route_import_id_reallocation:
                        description:
                        - Enable VRF route import ID reallocation.
                        type: bool
                        default: false
                    per_vrf_loopback_auto_provision:
                        description:
                        - Enable per VRF loopback auto provision.
                        type: bool
                        default: false
                    per_vrf_loopback_auto_provision_ipv6:
                        description:
                        - Enable per VRF loopback auto provision for IPv6.
                        type: bool
                        default: false
                    # Network settings
                    network_template:
                        description:
                        - Network template name.
                        type: str
                        default: Default_Network_Universal
                    network_extension_template:
                        description:
                        - Network extension template name.
                        type: str
                        default: Default_Network_Extension_Universal
                    brownfield_network_name_format:
                        description:
                        - Brownfield network name format.
                        type: str
                        default: Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$
                    brownfield_skip_overlay_network_attachments:
                        description:
                        - Skip overlay network attachments in brownfield deployments.
                        type: bool
                        default: false
                    # Fabric interface and underlay settings
                    fabric_mtu:
                        description:
                        - Fabric MTU size.
                        type: int
                        default: 9216
                    l2_host_interface_mtu:
                        description:
                        - Layer 2 host interface MTU size.
                        type: int
                        default: 9216
                    target_subnet_mask:
                        description:
                        - Target subnet mask length.
                        type: int
                        default: 30
                    intra_fabric_subnet_range:
                        description:
                        - Intra-fabric subnet range.
                        type: str
                        default: "10.4.0.0/16"
                    static_underlay_ip_allocation:
                        description:
                        - Enable static underlay IP allocation.
                        type: bool
                        default: false
                    # OSPF settings
                    ospf_area_id:
                        description:
                        - OSPF area ID.
                        type: str
                        default: "0.0.0.0"
                    ospf_authentication:
                        description:
                        - Enable OSPF authentication.
                        type: bool
                        default: false
                    link_state_routing_tag:
                        description:
                        - Link state routing tag.
                        type: str
                        default: UNDERLAY
                    # ISIS settings
                    isis_area_number:
                        description:
                        - ISIS area number.
                        type: str
                        default: "0001"
                    isis_authentication:
                        description:
                        - Enable ISIS authentication.
                        type: bool
                        default: false
                    mpls_isis_area_number:
                        description:
                        - MPLS ISIS area number.
                        type: str
                        default: "0001"
                    # BFD settings
                    bfd:
                        description:
                        - Enable BFD (Bidirectional Forwarding Detection).
                        type: bool
                        default: false
                    bfd_pim:
                        description:
                        - Enable BFD for PIM.
                        type: bool
                        default: false
                    bfd_isis:
                        description:
                        - Enable BFD for ISIS.
                        type: bool
                        default: false
                    bfd_ospf:
                        description:
                        - Enable BFD for OSPF.
                        type: bool
                        default: false
                    bfd_ibgp:
                        description:
                        - Enable BFD for iBGP.
                        type: bool
                        default: false
                    bfd_authentication:
                        description:
                        - Enable BFD authentication.
                        type: bool
                        default: false
                    # Multicast settings
                    anycast_rendezvous_point_ip_range:
                        description:
                        - Anycast rendezvous point IP range.
                        type: str
                        default: "10.254.254.0/24"
                    rendezvous_point_count:
                        description:
                        - Number of rendezvous points.
                        type: int
                        default: 2
                    rendezvous_point_loopback_id:
                        description:
                        - Rendezvous point loopback interface ID.
                        type: int
                        default: 254
                    multicast_group_subnet:
                        description:
                        - Multicast group subnet.
                        type: str
                        default: "239.1.1.0/25"
                    auto_generate_multicast_group_address:
                        description:
                        - Enable automatic multicast group address generation.
                        type: bool
                        default: false
                    underlay_multicast_group_address_limit:
                        description:
                        - Underlay multicast group address limit.
                        type: int
                        default: 128
                    tenant_routed_multicast:
                        description:
                        - Enable tenant routed multicast.
                        type: bool
                        default: false
                    tenant_routed_multicast_ipv6:
                        description:
                        - Enable tenant routed multicast for IPv6.
                        type: bool
                        default: false
                    # Security and authentication
                    security_group_tag:
                        description:
                        - Enable security group tag.
                        type: bool
                        default: false
                    macsec:
                        description:
                        - Enable MACSec encryption.
                        type: bool
                        default: false
                    pim_hello_authentication:
                        description:
                        - Enable PIM hello authentication.
                        type: bool
                        default: false
                    # PTP and timing
                    ptp:
                        description:
                        - Enable PTP (Precision Time Protocol).
                        type: bool
                        default: false
                    # Management and monitoring
                    real_time_backup:
                        description:
                        - Enable real-time backup.
                        type: bool
                        default: true
                    scheduled_backup:
                        description:
                        - Enable scheduled backup.
                        type: bool
                        default: true
                    scheduled_backup_time:
                        description:
                        - Scheduled backup time in HH:MM format.
                        type: str
                        default: "21:38"
                    real_time_interface_statistics_collection:
                        description:
                        - Enable real-time interface statistics collection.
                        type: bool
                        default: false
                    performance_monitoring:
                        description:
                        - Enable performance monitoring.
                        type: bool
                        default: false
                    strict_config_compliance_mode:
                        description:
                        - Enable strict configuration compliance mode.
                        type: bool
                        default: false
                    # System settings
                    site_id:
                        description:
                        - Site ID for the fabric.
                        type: str
                        default: "4225625065"
                    heartbeat_interval:
                        description:
                        - Heartbeat interval in seconds.
                        type: int
                        default: 190
                    # QoS and queuing
                    default_queuing_policy:
                        description:
                        - Enable default queuing policy.
                        type: bool
                        default: false
                    default_queuing_policy_other:
                        description:
                        - Default queuing policy for other switch types.
                        type: str
                        default: queuing_policy_default_other
                    default_queuing_policy_cloudscale:
                        description:
                        - Default queuing policy for cloudscale switches.
                        type: str
                        default: queuing_policy_default_8q_cloudscale
                    default_queuing_policy_r_series:
                        description:
                        - Default queuing policy for R-series switches.
                        type: str
                        default: queuing_policy_default_r_series
                    aiml_qos:
                        description:
                        - Enable AI/ML QoS optimization.
                        type: bool
                        default: false
                    # DHCP and AAA
                    tenant_dhcp:
                        description:
                        - Enable tenant DHCP.
                        type: bool
                        default: true
                    local_dhcp_server:
                        description:
                        - Enable local DHCP server.
                        type: bool
                        default: false
                    aaa:
                        description:
                        - Enable AAA (Authentication, Authorization, and Accounting).
                        type: bool
                        default: false
                    # Protocol settings
                    cdp:
                        description:
                        - Enable CDP (Cisco Discovery Protocol).
                        type: bool
                        default: false
                    nxapi:
                        description:
                        - Enable NX-API.
                        type: bool
                        default: false
                    nxapi_http:
                        description:
                        - Enable NX-API HTTP.
                        type: bool
                        default: true
                    nxapi_http_port:
                        description:
                        - NX-API HTTP port number.
                        type: int
                        default: 80
                    nxapi_https_port:
                        description:
                        - NX-API HTTPS port number.
                        type: int
                        default: 443
                    snmp_trap:
                        description:
                        - Enable SNMP trap.
                        type: bool
                        default: true
                    # Overlay and EVPN settings
                    route_reflector_count:
                        description:
                        - Number of route reflectors.
                        type: int
                        default: 2
                    advertise_physical_ip:
                        description:
                        - Advertise physical IP addresses.
                        type: bool
                        default: false
                    advertise_physical_ip_on_border:
                        description:
                        - Advertise physical IP on border devices.
                        type: bool
                        default: true
                    anycast_border_gateway_advertise_physical_ip:
                        description:
                        - Advertise physical IP on anycast border gateway.
                        type: bool
                        default: false
                    # VLAN and interface ranges
                    sub_interface_dot1q_range:
                        description:
                        - Sub-interface dot1q range.
                        type: str
                        default: "2-511"
                    object_tracking_number_range:
                        description:
                        - Object tracking number range.
                        type: str
                        default: "100-299"
                    route_map_sequence_number_range:
                        description:
                        - Route map sequence number range.
                        type: str
                        default: "1-65534"
                    ip_service_level_agreement_id_range:
                        description:
                        - IP Service Level Agreement ID range.
                        type: str
                        default: "10000-19999"
                    # Private VLAN
                    private_vlan:
                        description:
                        - Enable private VLAN.
                        type: bool
                        default: false
                    # Advanced features
                    policy_based_routing:
                        description:
                        - Enable policy-based routing.
                        type: bool
                        default: false
                    tcam_allocation:
                        description:
                        - Enable TCAM allocation.
                        type: bool
                        default: true
                    l3_vni_no_vlan_default_option:
                        description:
                        - Enable L3 VNI no VLAN default option.
                        type: bool
                        default: false
                    host_interface_admin_state:
                        description:
                        - Host interface administrative state.
                        type: bool
                        default: true
                    # Routing and STP
                    leaf_to_r_id_range:
                        description:
                        - Enable leaf to router ID range.
                        type: bool
                        default: false
                    # Bootstrap and day0
                    day0_bootstrap:
                        description:
                        - Enable day 0 bootstrap.
                        type: bool
                        default: false
                    bootstrap_multi_subnet:
                        description:
                        - Bootstrap multi-subnet configuration.
                        type: str
                        default: "#Scope_Start_IP, Scope_End_IP, Scope_Default_Gateway, Scope_Subnet_Prefix"
                    # OAM and debugging
                    next_generation_oam:
                        description:
                        - Enable next generation OAM.
                        type: bool
                        default: true
                    ngoam_south_bound_loop_detect:
                        description:
                        - Enable NGOAM south bound loop detection.
                        type: bool
                        default: false
                    # MPLS
                    mpls_handoff:
                        description:
                        - Enable MPLS handoff.
                        type: bool
                        default: false
                    # In-band management
                    inband_management:
                        description:
                        - Enable in-band management.
                        type: bool
                        default: false
                    # SSH
                    advanced_ssh_option:
                        description:
                        - Enable advanced SSH options.
                        type: bool
                        default: false
                    # Server collections
                    ntp_server_collection:
                        description:
                        - List of NTP servers.
                        type: list
                        elements: str
                        default: ["string"]
                    ntp_server_vrf_collection:
                        description:
                        - List of NTP server VRFs.
                        type: list
                        elements: str
                        default: ["string"]
                    dns_collection:
                        description:
                        - List of DNS servers.
                        type: list
                        elements: str
                        default: ["5.192.28.174"]
                    dns_vrf_collection:
                        description:
                        - List of DNS server VRFs.
                        type: list
                        elements: str
                        default: ["string"]
                    syslog_server_collection:
                        description:
                        - List of syslog servers.
                        type: list
                        elements: str
                        default: ["string"]
                    syslog_server_vrf_collection:
                        description:
                        - List of syslog server VRFs.
                        type: list
                        elements: str
                        default: ["string"]
                    syslog_severity_collection:
                        description:
                        - List of syslog severity levels.
                        type: list
                        elements: str
                        default: ["7"]
                    # Extra configuration sections
                    extra_config_leaf:
                        description:
                        - Extra configuration for leaf switches.
                        type: str
                        default: string
                    extra_config_spine:
                        description:
                        - Extra configuration for spine switches.
                        type: str
                        default: string
                    extra_config_tor:
                        description:
                        - Extra configuration for ToR switches.
                        type: str
                        default: string
                    extra_config_aaa:
                        description:
                        - Extra AAA configuration.
                        type: str
                        default: string
                    extra_config_intra_fabric_links:
                        description:
                        - Extra configuration for intra-fabric links.
                        type: str
                        default: string
                    pre_interface_config_leaf:
                        description:
                        - Pre-interface configuration for leaf switches.
                        type: str
                        default: string
                    pre_interface_config_spine:
                        description:
                        - Pre-interface configuration for spine switches.
                        type: str
                        default: string
                    pre_interface_config_tor:
                        description:
                        - Pre-interface configuration for ToR switches.
                        type: str
                        default: string
                    # Netflow settings
                    netflow_settings:
                        description:
                        - Netflow monitoring configuration.
                        type: dict
"""

EXAMPLES = """
# Create a new fabric with basic VXLAN iBGP configuration
- name: Create basic VXLAN iBGP fabric
  cisco.nd.nd_manage_fabric:
    state: merged
    config:
      - name: example-fabric
        category: fabric
        security_domain: default
        management:
          type: vxlanIbgp
          bgp_asn: "65001"
          anycast_gateway_mac: "2020.0000.00aa"
          replication_mode: multicast

# Create a comprehensive fabric with advanced settings
- name: Create comprehensive fabric with advanced settings
  cisco.nd.nd_manage_fabric:
    state: merged
    config:
      - name: advanced-fabric
        category: fabric
        security_domain: all
        location:
          latitude: 37.7749
          longitude: -122.4194
        management:
          type: vxlanIbgp
          bgp_asn: "65001"
          anycast_gateway_mac: "2020.0000.00aa"
          replication_mode: multicast
          fabric_interface_type: p2p
          link_state_routing_protocol: ospf
          overlay_mode: cli
          power_redundancy_mode: redundant
          rendezvous_point_mode: asm
          isis_level: level-2
          stp_root_option: unmanaged
          vpc_peer_keep_alive_option: management
          allow_vlan_on_leaf_tor_pairing: none
          aiml_qos_policy: 400G
          greenfield_debug_flag: disable
          copp_policy: strict
          bgp_authentication: true
          bgp_authentication_key_type: 3des
          bfd: true
          bfd_ibgp: true
          macsec: false
          ptp: false
          real_time_backup: true
          performance_monitoring: true

# Create AI/ML optimized fabric
- name: Create AI/ML optimized fabric
  cisco.nd.nd_manage_fabric:
    state: merged
    config:
      - name: aiml-fabric
        category: fabric
        security_domain: all
        management:
          type: aimlVxlanIbgp
          bgp_asn: "65100"
          anycast_gateway_mac: "2020.0000.00ab"
          replication_mode: ingress
          aiml_qos: true
          aiml_qos_policy: 800G
          fabric_mtu: 9216
          l2_host_interface_mtu: 9216
          default_queuing_policy: true
          tenant_routed_multicast: true
          security_group_tag: true

# Replace existing fabric configuration
- name: Replace fabric configuration
  cisco.nd.nd_manage_fabric:
    state: replaced
    config:
      - name: example-fabric
        category: fabric
        security_domain: default
        management:
          type: vxlanEbgp
          bgp_asn: "65002"
          anycast_gateway_mac: "2020.0000.00ac"
          replication_mode: ingress
          fabric_interface_type: unNumbered
          link_state_routing_protocol: is-is
          isis_level: level-1

# Delete a fabric
- name: Delete fabric
  cisco.nd.nd_manage_fabric:
    state: deleted
    config:
      - name: example-fabric

# Query existing fabrics
- name: Query all fabrics
  cisco.nd.nd_manage_fabric:
    state: query

# Query specific fabric
- name: Query specific fabric
  cisco.nd.nd_manage_fabric:
    state: query
    config:
      - name: example-fabric

# Override fabric configurations (replace all with specified configs)
- name: Override all fabric configurations
  cisco.nd.nd_manage_fabric:
    state: overridden
    config:
      - name: production-fabric
        category: fabric
        security_domain: all
        management:
          type: vxlanIbgp
          bgp_asn: "65000"
          anycast_gateway_mac: "2020.0000.0001"
          replication_mode: multicast
          strict_config_compliance_mode: true
          real_time_backup: true
          scheduled_backup: true
          scheduled_backup_time: "02:00"
      - name: development-fabric
        category: fabric
        security_domain: dev
        management:
          type: vxlanEbgp
          bgp_asn: "65100"
          anycast_gateway_mac: "2020.0000.0002"
          replication_mode: ingress
          greenfield_debug_flag: enable
"""
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-instance-attributes
import copy
import json
import logging
import re
import sys
import traceback
from typing import Protocol, runtime_checkable

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

# from ansible_collections.cisco.nd.plugins.module_utils.models.nd_manage_fabric import FabricModel
from ansible_collections.cisco.nd.plugins.module_utils.models.manage_fabric import FabricModel
from ansible_collections.cisco.nd.plugins.module_utils.nd import NDModule

from ..module_utils.common.log import Log
from ..module_utils.common.models import merge_models, model_payload_with_defaults

try:
    import pydantic as _pydantic  # noqa: F401  # pylint: disable=unused-import

    HAS_PYDANTIC = True
    PYDANTIC_IMPORT_ERROR = None
except ImportError:
    HAS_PYDANTIC = False
    PYDANTIC_IMPORT_ERROR = traceback.format_exc()

try:
    from deepdiff import DeepDiff
except ImportError:
    HAS_DEEPDIFF = False
    DEEPDIFF_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_DEEPDIFF = True
    DEEPDIFF_IMPORT_ERROR = None


class LoggingMixin:
    """
    # Summary

    Plain-Python mixin providing shared logging initialization and `_log_entry()` helper.

    Eliminates four identical `_log_entry()` method definitions across `DiffComparer`,
    `GetHave`, `FabricRepository`, and `StateHandlerMixin`.

    ## Raises

    - None
    """

    def _log_entry(self, method_name: str) -> None:
        """
        # Summary

        Log method entry at DEBUG level.

        ## Raises

        - None
        """
        self.log.debug("ENTERED: %s.%s", self.class_name, method_name)  # type: ignore[attr-defined]


class PathBuilder:
    """
    # Summary

    Centralizes all path construction for the `/api/v1/manage/fabrics` endpoint family.

    Eliminates repeated hardcoded string literals throughout state-handler classes.

    ## Raises

    - None
    """

    _BASE: str = "/api/v1/manage/fabrics"

    @staticmethod
    def collection() -> str:
        """
        # Summary

        Return the base collection path for listing or creating fabrics.

        ## Raises

        - None
        """
        return PathBuilder._BASE

    @staticmethod
    def item(fabric_name: str) -> str:
        """
        # Summary

        Return the path for a single named fabric (PUT / DELETE).

        ## Raises

        - `ValueError` if `fabric_name` is empty or None.
        """
        if not fabric_name:
            raise ValueError("fabric_name must be a non-empty string.")
        return f"{PathBuilder._BASE}/{fabric_name}"


class RequestBuilder:
    """
    # Summary

    Assembles and stores API request dicts into a `requests` mapping.

    ## Raises

    - None
    """

    @staticmethod
    def post(requests: dict, fabric_name: str, payload: dict) -> None:
        """
        # Summary

        Add a POST request entry for the given fabric.

        ## Raises

        - None
        """
        requests[fabric_name] = {
            "verb": "POST",
            "path": PathBuilder.collection(),
            "payload": payload,
        }

    @staticmethod
    def put(requests: dict, fabric_name: str, payload: dict) -> None:
        """
        # Summary

        Add a PUT request entry for the given fabric.

        ## Raises

        - None
        """
        requests[fabric_name] = {
            "verb": "PUT",
            "path": PathBuilder.item(fabric_name),
            "payload": payload,
        }

    @staticmethod
    def delete(requests: dict, fabric_name: str) -> None:
        """
        # Summary

        Add a DELETE request entry for the given fabric.

        ## Raises

        - None
        """
        requests[fabric_name] = {
            "verb": "DELETE",
            "path": PathBuilder.item(fabric_name),
            "payload": "",
        }


class DiffComparer(LoggingMixin):
    """
    # Summary

    Wraps `DeepDiff` to compare two `FabricModel` instances and produce a structured diff.

    Centralizes all three `DeepDiff` call sites in the module:
    - `Merged.update_payload_merged()`
    - `Replaced.build_request()`
    - formerly `compare_fabric_models()` (now deleted)

    ## Raises

    - None
    """

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.class_name = self.__class__.__name__
        self.log = logger or logging.getLogger(f"nd.{self.class_name}")

    def compare(self, have: "FabricModel", want: "FabricModel") -> dict:
        """
        # Summary

        Compare two `FabricModel` instances and return a structured diff dict.

        Returns a dict with keys: `has_differences`, `values_changed`,
        `items_added`, `items_removed`, `full_diff`.

        ## Raises

        - None
        """
        self._log_entry("compare")
        have_dict = have.model_dump(by_alias=True)
        want_dict = want.model_dump(by_alias=True)
        diff = DeepDiff(have_dict, want_dict, ignore_order=True)
        result: dict = {
            "has_differences": bool(diff),
            "values_changed": {},
            "items_added": {},
            "items_removed": {},
        }
        for path_str, change in diff.get("values_changed", {}).items():
            parts, _ = self._resolve_path(path_str, have_dict)
            key = ".".join(parts)
            result["values_changed"][key] = {"have": change["old_value"], "want": change["new_value"]}
            self.log.debug("Changed: %s | have=%s -> want=%s", key, change["old_value"], change["new_value"])
        for path_str in diff.get("dictionary_item_added", set()):
            parts, value = self._resolve_path(path_str, want_dict)
            key = ".".join(parts)
            result["items_added"][key] = value
            self.log.debug("Added:   %s = %s", key, value)
        for path_str in diff.get("dictionary_item_removed", set()):
            parts, value = self._resolve_path(path_str, have_dict)
            key = ".".join(parts)
            result["items_removed"][key] = value
            self.log.debug("Removed: %s = %s", key, value)
        result["full_diff"] = diff
        return result

    def raw_diff(self, have_dict: dict, want_dict: dict) -> "DeepDiff":
        """
        # Summary

        Return a raw `DeepDiff` object for two already-serialized dicts.

        Used by `Merged.update_payload_merged()` which needs the raw diff
        keys `values_changed` and `dictionary_item_added`.

        ## Raises

        - None
        """
        return DeepDiff(have_dict, want_dict, ignore_order=True)

    @staticmethod
    def _resolve_path(path_str: str, source: dict) -> tuple[list[str], object]:
        """
        # Summary

        Parse a DeepDiff path string and resolve its value from `source`.

        ## Raises

        - None
        """
        parts = re.findall(r"'([^']*)'", path_str)
        if not parts:
            parts = path_str.split(".")
            if parts and parts[0] == "root":
                parts = parts[1:]
        value: object = source
        try:
            for part in parts:
                value = value[part]  # type: ignore[index]
        except (KeyError, TypeError):
            value = None
        return parts, value


class GetHave(LoggingMixin):
    """
    Class to retrieve and process fabric state information from Nexus Dashboard (ND).

    This class handles the retrieval of fabric state information from the Nexus Dashboard
    API and processes the response into a list of FabricModel objects.

    Attributes:
        class_name (str): Name of the class.
        log (Logger): Logger instance for this class.
        path (str): API endpoint path for fabric information.
        verb (str): HTTP method used for the request (GET).
        fabric_state (dict): Raw fabric state data retrieved from ND.
        have (list): List of processed FabricModel objects.
        nd: Nexus Dashboard instance for making API requests.

    Methods:
        refresh(): Fetches the current fabric state from Nexus Dashboard.
        validate_nd_state(): Processes the fabric state data into FabricModel objects.
    """

    def __init__(self, nd, logger: logging.Logger | None = None) -> None:
        self.class_name = self.__class__.__name__
        self.log = logger or logging.getLogger(f"nd.{self.class_name}")

        self.path = PathBuilder.collection()
        self.verb = "GET"
        self.fabric_state: dict = {}
        self.have: list = []
        self.nd = nd

        self._log_entry("__init__")

    def refresh(self) -> None:
        """
        # Summary

        Refresh the fabric state by fetching the latest data from the ND API.

        ## Raises

        - None
        """
        self._log_entry("refresh")
        self.fabric_state = self.nd.request(self.path, method=self.verb)

    def validate_nd_state(self) -> None:
        """
        # Summary

        Process raw `fabric_state` data into `FabricModel` objects and populate `self.have`.

        ## Raises

        - `ValueError` if any fabric entry in the response is not a dict.
        """
        self._log_entry("validate_nd_state")

        for fabric in self.fabric_state.get("fabrics"):
            if not isinstance(fabric, dict):
                raise ValueError(f"Fabric data is not a dictionary: {fabric}")

            # Pick Model Based on Fabric Type
            validated_fabric = FabricModel(**fabric)
            # if fabric['management']['type'] == 'vxlanIbgp':
            #     validated_fabric = FabricModel(**fabric)
            # else:
            #     self.log.warning(f"Unsupported fabric management type: {fabric['management']['type']}")
            #     continue

            self.have.append(validated_fabric)
            # Sample Fabric Structure
            # fabric = {
            #     "name": f"{fabric['name']}",
            #     "category": f"{fabric['category']}",
            #     "securityDomain": f"{fabric['securityDomain']}",
            #     "management": {
            #         "type": f"{fabric['management']['type']}",
            #         "bgpAsn": f"{fabric['management']['bgpAsn']}",
            #         "anycastGatewayMac": f"{fabric['management']['anycastGatewayMac']}",
            #         "replicationMode": f"{fabric['management']['replicationMode']}",
            #     }
            # }


class FabricRepository(LoggingMixin):
    """
    # Summary

    Manages the `have`, `want`, and `query` fabric lists and provides
    lookup helpers used by all state-handler classes.

    ## Raises

    - None
    """

    def __init__(self, task_params: dict, have_state: list, logger: logging.Logger | None = None) -> None:
        self.class_name = self.__class__.__name__
        self.log = logger or logging.getLogger(f"nd.{self.class_name}")

        self.state: str = task_params["state"]
        self._have: list = have_state
        self._have_index: dict[str, "FabricModel"] = {f.name: f for f in have_state}
        self.want: list = []
        self.query: list = []
        self.validated: list = []

        self._task_params = task_params
        self._build_want()
        self._log_entry("__init__")

    @property
    def have(self) -> list:
        """
        # Summary

        Return the current list of `FabricModel` objects from the controller.

        ## Raises

        - None
        """
        return self._have

    @have.setter
    def have(self, value: list) -> None:
        """
        # Summary

        Set `have` and rebuild the name-index for O(1) lookups.

        ## Raises

        - None
        """
        self._have = value
        self._have_index = {f.name: f for f in value}

    @property
    def task_params(self) -> dict:
        """
        # Summary

        Return the task parameters dict used to build `want`.

        ## Raises

        - None
        """
        return self._task_params

    def fabric_in_have(self, fabric_name: str) -> "FabricModel | None":
        """
        # Summary

        Return the `FabricModel` from `have` whose `.name` matches
        `fabric_name`, or `None` if not found.

        ## Raises

        - None
        """
        self._log_entry(f"fabric_in_have({fabric_name!r})")
        return self._have_index.get(fabric_name)

    def _build_want(self) -> None:
        """
        # Summary

        Validate task parameters and populate `self.want`.

        For `merged` state with an existing fabric: calls `merge_models(have, want)`.
        Otherwise: calls `model_payload_with_defaults(want)`.

        ## Raises

        - None
        """
        self._log_entry("_build_want")
        for fabric_cfg in self._task_params.get("config") or []:
            have_fabric = self.fabric_in_have(fabric_cfg["name"])
            want_fabric = FabricModel(**fabric_cfg)

            if self.state == "merged" and have_fabric is not None:
                fabric_config_payload = merge_models(have_fabric, want_fabric)
            else:
                fabric_config_payload = model_payload_with_defaults(want_fabric)

            fabric = FabricModel(**fabric_config_payload)
            self.log.debug("Adding fabric to want list: %s", fabric.name)
            self.log.debug("Fabric model created: %s", fabric.model_dump(by_alias=True))
            self.want.append(fabric)


class ResultStore:
    """
    # Summary

    Holds the mutable result state (changed flag, diffs, responses, warnings)
    and the pending API `requests` dict shared by all state-handler classes.

    This is the second half of the former `Common` class (SRP split).
    The first half — fabric list management — lives in `FabricRepository`.

    ## Raises

    - None
    """

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.class_name = self.__class__.__name__
        self.log = logger or logging.getLogger(f"nd.{self.class_name}")
        self.result: dict = {"changed": False, "diff": [], "response": [], "warnings": []}
        self.requests: dict = {}


@runtime_checkable
class StateHandlerProtocol(Protocol):
    """
    # Summary

    Protocol defining the interface contract for all state-handler classes
    (`Merged`, `Replaced`, `Deleted`, `Overridden`, `Query`).

    Enables dict-based strategy dispatch in `main()` and runtime-checkable
    `isinstance` validation.

    ## Raises

    - None
    """

    result_store: ResultStore
    repo: FabricRepository

    def build_request(self) -> None:
        """
        # Summary

        Analyze `repo.want` against `repo.have` and populate
        `result_store.requests` with the necessary API calls.

        For `Query`, this is a no-op.

        ## Raises

        - None
        """  # Protocol stub — body is the docstring


class StateHandlerMixin(LoggingMixin):
    """
    # Summary

    Plain-Python mixin that provides shared initialization for all state-handler
    classes (`Merged`, `Replaced`, `Deleted`, `Overridden`, `Query`).

    Eliminates five identical `__init__` boilerplate blocks and the repeated
    `inspect.stack()[0][3]` + debug log pattern.

    ## Raises

    - None
    """

    def __init__(
        self,
        task_params: dict,
        have_state: list,
        logger: logging.Logger | None = None,
        result_store: ResultStore | None = None,
        repo: FabricRepository | None = None,
    ) -> None:
        self.class_name = self.__class__.__name__
        self.log = logger or logging.getLogger(f"nd.{self.class_name}")
        self.result_store: ResultStore = result_store or ResultStore(logger=self.log)
        self.repo: FabricRepository = repo or FabricRepository(task_params, have_state, logger=self.log)
        self.repo.have = have_state


class Merged(StateHandlerMixin):
    """
    # Summary

    Implements the `merged` state strategy for Cisco ND fabric configurations.

    Compares `repo.want` against `repo.have` and generates POST (create) or PUT (delta update)
    requests. Existing values not present in `want` are preserved.

    ## Raises

    - None
    """

    def __init__(
        self,
        task_params: dict,
        have_state: list,
        logger: logging.Logger | None = None,
        result_store: ResultStore | None = None,
        repo: FabricRepository | None = None,
    ) -> None:
        super().__init__(task_params, have_state, logger, result_store, repo)
        self._diff = DiffComparer(logger=self.log)
        self._log_entry("__init__")
        self.build_request()

    def build_request(self) -> None:
        """
        # Summary

        Compare `repo.want` against `repo.have` and populate `result_store.requests`.

        Issues POST for new fabrics; PUT (delta payload) for existing ones.

        ## Raises

        - None
        """
        self._log_entry("build_request")

        for want_fabric in self.repo.want:
            have_fabric = self.repo.fabric_in_have(want_fabric.name)

            if want_fabric == have_fabric:
                self.log.debug("Fabric %s is already in the desired state, skipping.", want_fabric.name)
                continue

            if not have_fabric:
                self.log.debug("Fabric %s does not exist in the current state, creating it.", want_fabric.name)
                payload = copy.deepcopy(want_fabric.model_dump(by_alias=True))
                RequestBuilder.post(self.result_store.requests, want_fabric.name, payload)
            else:
                diff_result = self._diff.compare(have_fabric, want_fabric)

                if diff_result["has_differences"]:
                    self.log.debug("Fabric %s differences:", want_fabric.name)
                    for key, change in diff_result["values_changed"].items():
                        self.log.debug("  CHANGED  %s: %r -> %r", key, change["have"], change["want"])
                    for key, value in diff_result["items_added"].items():
                        self.log.debug("  ADDED    %s: %r", key, value)
                    for key, value in diff_result["items_removed"].items():
                        self.log.debug("  REMOVED  %s: %r", key, value)
                    self.log.debug("  DIFF DETAILS: %s", diff_result)

                self.log.debug("Fabric %s exists in the current state, updating it.", want_fabric.name)
                payload = self.update_payload_merged(have_fabric, want_fabric)
                RequestBuilder.put(self.result_store.requests, want_fabric.name, payload)

    def _parse_path(self, path: str) -> list[str]:
        """
        # Summary

        Parse a DeepDiff path string into a list of key segments.

        Handles both dot notation (`root.key1.key2`) and bracket notation
        (`root['key1']['key2']`).

        ## Raises

        - None
        """
        self._log_entry("_parse_path")
        # Handle paths like "root.key1.key2"
        if "." in path and "[" not in path:
            parts = path.split(".")
            if parts[0] == "root":
                parts = parts[1:]
            return parts

        # Handle paths like "root['key1']['key2']"
        parts = re.findall(r"'([^']*)'", path)
        return parts

    def _process_values_changed(self, diff: "DeepDiff", updated_payload: dict) -> None:
        """
        # Summary

        Update `updated_payload` with changed values from `diff`.

        ## Raises

        - None
        """
        self._log_entry("_process_values_changed")

        if "values_changed" not in diff:
            return

        # Log the values changed for debugging
        self.log.debug("Values changed: %s", diff["values_changed"])

        for path, change in diff["values_changed"].items():
            parts = self._parse_path(path)

            # Navigate to the correct nested dictionary
            current = updated_payload
            for part in parts[:-1]:
                current = current[part]

            # Update the value
            current[parts[-1]] = change["new_value"]

    def _process_dict_items_added(self, diff: "DeepDiff", updated_payload: dict, want_dict: dict) -> None:
        """
        # Summary

        Add new items to `updated_payload` from `want_dict` based on `diff`.

        ## Raises

        - None
        """
        self._log_entry("_process_dict_items_added")

        if "dictionary_item_added" not in diff:
            return

        # Log the dictionary items added for debugging
        self.log.debug("Dictionary items added: %s", diff["dictionary_item_added"])

        for path in diff["dictionary_item_added"]:
            parts = self._parse_path(path)

            # Navigate to the correct nested dictionary
            current = updated_payload
            for part in parts[:-1]:  # pylint: disable=unused-variable
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Get the value from want
            value = want_dict
            for part in parts:
                value = value[part]

            # Add the new item
            current[parts[-1]] = value

    def update_payload_merged(self, have: "FabricModel", want: "FabricModel") -> dict:
        """
        # Summary

        Calculate differences between `have` and `want` and return a merged payload.

        Uses `DiffComparer.raw_diff()` to find delta, then applies changed values and
        added items on top of a deep copy of `have`.

        ## Raises

        - None
        """
        self._log_entry("update_payload_merged")
        have_dict = have.model_dump(by_alias=True)
        updated_payload = copy.deepcopy(have_dict)
        want_dict = want.model_dump(by_alias=True)

        diff = self._diff.raw_diff(have_dict, want_dict)

        if not diff:
            return updated_payload

        self._process_values_changed(diff, updated_payload)
        self._process_dict_items_added(diff, updated_payload, want_dict)

        return updated_payload


class Replaced(StateHandlerMixin):
    """
    # Summary

    Implements the `replaced` state strategy for Cisco ND fabric configurations.

    Compares `repo.want` against `repo.have` and generates POST (create) or PUT (full replace)
    requests. Unlike `Merged`, the full desired configuration is sent regardless of current state.

    ## Raises

    - None
    """

    def __init__(
        self,
        task_params: dict,
        have_state: list,
        logger: logging.Logger | None = None,
        result_store: ResultStore | None = None,
        repo: FabricRepository | None = None,
    ) -> None:
        super().__init__(task_params, have_state, logger, result_store, repo)
        self._diff = DiffComparer(logger=self.log)
        self._log_entry("__init__")
        self.build_request()

    def build_request(self) -> None:
        """
        # Summary

        Compare `repo.want` against `repo.have` and populate `result_store.requests`.

        Issues POST for new fabrics; PUT with full `want` payload for existing ones.

        ## Raises

        - None
        """
        self._log_entry("build_request")

        for want_fabric in self.repo.want:
            have_fabric = self.repo.fabric_in_have(want_fabric.name)

            if want_fabric == have_fabric:
                self.log.debug("Fabric %s is already in the desired state, skipping.", want_fabric.name)
                continue

            if not have_fabric:
                self.log.debug("Fabric %s does not exist in the current state, creating it.", want_fabric.name)
                payload = copy.deepcopy(want_fabric.model_dump(by_alias=True))
                RequestBuilder.post(self.result_store.requests, want_fabric.name, payload)
            else:
                diff = self._diff.raw_diff(have_fabric.model_dump(), want_fabric.model_dump())
                self.log.debug("Differences for fabric %s: %s", want_fabric.name, diff)
                # For replaced we use the full want payload including default values
                payload = copy.deepcopy(want_fabric.model_dump(by_alias=True))
                RequestBuilder.put(self.result_store.requests, want_fabric.name, payload)


class Deleted(StateHandlerMixin):
    """
    # Summary

    Implements the `deleted` state strategy for Cisco ND fabric configurations.

    Generates DELETE requests for fabrics that exist in both `repo.want` and `repo.have`.

    ## Raises

    - None
    """

    def __init__(
        self,
        task_params: dict,
        have_state: list,
        logger: logging.Logger | None = None,
        result_store: ResultStore | None = None,
        repo: FabricRepository | None = None,
    ) -> None:
        super().__init__(task_params, have_state, logger, result_store, repo)
        self._log_entry("__init__")
        self.build_request()

    def build_request(self) -> None:
        """
        # Summary

        Populate `result_store.requests` with DELETE entries for fabrics in both want and have.

        ## Raises

        - None
        """
        self._log_entry("build_request")
        want_names = {fabric.name for fabric in self.repo.want}
        have_names = {h.name for h in self.repo.have}
        self.delete_fabric_names = sorted(want_names & have_names)
        for fabric_name in self.delete_fabric_names:
            RequestBuilder.delete(self.result_store.requests, fabric_name)


class Overridden(StateHandlerMixin):
    """
    # Summary

    Implements the `overridden` state strategy for Cisco ND fabric configurations.

    Deletes fabrics that exist in `repo.have` but not in `repo.want`, and creates or
    replaces fabrics specified in `repo.want` (delegates to `Replaced`).

    The `Replaced` instance shares `self.result_store` so all requests land in one dict,
    eliminating the old copy-merge loop.

    ## Raises

    - None
    """

    def __init__(
        self,
        task_params: dict,
        have_state: list,
        logger: logging.Logger | None = None,
        result_store: ResultStore | None = None,
        repo: FabricRepository | None = None,
    ) -> None:
        super().__init__(task_params, have_state, logger, result_store, repo)
        self._log_entry("__init__")
        self.build_request()

    def build_request(self) -> None:
        """
        # Summary

        Populate `result_store.requests` with POST/PUT entries (via `Replaced`) for fabrics in
        `repo.want`, and DELETE entries for fabrics in `repo.have` that are not in `repo.want`.

        `Replaced.__init__` calls `build_request()` automatically and writes into the shared
        `result_store`, so this method only needs to add the DELETE entries.

        ## Raises

        - None
        """
        self._log_entry("build_request")
        # Replaced writes POST/PUT entries into the shared result_store during __init__
        _ = Replaced(
            task_params=self.repo.task_params,
            have_state=self.repo.have,
            logger=self.log,
            result_store=self.result_store,
            repo=self.repo,
        )
        want_names = {w.name for w in self.repo.want}
        for fabric in self.repo.have:
            if fabric.name not in want_names:
                RequestBuilder.delete(self.result_store.requests, fabric.name)


class Query(StateHandlerMixin):
    """
    # Summary

    Implements the `query` state strategy for Cisco ND fabric configurations.

    Makes no API mutations; returns current state from `GetHave`. Implements
    `StateHandlerProtocol.build_request()` as a no-op.

    ## Raises

    - None
    """

    def __init__(
        self,
        task_params: dict,
        have_state: list,
        logger: logging.Logger | None = None,
        result_store: ResultStore | None = None,
        repo: FabricRepository | None = None,
    ) -> None:
        super().__init__(task_params, have_state, logger, result_store, repo)
        self._log_entry("__init__")

    def build_request(self) -> None:
        """
        # Summary

        No-op implementation of `StateHandlerProtocol.build_request()`.

        Query does not produce API requests; results are assembled in `main()`.

        ## Raises

        - None
        """
        self._log_entry("build_request")


def main() -> None:  # pylint: disable=too-many-locals
    """
    # Summary

    Main entry point for the `nd_manage_fabric_old` Ansible module.

    ## Raises

    - None
    """
    argument_spec: dict = {}
    argument_spec.update(
        state={
            "type": "str",
            "default": "merged",
            "choices": ["merged", "replaced", "deleted", "overridden", "query"],
        },
        config={"required": False, "type": "list", "elements": "dict"},
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if sys.version_info < (3, 9):
        module.fail_json(msg="Python version 3.9 or higher is required for this module.")

    if not HAS_PYDANTIC:
        module.fail_json(msg=missing_required_lib("pydantic"), exception=PYDANTIC_IMPORT_ERROR)
    if not HAS_DEEPDIFF:
        module.fail_json(msg=missing_required_lib("deepdiff"), exception=DEEPDIFF_IMPORT_ERROR)

    # Logging setup
    try:
        log = Log()
        log.commit()
        mainlog = logging.getLogger("nd.main")
    except ValueError as error:
        module.fail_json(str(error))

    mainlog.info("---------------------------------------------")
    mainlog.info("Starting cisco.nd.manage_fabric module")
    mainlog.info("---------------------------------------------\n")

    nd = NDModule(module)
    task_params = nd.params
    fabrics = GetHave(nd)
    fabrics.refresh()
    fabrics.validate_nd_state()

    # ── Strategy dispatch ────────────────────────
    _STATE_HANDLERS: dict[str, type] = {  # pylint: disable=invalid-name
        "merged": Merged,
        "replaced": Replaced,
        "deleted": Deleted,
        "overridden": Overridden,
        "query": Query,
    }

    state = task_params.get("state")
    handler_cls = _STATE_HANDLERS.get(state)
    if handler_cls is None:
        module.fail_json(msg=f"Invalid state: {state!r}")

    try:
        task = handler_cls(task_params, fabrics.have)
    except ValueError as error:
        module.fail_json(msg=str(error))

    # ── Query short-circuit ───────────────────────────────────────────────
    if state == "query":
        for fabric in fabrics.have:
            task.repo.query.append(fabric.model_dump(by_alias=True))
        task.result_store.result["query"] = task.repo.query
        task.result_store.result["changed"] = False
        module.exit_json(**task.result_store.result)

    # ── Execute accumulated requests ──────────────────────────────────────
    # Sample entry: {'fabric-ansible': {'verb': 'DELETE', 'path': '/api/v1/manage/fabrics/fabric-ansible', 'payload': ''}
    if task.result_store.requests:
        for _, request_data in task.result_store.requests.items():
            verb = request_data["verb"]
            path = request_data["path"]
            payload = request_data["payload"]

            pretty_payload = json.dumps(payload, indent=2, sort_keys=True)
            mainlog.info("Calling nd.request with path: %s, verb: %s, and payload:\n%s", path, verb, pretty_payload)
            response = nd.request(path, method=verb, data=payload if payload else None)
            task.result_store.result["response"].append(response)
            task.result_store.result["changed"] = True
    else:
        mainlog.info("No requests to process")

    module.exit_json(**task.result_store.result)


if __name__ == "__main__":
    main()
