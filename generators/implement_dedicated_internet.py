import random

from infrahub_sdk import InfrahubClient
from infrahub_sdk.generator import InfrahubGenerator
from infrahub_sdk.node import InfrahubNode
from infrahub_sdk.protocols import CoreIPPrefixPool, CoreNumberPool

ACTIVE_STATUS = "active"
SERVICE_VLAN_POOL: str = "Customer vlan pool"
SERVICE_PREFIX_POOL: str = "Customer prefixes pool"

IP_PACKAGE_TO_PREFIX_SIZE: dict[str, int] = {"small": 29, "medium": 28, "large": 27}
IP_PACKAGE_TO_PREFIX_SIZE: dict[str, int] = {"small": 29, "medium": 28, "large": 27}


class ServiceBuilder:
    def __init__(
        self,
        client: InfrahubClient,
        customer_service: InfrahubNode,
    ) -> None:
        # Save parameters
        self.client = client
        self.customer_service = customer_service
        self.allocated_vlan = None
        self.allocated_prefix = None

    async def allocate_vlan(self) -> None:
        """Create a VLAN with ID coming from the pool provided and assign this VLAN to the service."""
        # Get resource pool
        resource_pool = await self.client.get(
            kind=CoreNumberPool,
            name__value=SERVICE_VLAN_POOL,
        )

        # Craft and save the vlan
        self.allocated_vlan = await self.client.create(
            kind="IpamVLAN",
            name=f"vlan__{self.customer_service.service_identifier.value}",
            vlan_id=resource_pool,  # Here we get the vlan ID from the pool
            description=f"VLAN allocated to service {self.customer_service.service_identifier.value}",
            status=ACTIVE_STATUS,
            role="customer",
            l2domain=["default"],
            service=self.customer_service,
        )

        # And save it to Infrahub
        await self.allocated_vlan.save(allow_upsert=True)


