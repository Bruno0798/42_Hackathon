import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid

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
	tabela = conn.query('select wines.wine_name, wines.harvest_year, wines.capacity, wines.location, AVG(prices.price_value) from wines right join prices on wines.wine_id = prices.wine_id group by wines.wine_id', ttl=600)
	return tabela

left_column, right_column = st.columns(2)

with left_column:
	st.header("Wines Table")
	data = carregar_wines_table()
	df = pd.DataFrame(data)
	st.dataframe(
		df,
		column_config={
			"wine_name": "Nome",
			"harvest_year": "Colheita",
			"capacity": st.column_config.NumberColumn("Capacidade", format="%d ml"),
			"location": "Origem",
			"AVG(prices.price_value)": st.column_config.NumberColumn("Preço", format="€%.2f")
		},
		hide_index=True,
	)
	AgGrid(df)

with right_column:
	st.header("Details")

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.wine_name} has a :{row.capacity}:")
