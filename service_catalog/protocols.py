#
# Generated by "infrahubctl protocols"
#

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from infrahub_sdk.protocols import CoreNode, BuiltinIPAddress, BuiltinIPAddressSync, BuiltinIPNamespace, BuiltinIPNamespaceSync, BuiltinIPPrefix, BuiltinIPPrefixSync, BuiltinTag, BuiltinTagSync, CoreAccount, CoreAccountGroup, CoreAccountGroupSync, CoreAccountRole, CoreAccountRoleSync, CoreAccountSync, CoreArtifact, CoreArtifactCheck, CoreArtifactCheckSync, CoreArtifactDefinition, CoreArtifactDefinitionSync, CoreArtifactSync, CoreArtifactTarget, CoreArtifactTargetSync, CoreArtifactThread, CoreArtifactThreadSync, CoreArtifactValidator, CoreArtifactValidatorSync, CoreBasePermission, CoreBasePermissionSync, CoreChangeComment, CoreChangeCommentSync, CoreChangeThread, CoreChangeThreadSync, CoreCheck, CoreCheckDefinition, CoreCheckDefinitionSync, CoreCheckSync, CoreComment, CoreCommentSync, CoreCredential, CoreCredentialSync, CoreCustomWebhook, CoreCustomWebhookSync, CoreDataCheck, CoreDataCheckSync, CoreDataValidator, CoreDataValidatorSync, CoreFileCheck, CoreFileCheckSync, CoreFileThread, CoreFileThreadSync, CoreGeneratorCheck, CoreGeneratorCheckSync, CoreGeneratorDefinition, CoreGeneratorDefinitionSync, CoreGeneratorGroup, CoreGeneratorGroupSync, CoreGeneratorInstance, CoreGeneratorInstanceSync, CoreGeneratorValidator, CoreGeneratorValidatorSync, CoreGenericAccount, CoreGenericAccountSync, CoreGenericRepository, CoreGenericRepositorySync, CoreGlobalPermission, CoreGlobalPermissionSync, CoreGraphQLQuery, CoreGraphQLQueryGroup, CoreGraphQLQueryGroupSync, CoreGraphQLQuerySync, CoreGroup, CoreGroupSync, CoreIPAddressPool, CoreIPAddressPoolSync, CoreIPPrefixPool, CoreIPPrefixPoolSync, CoreMenu, CoreMenuItem, CoreMenuItemSync, CoreMenuSync, CoreNodeSync, CoreNumberPool, CoreNumberPoolSync, CoreObjectPermission, CoreObjectPermissionSync, CoreObjectTemplate, CoreObjectTemplateSync, CoreObjectThread, CoreObjectThreadSync, CorePasswordCredential, CorePasswordCredentialSync, CoreProfile, CoreProfileSync, CoreProposedChange, CoreProposedChangeSync, CoreReadOnlyRepository, CoreReadOnlyRepositorySync, CoreRepository, CoreRepositorySync, CoreRepositoryValidator, CoreRepositoryValidatorSync, CoreResourcePool, CoreResourcePoolSync, CoreSchemaCheck, CoreSchemaCheckSync, CoreSchemaValidator, CoreSchemaValidatorSync, CoreStandardCheck, CoreStandardCheckSync, CoreStandardGroup, CoreStandardGroupSync, CoreStandardWebhook, CoreStandardWebhookSync, CoreTaskTarget, CoreTaskTargetSync, CoreThread, CoreThreadComment, CoreThreadCommentSync, CoreThreadSync, CoreTransformJinja2, CoreTransformJinja2Sync, CoreTransformPython, CoreTransformPythonSync, CoreTransformation, CoreTransformationSync, CoreUserValidator, CoreUserValidatorSync, CoreValidator, CoreValidatorSync, CoreWebhook, CoreWebhookSync, InternalAccountToken, InternalAccountTokenSync, InternalRefreshToken, InternalRefreshTokenSync, IpamNamespace, IpamNamespaceSync, LineageOwner, LineageOwnerSync, LineageSource, LineageSourceSync

if TYPE_CHECKING:
    from infrahub_sdk.node import RelatedNodeSync, RelationshipManagerSync
    from infrahub_sdk.protocols_base import (
        AnyAttribute,
        AnyAttributeOptional,
        String,
        StringOptional,
        Integer,
        IntegerOptional,
        Boolean,
        BooleanOptional,
        DateTime,
        DateTimeOptional,
        Dropdown,
        DropdownOptional,
        HashedPassword,
        HashedPasswordOptional,
        MacAddress,
        MacAddressOptional,
        IPHost,
        IPHostOptional,
        IPNetwork,
        IPNetworkOptional,
        JSONAttribute,
        JSONAttributeOptional,
        ListAttribute,
        ListAttributeOptional,
        URL,
        URLOptional,
    )


