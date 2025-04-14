import pytest
from fast_depends import Provider
from pytest_httpx import HTTPXMock
from streamlit.testing.v1 import AppTest

from infrahub_sdk import Config, InfrahubClientSync
from service_catalog.infrahub import get_client


@pytest.mark.skip(reason="Not working yet")
def test_portal(provider: Provider, mock_schema_query_01: HTTPXMock):
    def get_test_client(branch: str = "main") -> InfrahubClientSync:
        return InfrahubClientSync(address="http://mock", config=Config(insert_tracker=True))

    provider.override(get_client, get_test_client)

    app = AppTest.from_file("service_catalog/pages/1_🔌_Dedicated_Internet.py").run()

    app.text_input("input-service-identifier").set_value("test").run()
    app.text_input("input-account-reference").set_value("test").run()
    app.selectbox("select-location").select("bru01").run()
    app.selectbox("select-bandwidth").set_value(100).run()
    app.select_slider("select-ip-package").set_value("small").run()
    app.button("FormSubmitter:new_dedicated_internet_form-Submit").click().run()
