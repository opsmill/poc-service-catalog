# POC Service catalog

This repository is a proof of concept for service catalog using Infrahub and Streamlit.

> [!NOTE]
> Setting up the demo currently requires multiple steps, but we are working on adding it as a track on our [lab portal](https://opsmill.instruqt.com/pages/labs).

## Quick start

- Clone this repo `git clone https://github.com/opsmill/poc-service-catalog.git`
- Navigate to the directory `cd poc-service-catalog`
- Setup your poetry environment `poetry shell` and `poetry install`
- Export credentials `export INFRAHUB_ADDRESS='http://localhost:8000'; export INFRAHUB_API_TOKEN='06438eb2-8019-4776-878c-0941b1f1d1ec'`
- Start infrahub `invoke start`
- Load the schema `infrahubctl schema load schemas/`
- Load initial data `infrahubctl object load data/`
- Connect read-only repository `infrahubctl repository add --ref main --read-only infrahub-demo https://github.com/opsmill/poc-service-catalog.git`
- Spin service catalog app `streamlit run service_catalog/🏠_Home_Page.py`

👉 Login to [Infrahub UI](http://localhost:8000/login) on port `8000` with username `admin` and password `infrahub`

👉 You can connect to service catalog on port 8501 [Service catalog](http://localhost:8501/)
