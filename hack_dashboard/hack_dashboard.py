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
	data_wines = carregar_wines_table()
	df_wines = pd.DataFrame(data_wines)
	gd_wines = GridOptionsBuilder.from_dataframe(df_wines)
	gd_wines.configure_selection(selection_mode='unique', use_checkbox=True)
	gd_wines.configure_column(field="wine_name", header_name="Nome", width = 245, autoHeight=True)
	gd_wines.configure_column(field="wine_id", hide=True)
	gd_wines.configure_column(field="harvest_year", header_name="Colheita", width = 85, valueFormatter="value == '0' ? '' : value")
	gd_wines.configure_column(field="capacity", header_name="Capacidade", width = 110)
	gd_wines.configure_column(field="location", header_name="Origem", width = 80)
	gd_wines.configure_column(field="AVG(prices.price_value)", header_name="Preço", width = 80, type="customNumericFormat", precision=2)
	gridoptions = gd_wines.build()
	grid_table_wines = AgGrid(df_wines, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

def first(list):
    for i in list:
        return i

table_wines = grid_table_wines["selected_rows"]
wine_id = None
for wine in table_wines:
	if(wine):
		wine_id = wine.get('wine_id')
		break

wine_id = str(wine_id)
@st.cache_data
def carregar_store_prices(wine_id):
	tabela_stores = conn.query('SELECT stores.store_name, prices.price_value, prices.timestamp, prices.store_id, prices.wine_id FROM prices INNER JOIN stores on prices.store_id = stores.store_id WHERE wine_id = '+wine_id+' and timestamp IN (SELECT max(timestamp) FROM prices where wine_id = '+wine_id+' GROUP BY store_id)', ttl=600)
	return tabela_stores

with right_column:
	st.header("Details")
	data_stores =  carregar_store_prices(wine_id)
	df_stores = pd.DataFrame(data_stores)
	gd_stores = GridOptionsBuilder.from_dataframe(df_stores)
	gd_stores.configure_selection(selection_mode='multiple', use_checkbox=True)
	gd_stores.configure_column(field="store_name", header_name="Loja", width = 245, autoHeight=True)
	gd_stores.configure_column(field="price_value", header_name="Preço", width = 80, type="customNumericFormat", precision=2)
	gd_stores.configure_column(field="timestamp", header_name="Data", width = 150)
	gd_stores.configure_column(field="wine_id", hide=True)
	gd_stores.configure_column(field="store_id", hide=True)
	gridoptions = gd_stores.build()
	grid_table = AgGrid(df_stores, gridOptions=gridoptions,
					update_mode=GridUpdateMode.SELECTION_CHANGED)
	table_stores = grid_table["selected_rows"]
	wine_id_stores = None
	store_id_stores = None
	data_stores = pd.DataFrame()
	for wine in table_stores:
			wine_id_stores = str(wine.get('wine_id'))
			store_id_stores = str(wine.get('store_id'))
			store_name = wine.get('store_name')
			query_stores = conn.query('select tb.price_value from (SELECT price_value, DATE(timestamp) as date FROM prices WHERE wine_id = '+wine_id_stores+' and store_id = '+store_id_stores+') as tb group by tb.date order by tb.date', ttl=600)
			data_stores[store_name] = query_stores

chart_data = pd.DataFrame(data_stores)
st.line_chart(chart_data)
