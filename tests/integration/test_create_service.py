import logging
from pathlib import Path

import pytest
from fast_depends import Provider, dependency_provider
from streamlit.testing.v1 import AppTest

from infrahub_sdk.client import InfrahubClient, InfrahubClientSync
from infrahub_sdk.protocols import CoreGenericRepository
from infrahub_sdk.spec.object import ObjectFile
from infrahub_sdk.testing.docker import TestInfrahubDockerClient
from infrahub_sdk.testing.repository import GitRepo
from infrahub_sdk.yaml import SchemaFile
from service_catalog.infrahub import get_client
from service_catalog.protocols_async import LocationSite, ServiceDedicatedInternet

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


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
        return SchemaFile.load_from_disk(paths=[schema_dir])

    @pytest.fixture(scope="class")
    def override_client(self, provider: Provider, client_sync: InfrahubClientSync) -> None:
        """
        Override the client that will be returned by FastDepends.
        """

        def get_test_client(branch: str = "main") -> InfrahubClientSync:
            return client_sync

        provider.override(get_client, get_test_client)

    def test_schema_load(
        self, client_sync: InfrahubClientSync, schema_definition: list[SchemaFile], default_branch: str
    ):
        """
        Load the schema from the schema directory into the infrahub instance.
        """
        logger.info("Starting test: test_schema_load")

        client_sync.schema.load(schemas=[item.content for item in schema_definition])
        client_sync.schema.wait_until_converged(branch=default_branch)

    async def test_data_load(self, client: InfrahubClient, data_dir: Path, default_branch: str):
        """
        Load the data from the data directory into the infrahub instance.
        """
        logger.info("Starting test: test_data_load")

        await client.schema.all()
        object_files = sorted(ObjectFile.load_from_disk(paths=[data_dir]), key=lambda x: x.location)

        for idx, file in enumerate(object_files):
            file.validate_content()
            schema = await client.schema.get(kind=file.spec.kind, branch=default_branch)
            for item in file.spec.data:
                await file.spec.create_node(
                    client=client, position=[idx], schema=schema, data=item, branch=default_branch
                )

        sites = await client.all(kind=LocationSite)
        assert len(sites) == 3

    async def test_add_repository(
        self, client: InfrahubClient, root_dir: Path, default_branch: str, remote_repos_dir: Path
    ) -> None:
        """
        Add the local directory as a repository in the infrahub instance in order to validate the import of the repository
        and have the generator operational in infrahub.
        """
        repo = GitRepo(name="infrahub-demo-service-catalog", src_directory=root_dir, dst_directory=remote_repos_dir)
        await repo.add_to_infrahub(client=client)
        in_sync = await repo.wait_for_sync_to_complete(client=client)
        assert in_sync

        repos = await client.all(kind=CoreGenericRepository)
        assert repos

    async def test_portal(self, override_client, client: InfrahubClient, default_branch: str):
        """
        Test the streamlit app on top of a running infrahub instance.
        """
        app = AppTest.from_file("service_catalog/pages/1_🔌_Dedicated_Internet.py").run()

        app.text_input("input-service-identifier").set_value("test-12345").run()
        app.text_input("input-account-reference").set_value("test-12345").run()
        app.selectbox("select-location").select("bru01").run()
        app.selectbox("select-bandwidth").set_value(100).run()
        app.select_slider("select-ip-package").set_value("small").run()
        app.button("FormSubmitter:new_dedicated_internet_form-Submit").click().run(timeout=15)

        services = await client.all(kind=ServiceDedicatedInternet, branch=default_branch)
        assert len(services) == 1
