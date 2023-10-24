import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
	page_title = "Sogrape Wine Dashboard",
	page_icon = "https://upload.wikimedia.org/wikipedia/commons/a/a8/Logo_Sogrape_Original_Legacy_Wines.png",
	layout = "wide",
	initial_sidebar_state = "collapsed"
	)

# Initialize DB connection.
conn = st.experimental_connection('mysql', type='sql')
# Perform Wines Table query.

@st.cache_data
def carregar_wines_table():
	tabela = conn.query('SELECT * from wines;', ttl=600)
	return tabela

left_column, right_column = st.columns(2)

with left_column:
	st.header("Wines Table")
	df = carregar_wines_table()
	st.write(df)

with right_column:
	st.header("Details")

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.wine_name} has a :{row.capacity}:")
