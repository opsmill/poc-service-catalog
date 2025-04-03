import pytest
from fast_depends import Provider, dependency_provider
from pytest_httpx import HTTPXMock

from infrahub_sdk import InfrahubClientSync
from service_catalog.infrahub import get_client, get_dropdown_options


@pytest.fixture
def provider():
    yield dependency_provider
    dependency_provider.clear()


def test_get_dropdown_options(provider: Provider, client: InfrahubClientSync, mock_schema_query_01: HTTPXMock):
    def get_test_client(branch: str = "main") -> InfrahubClientSync:
        return client

    provider.override(get_client, get_test_client)

    options = get_dropdown_options(kind="ServiceDedicatedInternet", attribute_name="status")
    assert options == [
        "in-delivery",
        "in-decomissioning",
        "draft",
        "decomissioned",
        "active",
    ]
