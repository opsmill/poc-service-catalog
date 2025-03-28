from __future__ import annotations

import asyncio

import pandas as pd
import streamlit as st

from protocols.asynchronous import ServiceDedicatedInternet
from service_catalog.infrahub import filter_nodes


st.set_page_config(page_title="Service Requests", page_icon="📦")

st.markdown("# Service Requests")
st.write(
    "You will find on this page all services requests opened. For the one delivered you'll also find allocated assets."
)


def render_asset_table(service: ServiceDedicatedInternet) -> None:
    if service:
        dedicated_interfaces: list = []

        if (
            service.dedicated_interfaces.initialized
            and len(service.dedicated_interfaces.peers) > 0
        ):
            for interface in service.dedicated_interfaces.peers:
                dedicated_interfaces.append(
                    f"{interface.peer.device.hfid[0]}.{interface.peer.name.value}"
                )
        df = pd.DataFrame(
            {
                "vlan_id": [
                    service.vlan.peer.vlan_id.value if service.vlan.initialized else None
                ],
                "gateway_ip_address": [
                    service.gateway_ip_address.peer.display_label
                    if service.gateway_ip_address.initialized
                    else None
                ],
                "prefix": [
                    service.prefix.peer.display_label if service.prefix.initialized else None
                ],
                "dedicated_interfaces": [dedicated_interfaces],
            }
        )
        st.dataframe(
            df,
            column_config={
                "vlan_id": st.column_config.TextColumn(
                    "Vlan ID",
                ),
                "gateway_ip_address": "Gateway Ip Address",
                "prefix": "Prefix",
                "dedicated_interfaces": st.column_config.ListColumn(
                    "Dedicated Interfaces",
                ),
            },
            hide_index=True,
        )


def render_details_table(service: ServiceDedicatedInternet) -> None:
    if service:
        st.dataframe(
            pd.DataFrame(
                {
                    "service_id": [service.service_identifier.value],
                    "account_ref": [
                        service.account_reference.value,
                    ],
                    "status": [service.status.value],
                    "location": [service.location.peer.display_label],
                    "bandwidth": [service.bandwidth.value],
                    "ip_package": [service.ip_package.value],
                }
            ),
            column_config={
                "service_id": "Service Identifier",
                "account_id": "Account Identifier",
                "status": "Status",
                "location": "Location",
                "bandwidth": "Bandwidth",
                "ip_package": "Ip Package",
            },
            hide_index=True,
        )


# Get the data
services: list[ServiceDedicatedInternet] = asyncio.run(
    filter_nodes(
        kind=ServiceDedicatedInternet,  # TODO: So far we only manage this kind
        include=["prefix", "interfaces"],
    )
)

if len(services) == 0:
    st.warning("There is currently no service ...")

# Render the containers
for service in services:
    with st.container(border=True):
        # Display title
        st.title(service.service_identifier.value)

        render_details_table(service)

        st.write("#### Assets")

        if service.status.value == "draft":
            st.warning("Service is in the building process ...")
        else:
            render_asset_table(service)
