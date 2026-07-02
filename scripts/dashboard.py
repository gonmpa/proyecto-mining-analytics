import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import duckdb
import pandas as pd

print("Conectando a DuckDB y extrayendo el Cubo de Datos...")
db_path = '/home/gonsa/mi_proyecto_mining/data/mining_analytics.db'

# Consulta SQL que une la tabla de hechos con las dimensiones
query = """
    SELECT 
        f.inventory_year, 
        f.tonnage, 
        c.commodity_desc, 
        m.mine_name, 
        m.latitude, 
        m.longitude
    FROM main.fct_inventory f
    JOIN main.dim_commodities c ON f.commodity_code = c.commodity_code
    JOIN main.dim_mines m ON f.mineral_id = m.mineral_id
    WHERE f.tonnage > 0 AND m.latitude IS NOT NULL
"""

con = duckdb.connect(db_path)
df = con.execute(query).df()
con.close()

print(f"Datos cargados: {len(df)} registros. Levantando servidor Dash...")

# Inicializar aplicación
app = dash.Dash(__name__)

# Obtener lista de minerales para el filtro interactivo
minerales = df['commodity_desc'].dropna().unique()
mineral_defecto = minerales[0] if len(minerales) > 0 else None

# Diseño de la página web
app.layout = html.Div([
    html.H1("Plataforma de Telemetría e Inventario Minero", style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    html.Div([
        html.Label("Selecciona un Mineral para filtrar todos los gráficos:"),
        dcc.Dropdown(
            id='filtro-mineral',
            options=[{'label': m, 'value': m} for m in sorted(minerales)],
            value=mineral_defecto,
            clearable=False
        )
    ], style={'width': '40%', 'margin': 'auto', 'paddingBottom': '30px', 'fontFamily': 'Arial'}),

    # Fila 1: Dos gráficos
    html.Div([
        dcc.Graph(id='grafico-tendencia', style={'display': 'inline-block', 'width': '50%'}),
        dcc.Graph(id='grafico-barras', style={'display': 'inline-block', 'width': '50%'}),
    ]),

    # Fila 2: Mapa
    html.Div([
        dcc.Graph(id='mapa-minas', style={'width': '100%'})
    ])
])

# Lógica de interactividad
@app.callback(
    [Output('grafico-tendencia', 'figure'),
     Output('grafico-barras', 'figure'),
     Output('mapa-minas', 'figure')],
    [Input('filtro-mineral', 'value')]
)
def actualizar_dashboard(mineral_seleccionado):
    df_filtrado = df[df['commodity_desc'] == mineral_seleccionado]
    
    # 1. Gráfico de Líneas: Evolución temporal
    df_anio = df_filtrado.groupby('inventory_year', as_index=False)['tonnage'].sum()
    fig_lineas = px.line(df_anio, x='inventory_year', y='tonnage', 
                         title=f'Producción Histórica: {mineral_seleccionado}', markers=True)
    
    # 2. Gráfico de Barras: Top 10 Minas
    df_minas = df_filtrado.groupby('mine_name', as_index=False)['tonnage'].sum().nlargest(10, 'tonnage')
    fig_barras = px.bar(df_minas, x='mine_name', y='tonnage', 
                        title=f'Top 10 Minas por Volumen: {mineral_seleccionado}')
    
    # 3. Mapa Interactivo de las ubicaciones mineras
    fig_mapa = px.scatter_mapbox(df_filtrado, lat="latitude", lon="longitude", hover_name="mine_name",
                                 hover_data=["tonnage"], size="tonnage", 
                                 color_discrete_sequence=["#FF5733"], zoom=3, height=400,
                                 title=f'Distribución Geográfica de Minas: {mineral_seleccionado}')
    fig_mapa.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":40,"l":0,"b":0})
    
    return fig_lineas, fig_barras, fig_mapa

if __name__ == '__main__':
    # host='0.0.0.0' permite que Windows vea el servidor levantado en Ubuntu
    app.run(debug=True, host='0.0.0.0', port=8050)
