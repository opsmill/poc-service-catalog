import os
from functools import wraps
from typing import Any, Callable, Coroutine

import streamlit as st
from infrahub_sdk import Config, InfrahubClient, InfrahubNode
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
    async def wrapper(*args, **kwargs):
        client: InfrahubClient = get_client()  # Initialize the client
        return await func(client, *args, **kwargs)

    return wrapper


@st.cache_resource
def get_client(branch: str = "main") -> InfrahubClient:
    address: str = get_instance_address()
    return InfrahubClient(address=address, config=Config(default_branch=branch))


@with_client
async def get_all_branches(client: InfrahubClient) -> dict[str, BranchData]:
    return await client.branch.all()


@with_client
async def create_branch(client: InfrahubClient, branch_name: str) -> BranchData:
    return await client.branch.create(branch_name=branch_name, sync_with_git=False)


@with_client
async def create_and_save(
    client: InfrahubClient, kind: str, data: dict, branch: str = "main"
) -> InfrahubNode:
    infrahub_node = await client.create(
        kind=kind,
        branch=branch,
        **data,
    )
    await infrahub_node.save(allow_upsert=True)
    return infrahub_node


@with_client
async def filter_nodes(
    client: InfrahubClient,
    kind: str,
    filters: dict = {},
    include: list[str] = None,
    branch: str = "main",
) -> list[InfrahubNode]:
    return await client.filters(
        kind=kind,
        branch=branch,
        include=include,
        prefetch_relationships=True,
        populate_store=True,
        **filters,
    )


@with_client
async def get_dropdown_options(
    client: InfrahubClient, kind: str, attribute_name: str, branch: str = "main"
) -> list[str]:
    # Get schema for this kind
    schema = await client.schema.get(kind=kind, branch=branch)

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
