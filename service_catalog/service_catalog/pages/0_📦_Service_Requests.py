import asyncio

import streamlit as st

from service_catalog.infrahub import filter_nodes

st.set_page_config(page_title="Service Requests", page_icon="📦")

st.markdown("# Service Requests")
st.write(
    "You will find on this page all services requests opened. For the one delivered you'll also find allocated assets."
)

in_progress = asyncio.run(
    filter_nodes(
        kind="CoreProposedChange",
        filters={"tags__name__values": ["service_request"]},
    )
)


def get_service_requests() -> list[dict]:
    data: list[dict] = []

    # First we get in progress requests
    in_progress_requests = asyncio.run(
        filter_nodes(
            kind="CoreProposedChange",
            filters={"tags__name__values": ["service_request"], "state__value": "open"},
        )
    )

    for req in in_progress_requests:
        line: dict = {"title": req.name.value, "status": "in-delivery"}
        data.append(line)

    # Then we get services that are existing in main branch
    # TODO: Here we only display that particular type of service
    # might need to be extended later one
    delivered_services = asyncio.run(
        filter_nodes(
            kind="ServiceDedicatedInternet",
            include=["prefix"],
        )
    )

    # Build the data to be displayed
    for srv in delivered_services:
        # TODO: Manage case where we don't have prefix assigned for instance
        line: dict = {
            "title": srv.service_identifier.value,
            "status": srv.status.value,
            "assets": {},
        }

        # Manage interfaces
        interfaces_value: list = []
        for interface in srv.dedicated_interfaces.peers:
            interfaces_value.append(
                f"{interface.peer.device.hfid[0]}.{interface.peer.name.value}"
            )
        line["assets"]["interfaces"] = "; ".join(interfaces_value)

        # Manage prefix
        line["assets"]["prefix"] = srv.prefix.peer.display_label

        # Manage gateway
        line["assets"]["gateway"] = srv.gateway_ip_address.peer.display_label

        # Add line to overall result
        data.append(line)

    return data


def render_asset_table(data: dict) -> None:
    st.table(data=data)


# Get the data
data = get_service_requests()

# Render the containers
for service_request in data:
    with st.container(border=True):
        # Display title
        st.title(service_request["title"])

        # Display based on status
        if service_request["status"] == "in-delivery":
            # For service in delivery we don't display assets
            st.warning("This service is currently being implemented...")
        elif service_request["status"] == "active":
            st.success("This is service is active!")
            render_asset_table(service_request["assets"])
        elif service_request["status"] in ["in-decomissioning", "decomissioned"]:
            st.warning(f"This is service is {service_request["status"]}!")
            render_asset_table(service_request["assets"])
