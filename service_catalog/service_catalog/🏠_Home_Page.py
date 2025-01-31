import streamlit as st

st.set_page_config(
    page_title="Service Catalog",
    page_icon="👋",
)

st.write("# Welcome to Service Catalog! 👋")

st.markdown(
    """
    This portal is designed to facilitate service delivery operations by exposing forms and data in a simplified format.
    You can request new instance of supported service type and track ongoing or active service implementations!
    """
)

st.write("## Request new service")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.header("🔌 Dedicated Internet")
        st.write(
            "This form will allow you to request the implementation of a new dedicated internet service.."
        )
        if st.button("Create", use_container_width=True, key="dedicated_internet"):
            st.switch_page("pages/1_🔌_Dedicated_Internet.py")

with col2:
    with st.container(border=True):
        st.header("🛜 Wireless")
        st.write(
            "This form will allow you to request the implementation of a new wireless service."
        )
        if st.button("Create", use_container_width=True, key="wireless"):
            st.switch_page("pages/2_🛜_Wireless.py")


st.write("## View current requests")

with st.container(border=True):
    st.header("📦 Service requests")
    st.write(
        "You will find on this page all services requests opened. For the one delivered you'll also find allocated assets."
    )
    if st.button("View", use_container_width=True, key="service_requests"):
        st.switch_page("pages/0_📦_Service_Requests.py")
