# POC Service catalog

This repository is a proof of concept for service catalog built while writting a blog post.

> [!NOTE]
> Setting up the demo currently requires multiple steps, but we are working on adding it as a track on our [lab portal](https://opsmill.instruqt.com/pages/labs).

## Quick start

- Clone this repo `git clone https://github.com/opsmill/poc-service-catalog.git`
- Run Infrahub with docker compose `curl https://infrahub.opsmill.io | docker compose -f - up -d`
- Login to Infrahub UI `http://127.0.0.1:8000/login` with login `admin` and password `infrahub`
- Browse to [Create group page](http://127.0.0.1:8000/objects/CoreGroup) and create a new `StandardGroup` with name `automated_dedicated_internet`
- Browse to [Create repository page](http://127.0.0.1:8000/objects/CoreGenericRepository) and create a new `ReadOnlyRepository` with location `https://github.com/opsmill/poc-service-catalog.git`
- Navigate to service catalog directory `cd service_catalog`
- Setup your poetry environment `poetry shell` and `poetry install`
- Export credentials `export INFRAHUB_ADDRESS='http://localhost:8000'; export INFRAHUB_API_TOKEN='06438eb2-8019-4776-878c-0941b1f1d1ec'`
- Load data using CTL `infrahubctl run ../schemas/data.py`
- Spin service catalog app `streamlit run service_catalog/landing.py`

At this point you can connect to service catalog on port 8501 [http://localhost:8501/](Service catalog)
