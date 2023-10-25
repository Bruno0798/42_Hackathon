import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


data = {
    'country': ['Japan', 'China', 'Thailand', 'France', 'Belgium', 'South Korea'],
    'capital': ['Tokyo', 'Beijing', 'Bangkok', 'Paris', 'Brussels', 'Seoul']
}

df = pd.DataFrame(data)
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='unique', use_checkbox=True)
gridoptions = gd.build()

grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

st.write('## Selected')
selected_row = grid_table["selected_rows"]
st.dataframe(selected_row)
