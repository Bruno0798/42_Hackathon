import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
	page_title = "Sogrape Wine Dashboard",
	page_icon = "https://upload.wikimedia.org/wikipedia/commons/a/a8/Logo_Sogrape_Original_Legacy_Wines.png",
	layout = "centered",
	initial_sidebar_state = "collapsed"
	)

left_column, right_column = st.columns(2)

with left_column:
	st.header("Wines Table")

with right_column:
	st.header("Details")

st.write(st.secrets)

# Initialize connection.
conn = st.experimental_connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from wines;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.wine_name} has a :{row.capacity}:")
