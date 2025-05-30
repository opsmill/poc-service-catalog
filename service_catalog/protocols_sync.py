#
# Generated by "infrahubctl protocols"
#

from __future__ import annotations

from typing import TYPE_CHECKING

from infrahub_sdk.protocols import (
    BuiltinIPAddress,
    BuiltinIPPrefix,
    CoreArtifactTarget,
    CoreNodeSync,
    CoreObjectTemplateSync,
    CoreProfileSync,
    LineageSource,
)

if TYPE_CHECKING:
    from infrahub_sdk.node import RelatedNodeSync, RelationshipManagerSync
    from infrahub_sdk.protocols_base import (
        BooleanOptional,
        Dropdown,
        DropdownOptional,
        Integer,
        IntegerOptional,
        IPHost,
        IPNetwork,
        String,
        StringOptional,
    )


class DcimConnector(CoreNodeSync):
    connected_endpoints: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class TemplateDcimGenericDevice(CoreNodeSync):
    template_name: String
    member_of_groups: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class TemplateDcimInterface(CoreNodeSync):
    template_name: String
    member_of_groups: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class DcimEndpoint(CoreNodeSync):
    connector: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class LocationGeneric(CoreNodeSync):
    description: StringOptional
    name: String
    shortname: String
    children: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    parent: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class OrganizationGeneric(CoreNodeSync):
    description: StringOptional
    name: String
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class ServiceGeneric(CoreNodeSync):
    account_reference: String
    service_identifier: String
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class DcimGenericDevice(CoreNodeSync):
    description: StringOptional
    name: String
    os_version: StringOptional
    interfaces: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    platform: RelatedNodeSync
    primary_address: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class LocationHosting(CoreNodeSync):
    shortname: String
    devices: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    prefixes: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    vlans: RelationshipManagerSync


class DcimInterface(CoreNodeSync):
    description: StringOptional
    enabled: BooleanOptional
    mtu: IntegerOptional
    name: String
    speed: Integer
    device: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class CoreObjectComponentTemplate(CoreNodeSync):
    template_name: String
    member_of_groups: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class DcimPhysicalDevice(CoreNodeSync):
    position: IntegerOptional
    rack_face: DropdownOptional
    serial: StringOptional
    device_type: RelatedNodeSync
    location: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class LocationCountry(LocationGeneric):
    description: StringOptional
    name: String
    shortname: String
    timezone: StringOptional
    children: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    parent: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class ServiceDedicatedInternet(ServiceGeneric):
    account_reference: String
    bandwidth: Dropdown
    ip_package: Dropdown
    service_identifier: String
    status: DropdownOptional
    dedicated_interfaces: RelationshipManagerSync
    gateway_ip_address: RelatedNodeSync
    location: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    prefix: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    vlan: RelatedNodeSync


class DcimDevice(CoreArtifactTarget, DcimGenericDevice, DcimPhysicalDevice):
    description: StringOptional
    index: IntegerOptional
    name: String
    os_version: StringOptional
    position: IntegerOptional
    rack_face: DropdownOptional
    role: DropdownOptional
    serial: StringOptional
    status: Dropdown
    artifacts: RelationshipManagerSync
    device_type: RelatedNodeSync
    interfaces: RelationshipManagerSync
    location: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    object_template: RelatedNodeSync
    platform: RelatedNodeSync
    primary_address: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class DcimDeviceType(CoreNodeSync):
    description: StringOptional
    full_depth: BooleanOptional
    height: IntegerOptional
    name: String
    part_number: StringOptional
    weight: IntegerOptional
    manufacturer: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    platform: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class IpamIPAddress(BuiltinIPAddress):
    address: IPHost
    description: StringOptional
    fqdn: StringOptional
    interface: RelatedNodeSync
    ip_namespace: RelatedNodeSync
    ip_prefix: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync


class DcimInterfaceL2(DcimInterface, DcimEndpoint):
    description: StringOptional
    enabled: BooleanOptional
    l2_mode: StringOptional
    mtu: IntegerOptional
    name: String
    role: DropdownOptional
    speed: Integer
    status: DropdownOptional
    connector: RelatedNodeSync
    device: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
    tagged_vlan: RelationshipManagerSync
    tags: RelationshipManagerSync
    untagged_vlan: RelatedNodeSync