class DedicatedInternetGenerator(InfrahubGenerator):
    customer_service = None

    async def generate(self, data: dict) -> None:
        service_dict: dict = data["ServiceDedicatedInternet"]["edges"][0]["node"]

        # Translate the dict to proper object
        self.customer_service = await InfrahubNode.from_graphql(
            client=self.client, data=service_dict, branch=self.branch
        )

        # Allocate the VLAN to the service
        await self.allocate_vlan()

        # Translate teeshirt size to int
        self.prefix_length: int = IP_PACKAGE_TO_PREFIX_SIZE[
            self.customer_service.ip_package.value
        ]

        # Allocate the prefix to the service
        await self.allocate_prefix()

        # Allocate port
        await self.allocate_port()

        # Create L3 interface for gateway
        await self.allocate_gateway()

    async def allocate_vlan(self) -> None:
        """Create a VLAN with ID coming from the pool provided and assign this VLAN to the service."""
        # Get resource pool
        resource_pool = await self.client.get(
            kind=CoreNumberPool,
            name__value=SERVICE_VLAN_POOL,
        )

        # Craft and save the vlan
        self.allocated_vlan = await self.client.create(
            kind="IpamVLAN",
            name=f"vlan__{self.customer_service.service_identifier.value}",
            vlan_id=resource_pool,  # Here we get the vlan ID from the pool
            description=f"VLAN allocated to service {self.customer_service.service_identifier.value}",
            status=ACTIVE_STATUS,
            role="customer",
            l2domain=["default"],
            service=self.customer_service,
        )

        # And save it to Infrahub
        await self.allocated_vlan.save(allow_upsert=True)

    async def allocate_prefix(self) -> None:
        """Allocate a prefix coming from a resource pool to the service."""

        # Get resource pool
        resource_pool = await self.client.get(
            kind=CoreIPPrefixPool,
            name__value=SERVICE_PREFIX_POOL,
        )

        # Craft the data dict for prefix
        prefix_data: dict = {
            "status": "active",
            "description": f"Prefix allocated to service {self.customer_service.service_identifier.value}",
            "service": [self.customer_service.id],
            "role": "customer",
            "vlan": [self.allocated_vlan.id],
        }

        # Create resource from the pool
        self.allocated_prefix = await self.client.allocate_next_ip_prefix(
            resource_pool,
            data=prefix_data,
            prefix_length=self.prefix_length,
            identifier=self.customer_service.service_identifier.value,
        )

        await self.allocated_prefix.save(allow_upsert=True)

    async def allocate_port(self) -> None:
        """Allocate a port to the service."""
        allocated_port = None

        # Fetch interfaces records
        await self.customer_service.dedicated_interfaces.fetch()

        # If we have any interface attached to the service
        if len(self.customer_service.dedicated_interfaces.peers) > 0:
            # Loop over interfaces attached to the service
            for interface in self.customer_service.dedicated_interfaces.peers:
                # Get device related to the interface
                await interface.peer.device.fetch()
                # If the device is "core"
                if interface.peer.device.peer.role.value == "core":
                    # Big assomption but we assume port is already allocated
                    self.index = interface.peer.device.peer.index.value
                    allocated_port = interface
                    break

        # If we don't have yet a port, we need to find one
        if allocated_port is None:
            # Here, we pick randomly. In a real-life scenario, we might want to give this more thought
            self.index = random.randint(1, 2)

            # Find the switch on the site
            switch = await self.client.get(
                kind="DcimDevice",
                location__ids=[self.customer_service.location.id],
                role__value="core",
                index__value=self.index,
            )

            # Fetch switch interface data
            await switch.interfaces.fetch()

            # Find first interface on that switch that is free
            selected_interface = next(
                (
                    interface
                    for interface in switch.interfaces.peers
                    if interface.get().role.value == "customer"
                    and interface.get().status.value == "free"
                    and interface.get().service.id is None
                ),
                None,  # Default value if no match is found
            )

            # If we don't have any interface available
            if selected_interface is None:
                raise Exception(
                    f"There is no physical port to allocate to customer on {switch}"
                )
            else:
                allocated_port = selected_interface

        allocated_port = allocated_port.peer

        # Enforce all params of this interface
        allocated_port.enabled.value = True
        allocated_port.status.value = "active"
        allocated_port.l2_mode.value = "Access"
        allocated_port.role.value = "customer"
        allocated_port.description.value = f"Port allocated to service {self.customer_service.service_identifier.value}"
        allocated_port.speed.value = int(self.customer_service.bandwidth.value)
        allocated_port.service = self.customer_service
        allocated_port.untagged_vlan = self.allocated_vlan

        # Finally save
        await allocated_port.save(allow_upsert=True)

    async def allocate_gateway(self) -> None:
        """Allocate a port to the service."""

        # Find the corresponding router
        router = await self.client.get(
            kind="DcimDevice",
            location__ids=[self.customer_service.location.id],
            role__value="edge",
            index__value=self.index,
        )

        # FIXME: https://github.com/opsmill/infrahub-sdk-python/issues/66
        vlan_id: int = self.allocated_vlan.vlan_id.value["value"]

        # Create interface
        gateway_interface = await self.client.create(
            kind="DcimInterfaceL3",
            name=f"vlan{vlan_id}",
            speed=1000,
            device=router,
            status="active",
            role="customer",
            description=f"Gateway interface for service {self.customer_service.service_identifier.value}",
            enabled=True,
            service=self.customer_service,
            untagged_vlan=self.allocated_vlan,
        )
        await gateway_interface.save(allow_upsert=True)

        # Compute the gateway ip
        address: str = f"{str(next(self.allocated_prefix.prefix.value.hosts()))}/{str(self.prefix_length)}"

        # Create IP object
        self.gateway_ip = await self.client.create(
            kind="IpamIPAddress",
            address=address,
            service=self.customer_service,
            interface=gateway_interface,
        )
        await self.gateway_ip.save(allow_upsert=True)

        # Add gateway to prefix
        self.allocated_prefix.gateway = self.gateway_ip

        # Save prefix
        await self.allocated_prefix.save(allow_upsert=True)
