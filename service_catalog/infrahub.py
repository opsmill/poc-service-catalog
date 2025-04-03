import os
from functools import wraps
from typing import Any, Callable, Coroutine
from fast_depends import inject, Depends
from typing import Annotated

import streamlit as st
from infrahub_sdk import Config, InfrahubClientSync
from infrahub_sdk.node import InfrahubNodeSync
from infrahub_sdk.branch import BranchData


def get_instance_address() -> str:
    if (
        "infrahub_address" not in st.session_state
        or not st.session_state.infrahub_address
    ):
        st.session_state.infrahub_address = os.environ.get("INFRAHUB_ADDRESS")

    if st.session_state.infrahub_address is None:
        st.exception(Exception("Can't find `INFRAHUB_ADDRESS` in variable envs..."))
    else:
        return st.session_state.infrahub_address

@st.cache_resource
def get_client(branch: str = "main") -> InfrahubClientSync:
    address: str = get_instance_address()
    return InfrahubClientSync(address=address, config=Config(default_branch=branch))


@inject
def get_all_branches(client: InfrahubClientSync = Depends(get_client)) -> dict[str, BranchData]:
    return client.branch.all()


@inject
def create_branch(branch_name: str, client: InfrahubClientSync = Depends(get_client)) -> BranchData:
    return client.branch.create(branch_name=branch_name, sync_with_git=False)


@inject
def create_and_save(
    kind: str, data: dict, branch: str = "main", client: InfrahubClientSync = Depends(get_client)
) -> InfrahubNodeSync:
    infrahub_node = client.create(
        kind=kind,
        branch=branch,
        **data,
    )
    infrahub_node.save(allow_upsert=True)
    return infrahub_node


@inject
def filter_nodes(
    kind: str,
    filters: dict = {},
    include: list[str] = None,
    branch: str = "main",
    client: InfrahubClientSync = Depends(get_client),
) -> list[InfrahubNodeSync]:
    """
    Filter nodes by kind, branch, include and filters.
    NOTE Not sure if we really need this function.
    """
    return client.filters(
        kind=kind,
        branch=branch,
        include=include,
        prefetch_relationships=True,
        **filters,
    )


@inject
def get_dropdown_options(
    kind: str, attribute_name: str, branch: str = "main",
    client: InfrahubClientSync = Depends(get_client),
) -> list[str]:
    """
    Get dropdown options for a given attribute.
    """

    breakpoint()
    # Get schema for this kind
    schema = client.schema.get(kind=kind, branch=branch)

    # Find desired attribute
    matched_attribute = next(
        (att for att in schema.attributes if att.name == attribute_name), None
    )

    if matched_attribute is None:
        raise Exception(f"Can't find attribute `{attribute_name}` for kind `{kind}`")
    else:
        return [choice["name"] for choice in matched_attribute.choices]