class DcimInterfaceL3(DcimInterface, DcimEndpoint):
    description: StringOptional
    enabled: BooleanOptional
    mtu: IntegerOptional
    name: String
    role: DropdownOptional
    speed: Integer
    status: DropdownOptional
    connector: RelatedNodeSync
    device: RelatedNodeSync
    ip_addresses: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class IpamL2Domain(CoreNodeSync):
    name: String
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    vlans: RelationshipManagerSync


class OrganizationManufacturer(OrganizationGeneric):
    description: StringOptional
    name: String
    device_type: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    platform: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class LocationMetro(LocationGeneric):
    description: StringOptional
    name: String
    shortname: String
    children: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    parent: RelatedNodeSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class DcimPlatform(CoreNodeSync):
    ansible_network_os: StringOptional
    containerlab_os: StringOptional
    description: StringOptional
    name: String
    napalm_driver: StringOptional
    netmiko_device_type: StringOptional
    nornir_platform: StringOptional
    devices: RelationshipManagerSync
    manufacturer: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class IpamPrefix(BuiltinIPPrefix):
    broadcast_address: StringOptional
    description: StringOptional
    hostmask: StringOptional
    is_pool: BooleanOptional
    is_top_level: BooleanOptional
    member_type: DropdownOptional
    netmask: StringOptional
    network_address: StringOptional
    prefix: IPNetwork
    role: DropdownOptional
    status: Dropdown
    utilization: IntegerOptional
    children: RelationshipManagerSync
    gateway: RelatedNodeSync
    ip_addresses: RelationshipManagerSync
    ip_namespace: RelatedNodeSync
    location: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    organization: RelatedNodeSync
    parent: RelatedNodeSync
    profiles: RelationshipManagerSync
    resource_pool: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
    vlan: RelatedNodeSync


class OrganizationProvider(OrganizationGeneric):
    description: StringOptional
    name: String
    member_of_groups: RelationshipManagerSync
    profiles: RelationshipManagerSync
    sites: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class LocationRack(LocationGeneric, LocationHosting):
    description: StringOptional
    facility_id: StringOptional
    height: IntegerOptional
    name: String
    shortname: String
    children: RelationshipManagerSync
    devices: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    owner: RelatedNodeSync
    parent: RelatedNodeSync
    prefixes: RelationshipManagerSync
    profiles: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync
    vlans: RelationshipManagerSync


class LocationSite(LocationGeneric, LocationHosting):
    description: StringOptional
    facility_id: StringOptional
    name: String
    physical_address: StringOptional
    shortname: String
    children: RelationshipManagerSync
    devices: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    owner: RelatedNodeSync
    parent: RelatedNodeSync
    prefixes: RelationshipManagerSync
    profiles: RelationshipManagerSync
    services: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync
    vlans: RelationshipManagerSync


