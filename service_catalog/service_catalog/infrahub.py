import os
from functools import wraps
from typing import Any, Callable, Coroutine

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


def with_client(
    func: Callable[..., Coroutine[Any, Any, Any]],
) -> Callable[..., Coroutine[Any, Any, Any]]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        client: InfrahubClientSync = get_client()  # Initialize the client
        return func(client, *args, **kwargs)

    return wrapper


@st.cache_resource
def get_client(branch: str = "main") -> InfrahubClientSync:
    address: str = get_instance_address()
    return InfrahubClientSync(address=address, config=Config(default_branch=branch))


@with_client
def get_all_branches(client: InfrahubClientSync) -> dict[str, BranchData]:
    return client.branch.all()


@with_client
def create_branch(client: InfrahubClientSync, branch_name: str) -> BranchData:
    return client.branch.create(branch_name=branch_name, sync_with_git=False)


@with_client
def create_and_save(
    client: InfrahubClientSync, kind: str, data: dict, branch: str = "main"
) -> InfrahubNodeSync:
    infrahub_node = client.create(
        kind=kind,
        branch=branch,
        **data,
    )
    infrahub_node.save(allow_upsert=True)
    return infrahub_node


@with_client
def filter_nodes(
    client: InfrahubClientSync,
    kind: str,
    filters: dict = {},
    include: list[str] = None,
    branch: str = "main",
) -> list[InfrahubNodeSync]:
    return client.filters(
        kind=kind,
        branch=branch,
        include=include,
        prefetch_relationships=True,
        populate_store=True,
        **filters,
    )


@with_client
def get_dropdown_options(
    client: InfrahubClientSync, kind: str, attribute_name: str, branch: str = "main"
) -> list[str]:
    # Get schema for this kind
    schema = client.schema.get(kind=kind, branch=branch)

    # Find desired attribute
    matched_attribute = next(
        (att for att in schema.attributes if att.name == attribute_name), None
    )

    # Raise exception if we can't find it
    if matched_attribute is None:
        Exception(f"Can't find attribute `{attribute_name}` for kind `{kind}`")
    else:
        # Otherwise return choices
        return [choice["name"] for choice in matched_attribute.choices]
