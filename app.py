import streamlit as st
from scrape import scrape_page
import pandas as pd

st.title("Web Scraping App")
page_url = st.text_input("Wather page Link")

if st.button("Start Scraping"):
    data_scraping_state = st.text("Scraping Page Content ...")
    data = scrape_page(page_url)
    if isinstance(data, pd.DataFrame):
        st.dataframe(data)
        data_scraping_state.text("")
