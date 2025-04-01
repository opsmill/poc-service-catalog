from __future__ import annotations

import asyncio

from typing import Any

import streamlit as st

from protocols.asynchronous import LocationSite, ServiceDedicatedInternet, CoreProposedChange
from service_catalog.infrahub import (
    create_and_save,
    create_branch,
    filter_nodes,
    get_dropdown_options,
)

st.set_page_config(page_title="Dedicated Internet", page_icon="🔌")

st.markdown("# Dedicated Internet")
st.write(
    "This form will allow you to request the implementation of a new dedicated internet service."
)


def get_locations_options() -> list[str]:
    site_list: list[LocationSite] = asyncio.run(
        filter_nodes(kind=LocationSite)
    )

    return [site.shortname.value for site in site_list]


with st.form("new_dedicated_internet_form"):
    # Identifiers
    service_identifier = st.text_input("Service Identifier")
    account_reference = st.text_input("Account Reference")

    # Location
    location_options: list[str] = get_locations_options()
    location = st.selectbox(
        "Location",
        location_options,
    )

    # Bandwidth
    bandwidth_options: list[str] = asyncio.run(
        get_dropdown_options(
            kind=ServiceDedicatedInternet,
            attribute_name="bandwidth",
        )
    )
    bandwidth = st.selectbox(
        "Bandwidth",
        options=bandwidth_options,
    )

    # IP package
    ip_package_options: list[str] = asyncio.run(
        get_dropdown_options(
            kind=ServiceDedicatedInternet,
            attribute_name="ip_package",
        )
    )
    ip_package = st.select_slider(
        "IP Package",
        options=ip_package_options,
    )

    # Submit button
    submitted = st.form_submit_button("Submit", use_container_width=True)

if submitted:
    with st.status("Submitting new service request...", expanded=True) as status:
        # TODO: Implement some validation in the inputs
        st.write("Creating branch...")
        branch_name: str = f"implement_{service_identifier.lower()}"
        asyncio.run(create_branch(branch_name))

        st.write("Creating service object...")
        service: dict[str, Any] = {
            "service_identifier": service_identifier,
            "account_reference": account_reference,
            "status": "draft",
            "bandwidth": bandwidth,
            "ip_package": ip_package,
            "member_of_groups": ["automated_dedicated_internet"],
            "location": [location],
        }
        service_obj: ServiceDedicatedInternet = asyncio.run(
            create_and_save(
                kind=ServiceDedicatedInternet,
                data=service,
                branch=branch_name,
            )
        )

        st.write("Opening proposed change request...")
        proposed_change: dict[str, Any] = {
            "name": f"Implement service {service_identifier.lower()}",
            "source_branch": branch_name,
            "description": "This request is coming from service catalog form!",
            "destination_branch": "main",
            "tags": ["service_request"],
        }

        proposed_change_obj: CoreProposedChange = asyncio.run(
            create_and_save(
                kind=CoreProposedChange,
                data=proposed_change,
            )
        )

        status.update(label="Service request opened!", state="complete", expanded=False)
