import pytest
import time
import logging

from streamlit.testing.v1 import AppTest

from pathlib import Path
from typing import Any
from fast_depends import Provider, dependency_provider
from infrahub_sdk.graphql import Mutation
from infrahub_sdk.ctl.utils import load_yamlfile_from_disk_and_exit
from infrahub_sdk.task.models import TaskState
from infrahub_sdk.yaml import SchemaFile
from infrahub_sdk.spec.object import ObjectFile
from infrahub_sdk.testing.docker import TestInfrahubDockerClient
from infrahub_sdk.client import InfrahubClientSync, InfrahubClient
from service_catalog.protocols_async import LocationSite, ServiceDedicatedInternet
from service_catalog.infrahub import get_client
from infrahub_sdk.testing.repository import GitRepo
from infrahub_sdk.protocols import CoreGenericRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TestServiceCatalog(TestInfrahubDockerClient):

    @pytest.fixture(scope="class")
    def provider(self):
        yield dependency_provider
        dependency_provider.clear()


    @pytest.fixture(scope="class")
    def default_branch(self) -> str:
        return "main"

    @pytest.fixture(scope="class")
    def schema_definition(self, schema_dir: Path) -> list[SchemaFile]:
        schema_files = SchemaFile.load_from_disk(paths=[schema_dir])
        return schema_files

    @pytest.fixture(scope="class")
    def override_client(self, provider: Provider, client_sync: InfrahubClientSync) -> None:
        def get_test_client(branch: str = "main") -> InfrahubClientSync:
            return client_sync
        provider.override(get_client, get_test_client)

    def test_schema_load(self, client_sync: InfrahubClientSync, schema_definition: list[SchemaFile], default_branch: str):
        logging.info("Starting test: test_schema_load")

        client_sync.schema.load(schemas=[item.content for item in schema_definition])
        client_sync.schema.wait_until_converged(branch=default_branch)

    async def test_data_load(self, client: InfrahubClient, data_dir: Path, default_branch: str):
        logging.info("Starting test: test_data_load")

        await client.schema.all()
        object_files = sorted(ObjectFile.load_from_disk(paths=[data_dir]), key=lambda x: x.location)

        for idx, file in enumerate(object_files):
            file.validate_content()
            schema = await client.schema.get(kind=file.spec.kind, branch=default_branch)
            for item in file.spec.data:
                await file.spec.create_node(client=client, position=[idx], schema=schema, data=item, branch=default_branch)

        sites = await client.all(kind=LocationSite)
        assert len(sites) == 3

    async def test_add_repository(self, client: InfrahubClient, root_dir: Path, default_branch: str, remote_repos_dir: Path) -> None:

        repo = GitRepo(name="poc-service-catalog", src_directory=root_dir, dst_directory=remote_repos_dir)
        await repo.add_to_infrahub(client=client)
        in_sync = await repo.wait_for_sync_to_complete(client=client)
        assert in_sync

        repos = await client.all(kind=CoreGenericRepository)
        assert repos

    async def test_portal(self, override_client, client: InfrahubClient, default_branch: str):

        app = AppTest.from_file("service_catalog/pages/1_🔌_Dedicated_Internet.py").run()

        app.text_input("input-service-identifier").set_value("test-12345").run()
        app.text_input("input-account-reference").set_value("test-12345").run()
        app.selectbox("select-location").select("bru01").run()
        app.selectbox("select-bandwidth").set_value(100).run()
        app.select_slider("select-ip-package").set_value("small").run()
        app.button("FormSubmitter:new_dedicated_internet_form-Submit").click().run(timeout=15)

        services = await client.all(kind=ServiceDedicatedInternet, branch=default_branch)
        assert len(services) == 1

        breakpoint()
