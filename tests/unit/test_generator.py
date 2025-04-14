import pytest
from fast_depends import Provider, dependency_provider
from pytest_httpx import HTTPXMock

from service_catalog.protocols_async import TemplateDcimDevice
from infrahub_sdk.schema.repository import InfrahubRepositoryConfig


def test_generator(repository_config: InfrahubRepositoryConfig):
    generator = repository_config.get_generator_definition("dedicated_internet_generator")
    generator_class = generator.load_class()

    assert generator_class is not None
