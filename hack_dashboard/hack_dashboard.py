import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

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
	tabela = conn.query('select wines.wine_name, wines.wine_id, wines.harvest_year, wines.capacity, wines.location, AVG(prices.price_value) from wines right join prices on wines.wine_id = prices.wine_id group by wines.wine_id', ttl=600)
	return tabela

left_column, right_column = st.columns(2)

with left_column:
	st.header("Wines Table")
	data = carregar_wines_table()
	df = pd.DataFrame(data)
	gd = GridOptionsBuilder.from_dataframe(df)
	gd.configure_selection(selection_mode='unique', use_checkbox=True)
	gd.configure_column(field="wine_name", header_name="Nome", width = 245, autoHeight=True)
	gd.configure_column(field="wine_id", hide=True)
	gd.configure_column(field="harvest_year", header_name="Colheita", width = 85, valueFormatter="value == '0' ? '' : value")
	gd.configure_column(field="capacity", header_name="Capacidade", width = 110, valueFormatter="value ml")
	gd.configure_column(field="location", header_name="Origem", width = 80)
	gd.configure_column(field="AVG(prices.price_value)", header_name="Preço", width = 80, type="customNumericFormat", precision=2)

	gridoptions = gd.build()
	grid_table = AgGrid(df, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

def first(list):
    for i in list:
        return i

table = grid_table["selected_rows"]
wine_id = None
for wine in table:
	if(wine):
		wine_id = wine.get('wine_id')
		break

wine_id = str(wine_id)

@st.cache_data
def carregar_store_prices(wine_id):
	tabela = conn.query('SELECT stores.store_name, prices.price_value, prices.timestamp FROM prices inner join stores on prices.store_id = stores.store_id where prices.wine_id ='+wine_id+' and TIMESTAMP >= CURDATE() ', ttl=600)
	return tabela

with right_column:
	st.header("Details")
	data =  carregar_store_prices(wine_id)
	df = pd.DataFrame(data)
	gd = GridOptionsBuilder.from_dataframe(df)
	gd.configure_selection(selection_mode='multiple', use_checkbox=True)
	gd.configure_column(field="store_name", header_name="Loja", width = 245, autoHeight=True)
	gd.configure_column(field="price_value", header_name="Preço", width = 80, type="customNumericFormat", precision=2)
	gd.configure_column(field="timestamp", header_name="Data", width = 150)
	gridoptions = gd.build()
	grid_table = AgGrid(df, gridOptions=gridoptions,
					update_mode=GridUpdateMode.SELECTION_CHANGED)
	chart_data = pd.DataFrame(np.random.randn(20, 3))
	st.line_chart(chart_data)
	#st.dataframe(wine_id)
