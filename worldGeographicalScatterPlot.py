from data import df_confirmados
import plotly.express as px
from plotly.offline import plot

# Geographical Scatter Plot
fig = px.scatter_geo(
    df_confirmados,
    locations="Pais",
    size="Confirmados",
    locationmode="country names",
    hover_name="Pais",
    hover_data={"Confirmados": True, "Pais": False},
    size_max=50,
    opacity=0.6,
    projection='natural earth',
    animation_frame=df_confirmados["Fecha"].astype(str)
)
fig.update_layout(
    title_text='Casos confirmados de COVID-19 a nivel mundial',
    annotations=[
        dict(
            showarrow=False,
            text="Fuente: Johns Hopkins CSSE",
            xanchor='right',
            x=0.85,
            yanchor='top',
            y=-0.05
        ),
        dict(
            showarrow=False,
            text="por Gustavo Guzmán",
            xanchor='right',
            x=0.85,
            yanchor='top',
            y=-0.10
        )
    ],
    geo_scope='world'
)
plot(fig)