class DcimConnector(CoreNode):
    connected_endpoints: RelationshipManagerSync


class DcimEndpoint(CoreNode):
    connector: RelatedNodeSync


class ServiceGeneric(CoreNode):
    service_identifier: String
    account_reference: String


class OrganizationGeneric(CoreNode):
    name: String
    description: StringOptional
    tags: RelationshipManagerSync


class LocationGeneric(CoreNode):
    name: String
    shortname: String
    description: StringOptional
    tags: RelationshipManagerSync


class DcimGenericDevice(CoreNode):
    name: String
    description: StringOptional
    os_version: StringOptional
    interfaces: RelationshipManagerSync
    tags: RelationshipManagerSync
    primary_address: RelatedNodeSync
    platform: RelatedNodeSync


class LocationHosting(CoreNode):
    shortname: String
    prefixes: RelationshipManagerSync
    devices: RelationshipManagerSync


class DcimInterface(CoreNode):
    name: String
    description: StringOptional
    speed: Integer
    mtu: Integer
    enabled: Boolean
    device: RelatedNodeSync
    tags: RelationshipManagerSync


class DcimPhysicalDevice(CoreNode):
    position: IntegerOptional
    serial: StringOptional
    rack_face: Dropdown
    device_type: RelatedNodeSync
    location: RelatedNodeSync


class LocationCountry(LocationGeneric):
    timezone: StringOptional


class ServiceDedicatedInternet(ServiceGeneric):
    status: Dropdown
    bandwidth: Dropdown
    ip_package: Dropdown
    location: RelatedNodeSync
    dedicated_interfaces: RelationshipManagerSync
    vlan: RelatedNodeSync
    gateway_ip_address: RelatedNodeSync
    prefix: RelatedNodeSync


class DcimDevice(CoreArtifactTarget, DcimGenericDevice, DcimPhysicalDevice):
    status: Dropdown
    role: DropdownOptional
    index: IntegerOptional


class DcimDeviceType(CoreNode):
    name: String
    description: StringOptional
    part_number: StringOptional
    height: Integer
    full_depth: Boolean
    weight: IntegerOptional
    platform: RelatedNodeSync
    manufacturer: RelatedNodeSync
    tags: RelationshipManagerSync


class IpamIPAddress(BuiltinIPAddress):
    fqdn: StringOptional
    interface: RelatedNodeSync


class DcimInterfaceL2(DcimInterface, DcimEndpoint):
    role: DropdownOptional
    status: DropdownOptional
    l2_mode: StringOptional


class DcimInterfaceL3(DcimInterface, DcimEndpoint):
    role: DropdownOptional
    status: DropdownOptional
    ip_addresses: RelationshipManagerSync


class IpamL2Domain(CoreNode):
    name: String
    vlans: RelationshipManagerSync


class OrganizationManufacturer(OrganizationGeneric):
    device_type: RelationshipManagerSync
    platform: RelationshipManagerSync


class LocationMetro(LocationGeneric):
    pass


class DcimPlatform(CoreNode):
    name: String
    description: StringOptional
    nornir_platform: StringOptional
    napalm_driver: StringOptional
    netmiko_device_type: StringOptional
    ansible_network_os: StringOptional
    containerlab_os: StringOptional
    devices: RelationshipManagerSync
    manufacturer: RelatedNodeSync


class IpamPrefix(BuiltinIPPrefix):
    status: Dropdown
    role: DropdownOptional
    organization: RelatedNodeSync
    location: RelatedNodeSync
    gateway: RelatedNodeSync


class OrganizationProvider(OrganizationGeneric):
    pass


class LocationRack(LocationGeneric, LocationHosting):
    facility_id: StringOptional
    height: Integer
    owner: RelatedNodeSync


class LocationSite(LocationGeneric, LocationHosting):
    facility_id: StringOptional
    physical_address: StringOptional
    owner: RelatedNodeSync


class IpamVLAN(CoreNode):
    name: String
    description: StringOptional
    vlan_id: Integer
    status: Dropdown
    role: DropdownOptional
    location: RelationshipManagerSync
    prefixes: RelationshipManagerSync
    l2domain: RelatedNodeSync