class IpamVLAN(CoreNodeSync):
    description: StringOptional
    name: String
    role: DropdownOptional
    status: Dropdown
    vlan_id: Integer
    l2domain: RelatedNodeSync
    location: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    prefixes: RelationshipManagerSync
    profiles: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileBuiltinIPAddress(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileBuiltinIPPrefix(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    is_pool: BooleanOptional
    member_type: DropdownOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileBuiltinTag(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimConnector(LineageSource, CoreProfileSync, CoreNodeSync):
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimDevice(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    index: IntegerOptional
    os_version: StringOptional
    position: IntegerOptional
    profile_name: String
    profile_priority: IntegerOptional
    rack_face: DropdownOptional
    role: DropdownOptional
    serial: StringOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimDeviceType(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    full_depth: BooleanOptional
    height: IntegerOptional
    part_number: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    weight: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimEndpoint(LineageSource, CoreProfileSync, CoreNodeSync):
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimGenericDevice(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    os_version: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimInterface(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    enabled: BooleanOptional
    mtu: IntegerOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimInterfaceL2(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    enabled: BooleanOptional
    l2_mode: StringOptional
    mtu: IntegerOptional
    profile_name: String
    profile_priority: IntegerOptional
    role: DropdownOptional
    status: DropdownOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimInterfaceL3(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    enabled: BooleanOptional
    mtu: IntegerOptional
    profile_name: String
    profile_priority: IntegerOptional
    role: DropdownOptional
    status: DropdownOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimPhysicalDevice(LineageSource, CoreProfileSync, CoreNodeSync):
    position: IntegerOptional
    profile_name: String
    profile_priority: IntegerOptional
    rack_face: DropdownOptional
    serial: StringOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileDcimPlatform(LineageSource, CoreProfileSync, CoreNodeSync):
    ansible_network_os: StringOptional
    containerlab_os: StringOptional
    description: StringOptional
    napalm_driver: StringOptional
    netmiko_device_type: StringOptional
    nornir_platform: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileIpamIPAddress(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    fqdn: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileIpamL2Domain(LineageSource, CoreProfileSync, CoreNodeSync):
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileIpamNamespace(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileIpamPrefix(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    is_pool: BooleanOptional
    member_type: DropdownOptional
    profile_name: String
    profile_priority: IntegerOptional
    role: DropdownOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileIpamVLAN(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    role: DropdownOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileLocationCountry(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    timezone: StringOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileLocationGeneric(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileLocationHosting(LineageSource, CoreProfileSync, CoreNodeSync):
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileLocationMetro(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileLocationRack(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    facility_id: StringOptional
    height: IntegerOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileLocationSite(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    facility_id: StringOptional
    physical_address: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileOrganizationGeneric(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileOrganizationManufacturer(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileOrganizationProvider(LineageSource, CoreProfileSync, CoreNodeSync):
    description: StringOptional
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileServiceDedicatedInternet(LineageSource, CoreProfileSync, CoreNodeSync):
    profile_name: String
    profile_priority: IntegerOptional
    status: DropdownOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class ProfileServiceGeneric(LineageSource, CoreProfileSync, CoreNodeSync):
    profile_name: String
    profile_priority: IntegerOptional
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync


class TemplateDcimDevice(LineageSource, TemplateDcimGenericDevice, CoreObjectTemplateSync, CoreNodeSync):
    description: StringOptional
    index: IntegerOptional
    os_version: StringOptional
    position: IntegerOptional
    rack_face: DropdownOptional
    role: DropdownOptional
    serial: StringOptional
    status: DropdownOptional
    template_name: String
    artifacts: RelationshipManagerSync
    device_type: RelatedNodeSync
    interfaces: RelationshipManagerSync
    location: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    platform: RelatedNodeSync
    primary_address: RelatedNodeSync
    related_nodes: RelationshipManagerSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class TemplateDcimInterfaceL2(LineageSource, CoreObjectComponentTemplate, TemplateDcimInterface, CoreNodeSync):
    description: StringOptional
    enabled: BooleanOptional
    l2_mode: StringOptional
    mtu: IntegerOptional
    name: String
    role: DropdownOptional
    speed: Integer
    status: DropdownOptional
    template_name: String
    connector: RelatedNodeSync
    device: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
    tagged_vlan: RelationshipManagerSync
    tags: RelationshipManagerSync
    untagged_vlan: RelatedNodeSync


class TemplateDcimInterfaceL3(LineageSource, CoreObjectComponentTemplate, TemplateDcimInterface, CoreNodeSync):
    description: StringOptional
    enabled: BooleanOptional
    mtu: IntegerOptional
    name: String
    role: DropdownOptional
    speed: Integer
    status: DropdownOptional
    template_name: String
    connector: RelatedNodeSync
    device: RelatedNodeSync
    ip_addresses: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
    tags: RelationshipManagerSync


class TemplateIpamIPAddress(LineageSource, CoreObjectComponentTemplate, CoreNodeSync):
    address: IPHost
    description: StringOptional
    fqdn: StringOptional
    template_name: String
    interface: RelatedNodeSync
    ip_namespace: RelatedNodeSync
    ip_prefix: RelatedNodeSync
    member_of_groups: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync


class TemplateIpamVLAN(LineageSource, CoreObjectComponentTemplate, CoreNodeSync):
    description: StringOptional
    role: DropdownOptional
    status: Dropdown
    template_name: String
    vlan_id: Integer
    l2domain: RelatedNodeSync
    location: RelationshipManagerSync
    member_of_groups: RelationshipManagerSync
    prefixes: RelationshipManagerSync
    related_nodes: RelationshipManagerSync
    service: RelatedNodeSync
    subscriber_of_groups: RelationshipManagerSync
