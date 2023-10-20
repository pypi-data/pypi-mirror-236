from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

class Grid:
    def __init__(self, df):
        self.df = df
        self.gb = GridOptionsBuilder.from_dataframe(df)
        self.gb.configure_pagination()
        self.gb.configure_side_bar()
        self.gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        self.gridOptions = self.gb.build()
        
    def render(self, theme_select, grid_height=500):

        # theme : str, optional
        #         theme used by ag-grid. One of:
        #             'streamlit' -> follows default streamlit colors
        #             'light'     -> ag-grid balham-light theme
        #             'dark'      -> ag-grid balham-dark theme
        #             'blue'      -> ag-grid blue theme
        #             'fresh'     -> ag-grid fresh theme
        #             'material'  -> ag-grid material theme
        #         By default 'light'        

        return AgGrid(
            self.df, 
            height = grid_height, 
            gridOptions=self.gridOptions, 
            enable_enterprise_modules=True, 
            fit_columns_on_grid_load=True, 
            theme=theme_select,
            update_mode=GridUpdateMode.SELECTION_CHANGED
        )