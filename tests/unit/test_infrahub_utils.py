
import pytest
from fast_depends import dependency_provider, inject, Depends, Provider

from service_catalog.infrahub import get_dropdown_options, get_client
from service_catalog.protocols import ServiceDedicatedInternet
from infrahub_sdk import InfrahubClientSync
from pytest_httpx import HTTPXMock


@pytest.fixture
def provider():
    yield dependency_provider
    dependency_provider.clear()


def test_get_dropdown_options(provider: Provider, client: InfrahubClientSync, mock_schema_query_01: HTTPXMock):

    def get_test_client(branch: str = "main"):
        return client

    provider.override(get_client, get_test_client)

    options = get_dropdown_options(kind="ServiceDedicatedInternet", attribute_name="status")
    assert options == ['in-delivery', 'in-decomissioning', 'draft', 'decomissioned', 'active']
